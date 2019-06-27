------------------- Average Weekday Ridership ------------------------
/*   Includes average daily number of boardings, including transfers 
but excluding some Caltrain monthly pass trips (Caltrain only requires 
monthly pass customers to tag their cards once at the beginning of each month).*/


select avg(countperday) from
(
    select count(*) as countperday,
    extract(day from generationtime) as day,
    extract(dow from generationtime) as dow
    from sfofaretransaction
    where
        extract(month from convert_timezone('UTC','PST', generationtime)) = 10 and
        extract(year from convert_timezone('UTC','PST', generationtime)) = 2018 and
        (subtype = 1 or subtype = 2  or subtype = 4)
    group by 2,3
) where dow between 1 and 5
; -- 877,404 for October 2018. different than report because of Caltrain ridership approximations


-- one month's average weekday ridership with operators' name --
select parts.participantname, op_counts.operatorid, op_counts.avg_weekday
from 
(select operatorid, avg(countperday) as avg_weekday 
from
(
    select operatorid, count(*) as countperday,
    extract(day from generationtime) as day,
    extract(dow from generationtime) as dow
    from sfofaretransaction
    where
        extract(month from generationtime) = 10 and
        extract(year from generationtime) = 2018 and
        (subtype = 1 or subtype = 2  or subtype = 4)
    group by operatorid, day, dow
) where dow between 1 and 5
group by operatorid) as op_counts
left join
(select participantid, participantname
from "clipper"."participants") as parts
on op_counts.operatorid = parts.participantid
;
