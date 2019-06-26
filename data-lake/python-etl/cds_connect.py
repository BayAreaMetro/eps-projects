############ REQUIREMENTS ####################
# brew install freetds
# pip pip install pymssql
# pip install sys
##############################################

# https://stackoverflow.com/questions/39149243/how-do-i-connect-to-a-sql-server-database-with-python

import sys
import pymssql

# $ python <database> <user> <password>
server = '54.241.21.8'
database = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]

conn = pymssql.connect(server=server, user=user, password=password, database=database)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM dbo.sfofaretransaction")
row = cursor.fetchone()

conn.close()

print(row)
