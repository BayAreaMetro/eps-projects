------------------- Unique Cards Used ------------------------


select count(distinct applicationserialnumber) as unique_cards
from "clipper"."sfofaretransaction"
where extract(month from convert_timezone('UTC', 'PST', generationtime)) = 10 and 
extract(year from convert_timezone('UTC', 'PST', generationtime)) = 2018
and applicationserialnumber < 2000000000;

 -- 1205508
