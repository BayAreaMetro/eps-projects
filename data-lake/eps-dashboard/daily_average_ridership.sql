-- daily average ridership --
select operatorid, date_part('year', generationtime::date) as year, date_part('month', generationtime::date) as month,
date_part('day', generationtime::date) as day,
count(*) as daily_count
    from sfofaretransaction
    where (subtype = 1 or subtype = 2  or subtype = 4) and 
        extract(dow from generationtime) between 1 and 5
    group by 1, 2, 3, 4
    order by 1, 2, 3, 4;


--- daily average ridership with one date column -- 
select operatorid, cast(generationtime as date) as date,
count(*) as daily_count
    from sfofaretransaction
    where (subtype = 1 or subtype = 2  or subtype = 4) and 
        extract(dow from generationtime) between 1 and 5
    group by 1, 2
    order by 1, 2;

-- joined to particpantname --
select date, daily_count, participantname
from 
(select operatorid, cast(generationtime as date) as date,
count(*) as daily_count
    from clipper.sfofaretransaction
    where (subtype = 1 or subtype = 2  or subtype = 4) and 
        extract(dow from generationtime) between 1 and 5
    group by 1, 2) as op_counts
left join
(select * from clipper.participants) as p
on p.participantid = op_counts.operatorid;
