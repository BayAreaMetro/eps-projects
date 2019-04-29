############ REQUIREMENTS ####################
# pip install psycopg2
# pip install os
# pip install sys
# pip install datetime
##############################################

import psycopg2
import os
import sys
import datetime

# arguments from command line
# $ python connect_lake.py arg1 arg2 arg3 arg4 arg5 arg6
# $ python connect_lake.py <year> <month> <db_user> <db_password> <aws_access_key_id> <aws_secret_access_key>

year = sys.argv[1]
month = sys.argv[2]
user = sys.argv[3]
password = sys.argv[4]
aws_access_key_id = sys.argv[5]
aws_secret_access_key = sys.argv[6]

# Connect to database

start_time = "'" + str(datetime.datetime.now()) + "'"

conn = psycopg2.connect("dbname='lake' \
host='data-viz-cluster.cepkffrgvgkl.us-west-2.redshift.amazonaws.com' \
port=5439 \
user={} \
password='{}'".format(user, password))

cur = conn.cursor()

# Counts before appending table

cur.execute("""SELECT count(*) from clipper.sfofaretransaction;""")

count_clipper_lake = cur.fetchall()
count_clipper_lake = count_clipper_lake[0][0]

print("lake.clipper.sfofaretransaction count ", count_clipper_lake)  # number

# Create temporary table of new data from this month

cur.execute("""CREATE TABLE clipper.sfofaretransaction{}{} AS
               SELECT * from clipper.sfofaretransaction
               where extract(year from generationtime) = {}
               and extract(month from generationtime) = {}"""\
               .format(year, month, year, month))

conn.commit()
print("created table clipper.sfofaretransaction{}{}".format(year, month))

# Row count of month's data

cur.execute("""SELECT count(*) from clipper.sfofaretransaction{}{}""".format(year, month))
count_one_month = cur.fetchall()
count_one_month = count_one_month[0][0]

print("{} {} rows {}".format(year, month, count_one_month))

# Unload to s3 bucket
# https://stackoverflow.com/questions/20323919/how-to-unload-a-table-on-redshift-to-a-single-csv-file

unload_sql="""unload ('select * from clipper.sfofaretransaction{}{}')
    to 's3://mtc-redshift-upload/sfofaretransaction{}{}'
    credentials
    'aws_access_key_id={};aws_secret_access_key={}'
    parallel off
    gzip;
    """.format(year, month, year, month, aws_access_key_id, aws_secret_access_key)
cur.execute(unload_sql)
conn.commit()
print("unloaded table clipper.sfofaretransaction{}{} to s3".format(year, month))

# Upload to Stagging database

conn_stagging = psycopg2.connect("dbname='staging' \
host='data-viz-cluster.cepkffrgvgkl.us-west-2.redshift.amazonaws.com' \
port=5439 \
user='{}' \
password='{}'".format(user, password))  # stagging for testing

cur_stagging = conn_stagging.cursor()


cur_stagging.execute("""SELECT count(*) from clipper.sfofaretransaction;""")

count_clipper_before = cur_stagging.fetchall()
count_clipper_before = count_clipper_before[0][0]

create_table_sql = """create table clipper.sfofaretransaction{}{}
                    (like clipper."sfofaretransaction");""".format(year, month)
cur_stagging.execute(create_table_sql)
conn_stagging.commit()

upload_sql = """copy clipper.sfofaretransaction{}{}
            from 's3://mtc-redshift-upload/sfofaretransaction{}{}'
                credentials
                'aws_access_key_id={};aws_secret_access_key={}'
                gzip;""".format(year,
                month, year, month, aws_access_key_id, aws_secret_access_key)

print(upload_sql)

cur_stagging.execute(upload_sql)
conn_stagging.commit()

# Alter table append to add data to sfofaretransaction

cur_stagging.execute("""insert into clipper.sfofaretransaction
                      (select * from clipper.sfofaretransaction{}{})""".format(year, month))
conn_stagging.commit()

# Drop new monthly table

cur_stagging.execute("""drop table clipper.sfofaretransaction{}{}""".format(year, month))
conn_stagging.commit()

cur.execute("""drop table clipper.sfofaretransaction{}{}""".format(year, month))
conn.commit()

print("dropped table clipper.sfofaretransaction{}{} from lake and stagging".format(year, month))

# Append transcation data to data log table

cur_stagging.execute("""SELECT count(*) from clipper.sfofaretransaction;""")
count_clipper_after = cur_stagging.fetchall()
count_clipper_after = count_clipper_after[0][0]

cur.execute("""SELECT count(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sfofaretransaction'""")
num_cols = cur.fetchall()
num_cols = num_cols[0][0]

desciption = "Uploaded columns from month: {} year: {}".format(year, month)

desciption = "'TEST " + desciption + "'"# for testing purposes

db_name = "'lake'"

end_time =  "'" + str(datetime.datetime.now()) + "'"

platform = "'python script'"

schema_name = "'clipper'"

table = "'sfofaretransaction'"

source = "'lake.clipper.sfofaretransaction'"  # for testing purposes

"""
aftertablenumrows (int4)
appendnumrows (int4)
dbname (varchar)
desciption (varchar)
enddate (date)
jobnumber (int4)
numcols (int4)
platform (varchar)
priortablenumrows (int4)
schemaname (varchar)
source (varchar)
startdate (date)
tableappended (varchar)
"""


insert_command = """INSERT INTO admin.data_log (aftertablenumrows,
                    appendnumrows,
                    dbname,
                    desciption,
                    enddate,
                    numcols,
                    platform,
                    priortablenumrows,
                    schemaname,
                    source,
                    startdate,
                    tableappended)
                    VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})
                    """.format(count_clipper_after, count_one_month,
                    db_name, desciption, end_time, num_cols, platform,
                    count_clipper_before, schema_name, source,
                    start_time, table)
print(insert_command)
cur.execute(insert_command)
conn.commit()
print("appened lake admin.data_logs for load of clipper.sfofaretransaction{}{} data".format(year, month))

conn.close()
