# Clipper Prediction Models

Using machine learning models, we wanted to see how well we could predicted Clipper card rides accross all transit operators.  The data is queried from the Data Lake's clipper.sfofaretransaction table. Different data sources across the agency will have different numbers.  This is to demonstrate that ridership can be predicted, but the counts may not match up with official accounts from crystal reports.

To improve prediction accuaray, we joined that data with tables containing weather and holidays.  This data came from:
* [Holidays](https://gist.github.com/shivaas/4758439)
* [Weather Download](https://www.ncdc.noaa.gov/cdo-web/datasets#GHCND)  (It must be requested for download.)


Included are notebooks for Random Forest Models, which using the following features:
    
    Time Based Features: day of week, day of the month, month, year.
    
    Holiday Indicator: 1 if this day was a Holiday and 0 if it was not.
    
    Holiday Indicators for individual Holidays (1 if this day was Christmas, 0 otherwise etc.)
    
    The min tempertaure, max temperature, and perciptation in San Francisco for that day.

    The number of clipper rides on the pervious day (yesterday_swipes).
    
    The number of clipper rides on that day last year (year_ago_swipes).
    
    The average daily weekday ridership for the pervious month (weekday_avg_month_prior).
    
    The average daily weekend ridership for the pervious month (weekdend_avg_month_prior).
    
    
