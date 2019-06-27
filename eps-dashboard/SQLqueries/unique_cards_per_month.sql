-- Unique Cards Per Month --
 
select date_trunc('month', generationtime) as month, count(distinct applicationserialnumber)
from clipper.sfofaretransaction 
where generationtime > dateadd(year, -1, month) 
and date_trunc('month', generationtime) <= month 
and applicationserialnumber < 2000000000 
group by 1
order by 1; 

-- GOPI excel says 900,488 for Feb 2016 (we are 500 off)
