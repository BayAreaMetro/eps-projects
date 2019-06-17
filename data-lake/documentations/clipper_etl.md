# Clipper Data Transfer and ETL Set Up
Quinn Keck and Jacques Sham<br>

## Background

This documentation outlines the plan to transfer the Clipper data from Clipper Data Store to the Data Lake on Redshift, and the set up of ongoing ETL process to upload the clipper data to the Data Lake moving forward. The goal is to centralize Clipper data and thus to develop dashboard or tools for reporting and analysis. 

## Personas
Cubic: The consultant and data steward of Clipper. Cubic handles all Clipper daily operations for MTC and periodically send Clipper data to MTC. Terry Smith is contact person.
<br>
Data Engineers: Kearey Smith and USF interns, including Jacques Sham, Anastasia Keck
<br>
EPS staffs: EPS staffs, including Lysa Hale, Mike Lee, Ed Meng

## Tools
Data Clipper Store - MS SQL<br>
Data Lake - AWS S3, AWS Redshift<br>
ETL - Trifacta, Matillion<br>

## Implementation Before Data Lake Project
After the Clipper data is generated in Clipper operators, the data is store in XML format and be sent to Cubic's operational data store, where Cubic only store the data up to 1 year. After Cubic transform the data in tabular format, the data is sent to the Clipper Data Store and Crystal Reports. Crystal Reports is the reporting software which the EPS staffs obtain the data from. The reports generated from Crystal Reports is too detail and in PDF that EPS staffs do not find it useful or any way to aggregate the numbers for reporting. Crystal Reports does not provide dashboard or any dynamic functions for us to build a dashboard from it.
<br>

Crystal Reports was selected to report Clipper data in MTC was unclear as this is the decision made in 90's and the fact that most of the transit operator use Crystal Reports for reporting purpose. The flexibility of Crystal Reports was little as it only has pre-built reports. In the below screenshot Figure 1 is the main page of Crystal Reports; the folders on the left show all categories of pre-built reports you may look at.
<br>

![Screenshot](image/fig1.png)
Figure 1

<br><br>
If you download the report from Crystal Reports, you will go to the report and hit "Schedule" (When you hit "View" or "View Latest Instance" give you a blank gray page). Please see Figure 2.
![Screenshot](image/fig2.png)
Figure 2
<br><br>
![Screenshot](image/fig3.png)
Figure 3
<br><br>
Once you hit schedule, you are able to select date range and output format. Note that you are only allow to select report up to 90 days prior. The useful report format is in PDF; although it is possible to export to TSV, the format is not in a desired tabular format that could be easily to ETL from such TSV file to push to relational database. Figure 4 is the screenshot of the report in PDF format and Figure 5 is the screenshot of the report TSV format. You may see the format TSV format is not in tabular form because there is a column header associated with every row that means the file is downloaded to be the order of header, observation, header, observation...instead of having header, and all observations.<br>
![Screenshot](image/fig4.png)
Figure 4<br>
![Screenshot](image/fig5.png)
Figure 5
<br><br>
Due to the given constraints, it makes it harder to ETL clipper data to Redshift.<br>
Prior to the Data Lake Implementation, the flow of reporting Clipper data is below.<br>
![Screenshot](image/fig6.png)
Figure 6
<br>
Based on the data flow before implementing Data Lake, Cubic is responsible to upload the data to:<br>
1) Crystal Reports<br>
2) Clipper Data Store<br>

on monthly basis. The functionality of those are:<br><br>
1) Crystal Reports<br>
Crystal Reports is the an outdated online platform that users may download the aggregated numbers from. MTC outsourced the work to Transsight to download the numbers need for reporting and put the numbers into Excel spreadsheet, then send it to MTC EPS staffs on a monthly basis. The process and data selection are set up about 10-20 years before 2019, no one understand why and how the reporting process and system are set up in this way. However, the numbers produced in Crystal Report is the official record to use for reporting purpose, confirmed by Ed Meng.<br>
The contact person of each stakeholder:<br>
MTC: Lysa Hale, Mike Lee, Ed Meng<br>
Transsight: Gopi Purohit<br>
Cubic: Jeffrey Wei<br>
2) Clipper Data Store<br>
The operational data is sent to Clipper Data Store in monthly basis, but updated data made from Cubic would not be updated in Clipper Data Store; at the same time, there are transaction data entries are missing in Clipper Data Store, such as credit card transactions, because it was set up in this way previously between MTC and Cubic while no one in MTC now knows why it was set up in this way.<br>

The Clipper data sent to MTC has two purpose:<br>
1) Reporting Purpose<br>
Cubic is responsible to upload the accurate data onto Crystal Report and provide the data to EPS staffs for reporting to board members. Gopi from Transsight would download the data in reporting format in PDF and Excel files and upload to EPS' Box account, thus Lysa could able to utilize the data on Excel files for reporting to Board members. "1_Operations Report Data_12172018_charts (version 1).xls" is the Excel files that Lysa is relying on for her reports that provides that detail level of data, such as ridership per operator,  before aggregated to "Tabulation" tab which is the tab displaying the aggregated numbers Lysa need for reporting. However, Quinn and Jacques have spent approximately 4 practicum work days tried to tie the numbers between SQL query from Clipper Data Store and the numbers on such Excel file and were not able to get an identical numbers in between. In the meeting with Mike Lee and Ed Meng, Ed Meng mentioned that the data in Clipper Data Store is not accurate and MTC will stick with Crystal Report numbers for reporting purpose.
<br><br>
2) Analytics Purpose
The Clipper Data Store data is meant for analytics purpose because the Clipper Data Store data is no the same as the raw data in Crystal Reports. There are two major reasons to that:<br>
i) Cubic did not transfer the full data set in sfoAddVauleTransactions and sfoToTAddValueTransactions tables: The credit card transactions are missing, but there is no clear reason why Cubic not providing these transactions. <br>
ii) Cubic do not update the data set in Clipper Data Store. If there is changes to the data (One Possible reason due to operator sent the data late) after Cubic send the data to Clipper Data Store, no change will be made.<br><br>

Also note that, Caltrain does not require monthly pass travelers to tag Clipper every trip. The ridership numbers reported to board member or analytics rely on a formula to adjust from the ridership provided  by Crystal Reports. 

## Goal

The goal of this task includes:<br>
1) Transfer the existing data from Clipper Data Store (2013-2018) to Data Lake<br>
2) Set up a procedure to have Cubic provide monthly raw data directly to Data Lake and build a pipeline to transform the data into data warehouse<br>
3) Design and Construct schema and table structure to improve performance for dashboard<br>

## Transferring existing data
The data from Clipper Data Store between 2013 and 2018 was the first batch of data to be imported into Redshift. The process was using Trifacta as ETL tool to transfer the data. However, Trifacta by default is only able to handle up to 150 GB table. The data between 2013 and 2018 contains about 1.8 billion rows that Trifacta was overflowed and not able to handle the transfer. If the data size is consistently large, it is advised to upgrade the memory size of Trifacta or switch to Matillion. However, since it is only an one time operation, we do not need to have larger node in Trifacta for the regular operation unless the transfer transaction is handling more than 150 GB data.

## Preprocessing
Two proposed strategies to improve data lake performance for dashboard is to create views on data warehouse and create a star-schema structure database. Understanding the columns structures are required for both of the strategies.<br>
Prior to implementing the data lake project, Lysa has one monthly report, Clipper Update, which obtain the data from Crystal Reports. The report includes:<br>
* Average Weekday Ridership
* Fee-Generating Transactions
* Unique Cards Used
* Active Card Accounts
* Settled Transit Operator Revenue
* Customer Service Representative calls
* Website Traffic: Unique Visitors and Website Visits
<br><br>

The First task of preprocessing is to figure out which columns are useful for dashboard to replace Crystal Reports or frequently query in order to improve performance. Lysa has provided a spreadsheet, 1_Operations Reports Data_12172018_charts (version 1), which the name is the same every month. 
<br><br>
For each number reported on Lysa's Clipper Update, it queries in the following way:<br>

1. Average Weekday Ridership<br>
The average ridership per day for a given month including only days between Monday - Friday.  Ridership during the week is quite different than weekend ridership.
<br><br>

2. Fee-Generating Transactions<br>
The count of clipper transaction which generating revenue, ie, the count of rides that riders pay a fare to operator. For Bart or Caltrain, although a rider may tag twice for enter and exit, we only count once; similar to Golden State Ferry, only counting the tag when entering.
<br><br>

In this case, the query filter where transaction is subtype is 1, 2, 4. And the example query in Oct, 2018 is the follow:<br>
select count(\*)<br>
from sfofaretransaction<br>
where (subtype = 1 or subtype = 2 or subtype = 4) and<br>
extract(month from convert_timezone('UTC','PST', generationtime)) = 10 and <br>
extract(year from generationtime) = 2018<br>
; 
<br><br>

3. Unique Cards Used<br>
The count of distinct cards used in a given month. The example query in Oct, 2018 is the follow:<br>
select count(distinct applicationserialnumber)<br>
from sfofaretransaction<br>
where<br>
    extract(month from generationtime) = 10 and<br>
    extract(year from generationtime) = 2018 and<br>
    applicationserialnumber < 2000000000<br>
; <br>
4. Settled Transit Operator Revenue<br>
We do not have a precise query to tie the number as the Clipper Update. The best query for Oct, 2018 is the follow:<br>
select sum(purseamount) + sum(GenericECashPurseAmount)/100.00<br>
from sfofaretransaction<br>
where extract(month from generationtime) = 10 and <br>
      extract(year from generationtime) = 2018 and<br>
      applicationserialnumber < 2000000000<br>
;<br>

Where the query result is about $54M whereas the Clipper Update has $59M. The error potentially come from the fact the query did not capture the monthly pass revenue from addvaluetransaction.
<br><br>

5. Others<br>
* Generation time (generationtime) is in UTC, convert time zone to PST is necessary.
* Clipper serial number (applicationserialnumber) greater than 2,000,000,000 are not counted toward the report as they are single-ride ticket
<br>

Sara Barz's Intern Yeeling Tse documented her knowleadge of the Clipper Data Store during her intership.  Mike Lee is the main contact person if there are more questions on both domain knowledge on Clipper and the data store.  Sarah Dogget who recently joined the EPS team is also a good resource.

## Pipeline
In the short run, the ideal situation Cubic would continue to supply SQL structured data to Clipper Data Store and we would have a pipeline to obtain the data monthly transfer to the Data Lake. For the first stage of this task, we use Matillion to ETL from Clipper Data Store to Data Lake on monthly basis. In the long run, the plan is to have Cubic upload the XML files to the S3 bucket and ETL to Data Lake. 


## Schema and Table structures
The Schema and Table structure are the same as Clipper Data Store initially, please refer to the data stationary provided by Cubic. However, the structure will be re-modified to improve performance.


## Principle of Using Clipper Data

The EPS team leadership decided to use the data from Crystal Reports for official reports, the data in Clipper Data Store could only be used by analytics only.<br>
The outsourced process, showed on Figure 1, could not be changed in the short run because MTC has contract with the outsourced party that we could not obtain the data directly from Cubic for reporting. 
<br>
The planned work flow for Clipper Data in the Long Run
![Screenshot](image/fig7.jpeg)
Figure 7
