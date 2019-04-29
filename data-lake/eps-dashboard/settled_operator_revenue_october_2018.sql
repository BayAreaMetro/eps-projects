------------------- Settled Transit Operator Revenue ------------------------
/* This query is short many $.  No one has been able to get it close. */


select sum(purseamount) + 0.9375*sum(GenericECashPurseAmount)/100.00
from clipper.sfofaretransaction
where extract(month from convert_timezone('UTC','PST', generationtime)) = 10 and 
      extract(year from convert_timezone('UTC','PST', generationtime)) = 2018
;  -- 54,667,144.28750000  ($59,496,240 in Report)
