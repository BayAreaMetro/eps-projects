--- October 18 Ridership Counts --

-- Using MTC Admin Lake (dev doesn't have 2018) and matches Mike Lee's Numbers exactly

/*  Ridership by operator for (transaction count
OperatorID) Oct ’18, adjusted for UTC, filtering out limited use cards, 
selecting subtypes 1,2, and 4.  Caltrain requires adjustment due to monthly pass use.
This query does not adjust Caltrain */


select parts.participantname, op_counts.transaction_count
from 
(select operatorid, count(*) as transaction_count
from "clipper"."sfofaretransaction"
where  (subtype = 1 or subtype = 2  or subtype = 4) and
extract(month from convert_timezone('UTC', 'PST', generationtime)) = 10 and 
extract(year from convert_timezone('UTC', 'PST', generationtime)) = 2018
and applicationserialnumber < 2000000000
group by operatorid) as op_counts
LEFT JOIN 
(select participantid, participantname
from "clipper"."participants") as parts
ON op_counts.operatorid = parts.participantid;
