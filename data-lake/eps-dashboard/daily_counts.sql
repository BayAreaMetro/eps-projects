-- Daily Counts --

select operatorid, 
date_trunc('day', generationtime) as day,
count(*) as daily_count
from clipper.sfofaretransaction
where subtype in (1, 2, 4)
group by 1, 2
order by 1, 2;
