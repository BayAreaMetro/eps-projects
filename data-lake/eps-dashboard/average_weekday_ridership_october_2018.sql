-- Average Weekday Ridership --
select avg(countperday) from
(
    select count(*) as countperday,
    extract(day from generationtime) as day,
    extract(dow from generationtime) as dow
    from sfofaretransaction
    where
        extract(month from generationtime) = 10 and
        extract(year from generationtime) = 2018 and
        (subtype = 1 or subtype = 2  or subtype = 4)
    group by 2,3
) where dow between 1 and 5
; -- 877,404 different than report because of Caltrain
