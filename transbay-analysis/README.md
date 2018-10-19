Estimating AC Transit Transbay Ridership
================
Yeeling Tse
8/21/2018

-   [Goal](#goal)
-   [Data Sources](#data-sources)
-   [Methodology](#methodology)
    -   [Preparing the data](#preparing-the-data)
    -   [Classifying transbay routes](#classifying-transbay-routes)
-   [Results](#results)

Goal
----

Estimate ridership for AC Transit transbay routes F, O, and NL from 2014-2017 as per SPUR's data request.

Data Sources
------------

Load in Clipper data

``` r
library(readxl)
transactions <- read_excel("~/Downloads/AC Transit_transbay Oct %2717 info_SGB.xlsx")
```

Methodology
-----------

### Preparing the data

Add a column indicating the year of the transaction to later accomodate for the fare change in 2017

``` r
add_year <- function(tr_df) {
  year <- lubridate::year(tr_df$HourOfDay)
  tr_df <- tr_df %>%
    cbind(year)
  return(tr_df)
}
```

### Classifying transbay routes

*The following functions create 'rules' for what constitutes a transbay ride. These rules will modify an `is_transbay` column to be a boolean column that indicates a transbay ride.*

Because local and transbay rides have different fares, we can begin classifying rides through the amount paid.

``` r
classify_fare <- function(tr_df) {
  tr_df <- tr_df %>% 
    dplyr::mutate(is_transbay = case_when(PurseAmount %in% c(4.20, 2.10) & ContractID == 0 & year != 2017 ~ 1)) %>%
    dplyr::mutate(is_transbay = ifelse(PurseAmount %in% c(4.50, 2.20) & ContractID == 0 & year == 2017, 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(PurseAmount %in% c(2.00, 1.00) & ContractID == 0 & year != 2017, 0, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(PurseAmount %in% c(2.15, 1.05) & ContractID == 0 & year == 2017, 0, is_transbay))
    return(tr_df)
}
```

AC Transit has many products, some of which are restricted to either local or transbay rides. Continue classifying rides through the product used.

``` r
classify_contract <- function(tr_df) {
  tr_df <- tr_df %>%
    dplyr::mutate(is_transbay = ifelse(ContractID %in% c(121, 196), 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(ContractID %in% c(119, 101, 195, 120), 0, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(PurseAmount %in% c(2.10, 1.05) & ContractID %in% c(119, 101, 195, 120) & year != 2017, 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(PurseAmount %in% c(2.25, 1.10) & ContractID %in% c(119, 101, 195, 120) & year == 2017, 1, is_transbay))
    return(tr_df)
}
```

Transbay and local rides have different fares when transferring from certain operators.

``` r
classify_transfer_fare <- function(tr_df) {
  tr_df <- tr_df %>%
    dplyr::mutate(is_transbay = ifelse(ContractID %in% c(192, 193, 194, 197, 198) & PurseAmount %in% c(2.10, 1.05) & year != 2017, 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(ContractID %in% c(192, 193, 194, 197, 198) & PurseAmount %in% c(2.35, 1.15) & year == 2017, 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(ContractID %in% c(192, 193, 194, 197, 198) & PurseAmount == 0, 0, is_transbay))      
  return(tr_df)
}    
```

Transbay and local rides have different fares when transferring from BART.

``` r
classify_bart_transfer_fare <- function(tr_df) {
  tr_df <- tr_df %>%
    dplyr::mutate(is_transbay = ifelse(ContractID == 199 & PurseAmount %in% c(2.70, 1.60) & year != 2017, 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(ContractID == 199 & PurseAmount %in% c(2.85, 1.65) & year == 2017, 1, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(ContractID == 199 & PurseAmount %in% c(1.50, 0.5) & year != 2017, 0, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(ContractID == 199 & PurseAmount %in% c(0.70, 0.55) & year == 2017, 0, is_transbay)) %>%
    dplyr::mutate(is_transbay = ifelse(ContractID == 199 & PurseAmount == 1.65 & FareCategory == 0 & year == 2017, 0, is_transbay))
  return(tr_df)
}
```

This leaves us with rides with a subsidized product or a day pass, which are free regardless of a local or transbay ride. For these, we can estimate transbay riders depending on where they transferred from. For example, let's assume that AC Transit riders coming from MUNI are taking transbay rides.

``` r
classify_transfer_operator <- function(tr_df) {
  tr_df <- tr_df %>%
    dplyr::mutate(is_transbay = ifelse(ContractID %in% c(110, 114, 118, 170) & TransferOperator == 18, 1, is_transbay))
  return(tr_df)
}
```

*Now that we have these rules, apply them to our `transactions` table to modify the `is_transbay` column.*

``` r
transbay <- transactions %>% 
  add_year() %>%
  classify_fare() %>%
  classify_contract() %>%
  classify_transfer_fare() %>%
  classify_bart_transfer_fare() %>%
  classify_transfer_operator()
```

Not all the transactions were able to be classified using this method, so sort records into transbay, not transbay, and unknown.

``` r
transbay <- transbay %>%
  mutate(transbay_count = ifelse(is_transbay == 1, record_count, 0)) %>%
  mutate(non_transbay_count = ifelse(is_transbay == 0, record_count, 0)) %>%
  mutate(unknown = ifelse(is.na(is_transbay), record_count, 0))

transbay[is.na(transbay)] <- 0
```

Results
-------

Create results table and write to csv.

``` r
transbay_routes_by_year <- transbay %>%
  group_by(year, RouteID) %>%
  summarise(total_rides = sum(record_count), transbay_rides = sum(transbay_count), non_transbay_rides = sum(non_transbay_count), unknown_rides = sum(unknown))

write.csv(transbay_routes_by_year, "transbay.csv")
```
