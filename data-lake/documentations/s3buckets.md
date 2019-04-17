# S3 buckets Documentations

## Background
AWS S3 is one of the tools implemented in Data Lake. The process of Data Lake required data stewards to upload flat file(s) periodically to their assigned bucket and have ETL tools automatically ETL to the Data Warehouse. This documentation outlines the plan of this process. The goal is to have an assigned S3 bucket for data stewards to submit the data.

## Persona
Data Stewards: All data owners in MTC and MTC contractors
Data Engineers: Kearey Smith and USF interns, including Jacques Sham, Anastasia Keck

## Tools
Data Lake - AWS S3, AWS Redshift<br>
Language - Python (Potentially)<br>
ETL - Trifacta, Matillion
<br><br>

Trifacta and Matillion will be used in ETL process. At the early stage, there is no restriction on which platform to use in the ETL process. Potentially, Python would be used to handle unstructured data. However, an ETL tool is preferred unless the data structure is ETL tool or platform is not capable to handle. 

## Structure
Each department has two S3 buckets associated with, one is for data stewards to upload and one is a staging bucket for quality assurance purpose. We would call the buckets raw buckets and clean dat buckets, respectively. The buckets associated with the departments are the following:
<br>

Integrated Planning Department<br>
Raw Bucket: irpp-upload<br>
Clean Data Bucket:  irpp-clean<br>


Programming and Allocations<br>
Raw Data Bucket: pa-mtc-upload  (pa-upload already in use)<br>
Clean Data Bucket:  pa-mtc-clean<br>


Legislation and Public Affairs<br>
Raw Bucket:  lpa-upload  (lower case L)<br>
Clean Data Bucket:  lpa-clean<br>


Design and Project Delivery<br>
Raw Bucket: dpd-upload<br>
Clean Data Bucket:  dpd-clean<br>


Electronic Payments<br>
Raw Bucket: eps-upload<br>
Clean Data Bucket:  eps-clean<br>


Field Operations and Asset Management<br>
Raw Bucket:  foam-upload<br>
Clean Data Bucket: foam-clean<br> 

<br>
Data Stewards are only having access to their assigned raw bucket. However, data stewards across the same department would share the same login and bucket.
<br>

The clean data bucket are set up for staging purpose. Once data stewards has uploaded their data set in the raw bucket, the ETL tool(s) would ETL the transformed data and temporary save in the clean data bucket. Data Engineers are responsible to provide a report for data stewards to approve for quality assurance. Once the data set is approved by data stewards, the transformed data will be transferred to AWS Redshift. 


## Format
The pipeline access csv, excel, xml, json, text for tabular data. Other format may also be accepted but data engineers are responsible to build pipeline for unstructured data. csv is always the best format preferred to be uploaded.


## Access for Data Stewards
Each data stewards are provided with AWS Access Key and AWS Secret Key to the upload S3 bucket assigned for their department. We recommend data stewards to install "My S3 Browser" on Google Chrome browser to access their S3 buckets. However, "My S3 Browser" is only available on Google Chrome and we have not found any useful plugin is as reliable as "My S3 Browser" in FireFox or Safari. "My S3 Browser" upload procedures can be found in "s3_Data_Uploading_SetUp_foam.pdf" and the logins can be found in "AWS Accounts for Data Lake". 


## S3 buckets Permission
S3 upload buckets - Data Stewards, Data Engineers, Trifacta, Matillion<br>
S3 clean data buckets - Data Engineers, Tricata, Matillion
<br>

The S3 upload buckets access permission is granted to data stewards to push, write, and download data, as well as to data engineers, Trifacta and Matillion. Data stewards do not have access to S3 clean data buckets, only data engineers, Trifacta, Matillion are allowed to access to push, write, and download data.
<br>

To access S3 buckets on Trifacta, Trifacta requires data engineers to notify Trifacta to configure the newly set up S3 bucket(s) on Trifacta by sending an email to customer representative of Trifacta. After having Trifacta configured the platform on its side, data engineers are required to assign permission to Trifacta to read the newly set up S3 bucket(s).  To assign permission, go to the "My Security Credential " -> "User" -> Click on the policy which handles S3 buckets access. In the json file for policy, add the S3 url to the "Resource" array. The following is the example of Trifacta's access policy.
<br><br>
{<br>
    "Version": "2012-10-17",<br>
    "Statement": [<br>
        {<br>
            "Sid": "Stmt1473804744000",<br>
            "Effect": "Allow",<br>
            "Action": [<br>
                "s3:Get\*",<br>
                "s3:List\*",<br>
                "s3:Put\*",<br>
                "s3:DeleteObject"<br>
            ],<br>
            "Resource": [<br>
                "arn:aws:s3:::dataviz-trifacta/\*",<br>
                "arn:aws:s3:::dataviz-trifacta",<br>
                "arn:aws:s3:::irpp-upload/\*",<br>
                "arn:aws:s3:::irpp-upload",<br>
                "arn:aws:s3:::irpp-clean/\*",<br>
                "arn:aws:s3:::irpp-clean",<br>
                "arn:aws:s3:::ipa-mtc-upload/\*",<br>
                "arn:aws:s3:::ipa-mtc-upload",<br>
                "arn:aws:s3:::ipa-mtc-clean/\*",<br>
                "arn:aws:s3:::ipa-mtc-clean",<br>
                "arn:aws:s3:::dpd-upload/\*",<br>
                "arn:aws:s3:::dpd-upload",<br>
                "arn:aws:s3:::dpd-clean/\*",<br>
                "arn:aws:s3:::dpd-clean",<br>
                "arn:aws:s3:::eps-upload/\*",<br>
                "arn:aws:s3:::eps-upload",<br>
                "arn:aws:s3:::eps-clean/\*",<br>
                "arn:aws:s3:::eps-clean",<br>
                "arn:aws:s3:::foam-upload/\*",<br>
                "arn:aws:s3:::foam-upload",<br>
                "arn:aws:s3:::foam-clean/\*",<br>
                "arn:aws:s3:::foam-clean"<br>
            ]<br>
        }<br>
    ]<br>
}<br>
<br>
When add S3 buckets, be sure to include '/\*' end of the directory to allow Trifacta to access all folders within this S3 buckets.
<br>
The permission should be set in user's policy, not individual S3 bucket policy to keep all permission in one place. It is recommended to only include the S3 buckets that the ETL tools to access to, ie, if Matillion is not set up to ETL from foam, that Matillion should not be granted access to any buckets associated with foam. If ETL is done by Python, data engineers are responsible to make sure they are using MTC AWS credentials to access S3 buckets, not their personal AWS account.
<br>
The flow chart of the whole AWS user and bucket creation process can be found in this flow chart: "AWS_user_bucket.pdf".