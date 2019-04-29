------------------- Fee Generating Transactions ------------------------


/*   Includes single-tag fare payments, BART and Caltrain exits, Golden Gate 
Transit entries, add-value transactions, opt-out purse refunds and pass use, 
including institutional passes. Does not include transfers or transactions 
where fee value is $0 (e.g., issuance of free cards, zero-value tags in 
dual-tag systems, etc.). */


select count(*)
from sfofaretransaction
where (subtype = 1 or subtype = 2 or subtype = 4) and
extract(month from convert_timezone('UTC','PST', generationtime)) = 10 and 
extract(year from convert_timezone('UTC','PST', generationtime)) = 2018;  -- 23,564,830
