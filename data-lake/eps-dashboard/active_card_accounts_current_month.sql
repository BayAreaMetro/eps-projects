------------------- Active Card Accounts ------------------------
/* Active cards are those that have been used at least once within the last 12 months.  */


select count(distinct applicationserialnumber)
from sfofaretransaction
where
    generationtime > date_trunc('month',  (current_date) - interval '1 year')
    and generationtime < date_trunc('month', current_date)
    and applicationserialnumber < 2000000000
; -- 2,837,277  -- ran 1/14/2019
  -- 2,828,408 in January 2018 Report

select count(distinct applicationserialnumber)
from sfofaretransaction
where
    generationtime > date_trunc('month',  (current_date-58) - interval '1 year')
    and generationtime < date_trunc('month', current_date-58)
    and applicationserialnumber < 2000000000
;  -- ran on 2/27/2019 -- 2,890,741  -- 2,828,408 in January 2018 Report
