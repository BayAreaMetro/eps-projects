# EPS Dashboard
 
These queries are represetative of metrics in monthly Clipper and FasTrak reports shared with top excutives.  

The primaray audience would be the product mangers and then key stake holders.

These are queries from the Data Lake, and the numbers will not match the numbers in Crystal Reports.  We learned by talking with various member of the eps team that these numbers will never match up.  When possible, we've included how off different metrics were.

We also created a dimension table to improve query performance in dashboards, that sql is included as well.

## Prototype Dashboards

* [Clipper and FasTrak Google Data Studio Version One](https://datastudio.google.com/u/1/reporting/1-pk3dgT9gWh6QeuIiekzveX7SCSEqIpl/page/eTzn)

## Personally Identifiable Infomration (PII) Data

All of these queries aggergate the data at a level that excludes PII.  Any data/query dealing with PII data would only be seen internally. 

* [Diagram of Clipper Tables with PII Columns Highlighted](https://github.com/BayAreaMetro/eps-projects/blob/master/data-lake/documentations/PII_Clipper_Data_Store_ERD.pdf)

## Metrics

**Average Weekday Ridership**

Includes average daily number of boardings, including transfers but excluding some Caltrain monthly pass trips (Caltrain only requires monthly pass customers to tag their cards once at the beginning of each month). 

**Fee Generating Transactions**

Includes single-tag fare payments, BART and Caltrain exits, Golden Gate  Transit entries, add-value transactions, opt-out purse refunds and pass use,  including institutional passes. Does not include transfers or transactions where fee value is $0 (e.g., issuance of free cards, zero-value tags in dual-tag systems, etc.).

**Active Card Accounts**

Active cards are those that have been used at least once within the last 12 months.

**Unique Cards**

Number of unique clipper cards used in one month.

**Monthly Clipper Transactions**

Both the total number of clipper transcations and the total number of clipper fare only transcations are important. There must be 20 million of each every month to avoid higher fees.

**Revenue for Clipper and FasTrak**

Tracked on a monthly bias.

**Total Number of Clipper Swipes and FasTrak Tags**

Tracked on a monthly bias.

 
