Estimating AC Transit Tranbay Ridership
================
Yeeling Tse
8/21/2018

-   [Goal](#goal)
-   [Data Sources](#data-sources)
-   [Methodology](#methodology)
    -   [Preparing the data](#preparing-the-data)
    -   [Classifying transbay routes](#classifying-transbay-routes)

Goal
----

Estimate ridership for AC Transit transbay routes F, O, and NL from 2014-2017 as per SPUR's data request.

Data Sources
------------

Clipper datalake

``` r
source('~/Documents/connect_db.R')  
rs <- connect_rs()
```

Methodology
-----------

### Preparing the data

``` r
library(clpr)   
library(dplyr)  
library(dbplyr)
library(lubridate)  
library(odbc)
library(DBI)
source('~/Documents/connect_db.R')  
rs <- connect_rs()  
```

Load a sample of transactions.

``` r
tr_df <- sample_day_of_transactions(rs, '2016-10-17')   
```

Filter transactions to AC Transit routes F, O, or NL and add product descriptions.

``` r
ac_routes <- tr_df %>%
    dplyr::filter(operatorid == 1) %>%
    dplyr::filter(routename %in% c('F', 'O', 'NL')) %>%
    clpr::get_product_description()
```

### Classifying transbay routes

The following steps all add to a boolean column `is_transbay` created in the table that indicates a transbay ride.

Because local and transbay rides have different fares, we can begin classifying rides through the amount paid.

``` r
classify_fare <- tr_df %>% 
    dplyr::mutate(is_transbay = case_when(purseamount %in% c(4.2, 2.1) & contractid == 0 ~ 1)) %>%
    dplyr::mutate(is_transbay = ifelse(purseamount %in% c(2, 1), 0, is_transbay))
```

AC Transit has many products, some of which are restricted to either local or transbay rides. Continue classifying rides through the product used.

``` r
classify_contract <- classify_fare %>%
    dplyr::mutate(is_transbay = ifelse(contractid %in% c(121, 196), 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(contractid %in% c(119, 101, 195, 120), 0, is_transbay))
```

Transbay and local rides have different fares when transferring from certain operators.

``` r
classify_transfer_fare <- classify_contract %>%
    dplyr::mutate(is_transbay = ifelse(contractid %in% c(192, 193, 194, 197, 198) & purseamount %in% c(2.1, 1.05), 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(contractid %in% c(192, 193, 194, 197, 198) & purseamount == 0, 0, is_transbay))      
```

Transbay and local rides have different fares when transferring from BART.

``` r
classify_bart_transfer_fare <- classify_transfer_fare %>%
    dplyr::mutate(is_transbay = ifelse(contractid == 199 & purseamount %in% c(2.7, 1.6), 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(contractid == 199 & purseamount %in% c(1.5, 0.5), 0, is_transbay))
```

This leaves us with rides with a subsidized product or a day pass, which are free regardless of a local or transbay ride. For these, we can estimate transbay riders depending on where they transferred from. For example, let's assume that AC Transit riders coming from MUNI are taking transbay rides.

``` r
classify_from_muni <- classify_bart_transfer_fare %>%
    dplyr::mutate(is_transbay = ifelse(contractid %in% c(110, 114, 118, 170) & transferoperator == 18, 1, is_transbay))
```

Find the total amount of transbay rides.

``` r
num_transbay <- sum(classify_from_muni$is_transbay)
```
