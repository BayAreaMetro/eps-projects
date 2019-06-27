-- weekly average weekday ridership --
select operatorid, 
date_part('week', generationtime::date) as week,
count(*)/5 as weekly_avg
    from sfofaretransaction
    where (subtype = 1 or subtype = 2  or subtype = 4) and 
        extract(dow from generationtime) between 1 and 5
    group by operatorid, week
    order by 1, 2;

-- joined weekly average with week start --
select op_counts.operatorid, op_counts.week, op_counts.weekly_avg, mondays.monday
from 
(select operatorid, 
date_part('week', generationtime::date) as week,
count(*)/5 as weekly_avg
    from clipper.sfofaretransaction
    where (subtype = 1 or subtype = 2  or subtype = 4) and 
        extract(dow from generationtime) between 1 and 5
    group by operatorid, week) as op_counts
left join
(select date_part('week', generationtime::date) as week, cast(generationtime as date) as monday
from clipper.sfofaretransaction
where extract(dow from generationtime) = 1) as mondays
on op_counts.week = mondays.week;
