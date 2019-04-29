# Python ETL

This python script takes one month of data from lake schema on AWS Redshift and moves it to the stagging schema.  



To run the script, input the year (such as 2018) and month (January = 1, February = 2, etc) and the proper credentials.

  `$ python connect_lake.py <year> <month> <db_user> <db_password> <aws_access_key_id> <aws_secret_access_key>`



The script will upload the month's data to the `mtc-redshift-upload` s3 bucket, then copy that into staging. It drops the monthly tables created in the process.  As a backup, it does not drop the gzip file in the s3 bucket.

It will append a the `admin.data_logs table` with : 

* the row count of the clipper table before 

* the row count of the clipper table after

* count of the one month's rows

* database name

* desciption of the load

* start time, end time

* number of columns

* the platform (python)

* schema name

* source

* table name

This can keep data in the stagging schema up to date.


 
