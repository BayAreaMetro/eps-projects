-- This query generates data for machine learning models to predict clipper swipes
-- for all operators
-- join with yesterday's ridership, a year ago's ridership, month priors weekday avg, month priors weekend avg
select * from
(select date, year, month, day,  month || year as month_year, extract('dow' from date) as dow, year, weekend_flag,
 date-1 as yesterday, date-365 as year_ago,
 extract('month' from add_months(date,-1)) || extract('year' from add_months(date,-1)) as prior_month_year,
case when month in (12, 1, 2) then 1
when month in (2, 4, 5) then 2
when month in (6, 7, 8) then 3
else 4 end as season,
count(*) as swipes
from clipper."sfofaretransaction_time_dims"
where (subtype = 1 or subtype = 2 or subtype = 4)
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) as c
left join
(select date as y_date,
count(*) as yesterday_swipes
from clipper."sfofaretransaction_time_dims"
where (subtype = 1 or subtype = 2 or subtype = 4)
group by 1) as y
on c.yesterday = y.y_date
left join
(select date as ly_date,
count(*) as year_ago_swipes
from clipper."sfofaretransaction_time_dims"
where (subtype = 1 or subtype = 2 or subtype = 4)
group by 1) as ly
on c.year_ago = ly.ly_date
left join
(select mwd_month_year, weekday_avg_month_prior
from
(select month || year as mwd_month_year, weekend_flag, count(*)/count(distinct date) as weekday_avg_month_prior
from clipper."sfofaretransaction_time_dims"
where (subtype = 1 or subtype = 2 or subtype = 4)
group by 1, 2)
where weekend_flag is FALSE) as mwd
on c.prior_month_year = mwd.mwd_month_year
left join
(select mwe_month_year, weekend_avg_month_prior
from
(select month || year as mwe_month_year, weekend_flag, count(*)/count(distinct date) as weekend_avg_month_prior
from clipper."sfofaretransaction_time_dims"
where (subtype = 1 or subtype = 2 or subtype = 4)
group by 1, 2)
where weekend_flag is TRUE) as mwe
on c.prior_month_year = mwe.mwe_month_year;
