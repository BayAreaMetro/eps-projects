Understanding Clipper System Overlap
================
Yeeling Tse
12/4/2018

-   [Goal](#goal)
-   [Data Sources](#data-sources)
-   [Methodology](#methodology)
-   [Results](#results)

Goal
----

Understand how Clipper card holders ride multiple transit operators. Specifically, create a frequency matrix to understand system overlap changes with varying frequency levels: i.e. for Clipper card holders who touch BART 10x per month how much do they use any another transit operator? Or for Clipper card holders who touch Muni 40x per month, how much do they touch any another operator?

Data Sources
------------

Clipper Data: Load a week's worth of transactions

``` r
tr_df <- data.frame()

for (i in 01:07){
  day_trans <- day_of_transactions(rs, paste0('2016-10-', i)) %>% filter(subtype != 3 & subtype != 5)
  tr_df <- tr_df %>% rbind(day_trans)
}
```

Methodology
-----------

Find ride frequency counts for each user-operator pairing

``` r
freq <- tr_df %>% group_by(cardid_anony, participantname) %>% summarise(n = n())
```

Divide into operator in question vs. all other (ie. BART)

``` r
bart <- freq %>% filter(participantname == 'BART')
other <- freq %>% filter(participantname != 'BART') %>% group_by(cardid_anony) %>% summarise(other_n = sum(n))
```

Full join by user to compare BART and non-BART frequencies

``` r
by_user <- full_join(bart, other, by = 'cardid_anony')
by_user[is.na(by_user)] <- 0
```

Categorize frequencies into ranges for the frequency matrix

``` r
spread_bart <- by_user %>%
  dplyr::mutate(bart_range = case_when(n == 0 ~ '0')) %>%
  dplyr::mutate(bart_range = ifelse(0 < n & n <= 10, '1-10', bart_range)) %>%
  dplyr::mutate(bart_range = ifelse(10 < n & n <= 20, '11-20', bart_range)) %>%
  dplyr::mutate(bart_range = ifelse(20 < n & n <= 39, '21-39', bart_range)) %>%
  dplyr::mutate(bart_range = ifelse(n > 39, '40+', bart_range))

spread_other <- spread_bart %>%
  dplyr::mutate(other_range = case_when(other_n == 0 ~ '0')) %>%
  dplyr::mutate(other_range = ifelse(0 < other_n & other_n <= 10, '1-10', other_range)) %>%
  dplyr::mutate(other_range = ifelse(10 < other_n & other_n <= 20, '11-20', other_range)) %>%
  dplyr::mutate(other_range = ifelse(20 < other_n & other_n <= 39, '21-39', other_range)) %>%
  dplyr::mutate(other_range = ifelse(other_n > 39, '40+', other_range))
```

Results
-------

Create final frequency matrix

``` r
final <- spread_other %>% group_by(bart_range, other_range) %>%
  summarise(total = n()) %>%
  spread(bart_range, total)
```
