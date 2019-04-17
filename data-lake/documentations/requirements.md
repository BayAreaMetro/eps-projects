# MTC Data Lake Requirement Document Draft

Requirements for MTC Data Infrastructure
Prepared by Quinn Keck and Jacques Sham
<br>
This document outlines the major requirements to create a “Data Lake” warehouse infrastructure that will take in raw data from each department in the Metropolitan Transportation Commission (MTC), and upload data to an AWS Redshift Warehouse after quality assurance checks have been completed.  The goal of this project is to centralize the data across the agency to make data accessible at the MTC and foster a data-driven culture.  Data from Redshift will be used in a variety of projects, such as dashboards, to further the work of the MTC.   The following is a list of requirements for this endeavor.  
 
## Personas
 
<b>Data Stewards</b>: Data Stewards will be defined as people in the agency who update and maintain MTC data. They will upload their data and check for quality assurance of the data they uploaded. They have some technical skills: Using Excel and may know SQL Query.
<br> 
<b>Data Engineers</b>:  Anyone working on the data pipeline, dashboard building, or other data projects, such as the Data Visualization team or USF Data Science Interns.  They have high technical skills on programming language(s) and data tools.
<br>
<b>End-Users</b>:  Anyone who will be utilizing dashboards or other data products from the Data Lake. They have limited technical skills and will not be querying data from the Data Lake directly. 
 
 
## Requirements
 
1. Ingestion
<br>
Data Stewards need a reliable way to upload their data that will be put in the Data Lake. Each department at the MTC (Integrated Planning Department, Programming and Allocations, Legislation and Public Affairs, Design and Project Delivery, Field Operations and Asset Management, and Electronic Payments) will have their own S3 bucket and their own login credentials for that bucket to upload data to. Each data set will have their own folder under own department S3 bucket.  The data visualization department and IT services will work with data stewards to set up a reliable uploading method, such as the MY S3 BROWSER extension on chrome or a desktop extension. Every time Data Stewards upload a file to S3 bucket, they will also fill out a survey regards the information about the data set.
<br><br> 

2. Data Set Survey
<br>
Data Stewards will be filling out the data set survey every time they upload a file to S3 bucket. The survey includes questions regards on background on data stewards and data sets for documentation. The survey will be distributed in Microsoft Word or Google Sheet during the early stage.<br>
Survey Draft: (TBA)
<br><br> 

3. Quality Assurance /Quality Control (Should Follow MDM)
 <br>
Data Engineers will determine whether the data set is structured or unstructured that the data set can be ETL to the relationship database directly. They will use various tools to convert unstructured data be structured for relationship database. They are also responsible to assure the files received from Data Stewards are well formatted for ETL to the relationship database.<br>
Data Stewards need a way to assure that the data they uploaded is free from errors (such as dates that are in the future).  They need a summary of the data they uploaded for quality assurance, such as a dashboard.  Data engineers will be providing the summary for Data Stewards. Automatic ways of checking data quality may be implemented in addition. 
 
4. Updates (Data)
<br>
Every time new data is uploaded, the updates to the Data Lake need to run smoothly and in a timely manner. A mechanism for automatically checking the data stewards S3 buckets for new data and making sure any new data uploaded is not a repeat of data already ingested is needed.  A reliable data pipeline is needed for the ingestion of new data.
<br><br> 
 
5. Languages and Tools
<br>
i. AWS<br>
The pipeline and Data Lake will be built on AWS, so fluency in AWS services will be necessary for the data engineers.  Data Stewards and end-users will not need knowledge of AWS.  Primarily we will use S3, which is cloud-based flat file storage in buckets.  We will use AWS Redshift which is a large scale data warehouse. Potentially, data engineers may use AWS Athena to access flat files in S3 and AWS CloudWatch for AWS Redshift monitoring. Data engineers are responsible for the maintenance
<br>
ii. Trifacta<br>
Trifacta is the primary ETL tool will be used to wrangle the data, so anyone involved in Data Lake pipeline engineering will need to knowledgeable of it. Trifacta does not require any coding language to operate.  The alternative tools are AWS Glue or Matillion.
<br>
iii. Matillion<br>
Matillion is the alternative ETL tool to Trifacta, it does not require any code language to operate.
<br>
iii. Postgres<br>
AWS Redshift in the account is set up in Postgres. Data Engineers will use Postgres SQL language to query data from the data warehouse. While the data stewards themselves do not need to be fluent in SQL, it is the requirement for anyone who sets up and maintain the Data Lake or creating using the Data directly from the Data Lake.  End-users who will be only accessing dashboards or reports will not need to be frequent in SQL.
<br>
iv. TeamSQL<br>
TeamSQL is the preferred client software for data engineers to query data.  TeamSQL uses Postgres. Data Engineer will also generate high-level summary to Data Stewards for approval. TeamSQL discontinued on March, 2019.
<br>
v. Python<br>
Python is the programming language be used if ETL tools are not been using. Data Engineers will need a basic familiarity with Python to utilize certain AWS services, like AWS Lambda.  Data stewards and end-users do not need to know Python. Data Engineers may use Jupyter Notebook for the platform.
<br>
vi. My S3 Browser<br>
My S3 Browser is the extension on Google Chrome. Data stewards will need to be able to use My S3 Browser to upload data.  The data visualization department and IT services will work with data stewards to set up this extension or another reliable uploading method, such as a desktop extension. There is no similar extension recommended for Mozilla Firefox or Microsoft Internet Explorer.
<br><br>
6. Concurrency<br>
Many data stewards need to be able to put and data and end-users need to access data from the Data Lake at once.  This project can not be completed by anyone data engineer and needs to last through personnel transitions in the agency.  
<br><br>
7. Backup and Restore
<br>          
If there are failures anywhere along the data pipeline, the data needs to be able to be recovered.  This can be achieved by storing both the data in the original form and in the Data Lake warehouse.  Snapshots of the Redshift database would be saved to another S3 bucket.  When data is upload to redshift, the most recent backup of the database will be noted so that in the event something goes wrong with the upload, the database can be restored to its previous state.  Run logs of the S3 buckets and redshift database will be accessible in a data engineering dashboard.
<br><br> 
8. Maintenance and Monitoring
<br>
Data Engineers will maintain the pipeline, redshift database, dashboards, and other data projects.  They will need AWS accounts with the proper permissions, as well as access to Postgres accounts to query the database.   CloudWatch will be used for monitoring the activities in S3 and Redshift. Trifacta will be providing the logging report for any ETL activities in Trifacta.
<br><br> 
9. Analysis
<br>
Data in the Date Lake needs to be easily accessed, queried, joined, and otherwise available for analysis.  It needs to be able to query for the dashboards and other reporting tools in a timely manner for all people inside the agency who need it.  End-users need to have the permissions they need to access the data relevant to them.   Sense the database will be large, there will be a Business Intelligence Layer that stores the aggregated data in star schemas and OLAP cubes so it can be efficiently accessed in dashboards. The data in the Data Lake is only valuable to the MTC if it can be effectively used for analysis.
<br><br><br><br>

 
## Works Cited
 
https://www.splicemachine.com/7-requirements-operationalize-data-lakes/
https://aws.amazon.com/lake-formation/
https://aws.amazon.com/big-data/datalakes-and-analytics/
https://www.big-data-europe.eu/wp-content/uploads/D3.5-Big_Data_platform_requirements_architecture_and_usage.pdf
https://aws.amazon.com/blogs/big-data/build-a-data-lake-foundation-with-aws-glue-and-amazon-s3/
https://www.itbusinessedge.com/slideshows/data-lakes-8-enterprise-data-management-requirements-11.html