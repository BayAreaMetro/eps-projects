# Bus Report Dashboard

##### by Sarah Doggett

Clipper Operations lacked a way to easily spot and investigate issues related to bus device connectivity and status. Clipper worked with Cubic to develop a Bus Report that would provide detailed insight into the operational status of Clipper devices on the bus system. 

The Tableau dashboard was created to use this data to easily visualize the state of the bus devices and to see trends in performance. 

##### Background on Clipper Devices

DC unit transfers data between central server and CID; Passenger Clipper card journey tags are validated and captured by the CID; during card tags CID can also load the data contained in the Actionlist file pertained to any individual clipper card and if required block the card or products listed in the Hotlist file.

CID periodically sends passenger clipper card tag data (UD) to the DC and the DC will upload the UD to the central server when the bus arrives at the bus yard and establish communication with the yard access point.

### Project Resources



Tableau Online Dashboard:

https://10ay.online.tableau.com/#/site/metropolitantransportationcommission/workbooks/629306?:origin=card_share_link

## Data Source

At 11:30 pm each day, Cubic creates the Bus Report and places it on the SFTP server, as a g-zipped csv folder. Files are named using the convention of YYYYMMDD_BusStatus. The report contains the fields detailed in the Bus Report Data Dictionary table.

### Bus Report Data Dictionary

| Field Name                    | Data Type | Description                                                  |
| ----------------------------- | --------- | ------------------------------------------------------------ |
| RUN_DATE                      | Date      | Report execution date                                        |
| CD_REFERENCE_DATE             | Date      | Date entered by user - report will look for the version of CD downloaded on this date to confirm if the devices are using it. |
| SOURCE_PARTICIPANT_ID         | Int       | Clipper unique Operator ID                                   |
| CID_FLEET_VOLUME              | Int       | Total number of CID devices that have been connected to a bus belonging to this participant sometime in the past 90 days |
| DC_FLEET_VOLUME               | Int       | Total number of DC devices that have been connected to a bus belonging to this participant sometime in the past 90 days |
| VEHICLE_FLEET_VOLUME          | Int       | Total number of distinct bus vehicle IDs reported by DC devices belonging to this participant in the past 90 days |
| SHORT_VEHICLE_ID              | Int       | Vehicle unique ID                                            |
| CID_DEVICE_ID                 | Int       | CID decimal number                                           |
| DC_DEVICE_ID                  | Int       | DC decimal number                                            |
| CID_DEVICE_ID_HEX             | Str       | CID hexadecimal ID (ESN)                                     |
| DC_DEVICE_ID_HEX              | Str       | DC hexadecimal ID (ESN)                                      |
| LATEST_UD_TIMESTAMP           | Date      | Latest UD received date; from the bus device                 |
| DAYS_SINCE_LAST_CONN          | Int       | Number of days between the RUN DATE of the report and the LAST_CONNECTION_DATETIME. |
| DAYS_SINCE_LAST_COMPLETE_EXCH | Int       | Number of days between the RUN DATE of the report and the LAST_COMPLETE EXCHNGE of CD and UD |
| LAST_CONNECTED_YARD           | Str       | The yard name of the TDS that the CID last connected with, as long as the timestamp of this yard name record is not older than the last received UD transaction time stamp (less 2 days) for this CID. |
| UNFILTERED_CONNECTED_YARD     | Str       | The host name of the TDS that the CID last connected with.   |
| WITH_CORRECT_CD               | Y/N       | CID is using a version of CD that is at least as recent as that distributed on the CD_REFERENCE_DATE |
| WITH_CORRECT_APP              | Y/N       | CID is using a version of Application that is at least as recent as that distributed on the CD_REFERENCE_DATE |
| UD_RECEIVED                   | Y/N       | Y if UD has been received from this device since the CD_REFERENCE_DATE |
| UD_RECEIVED_24HRS             | Y/N       | Y if UD has been received in the past 24 hours               |
| UD_RECEIVED_1_5DAYS           | Y/N       | Y if UD has been received in the past 1-5 days               |
| UD_RECEIVED_5_10DAYS          | Y/N       | Y if UD has been received in the past 5-10 days              |
| UD_RECEIVED_10DAYS_PLUS       | Y/N       | Y if UD has been received over 10 days ago                   |
| LAST_COMPLETE_EXCHANGE        | Date      | Date that the device performed its last COMPLETE UD/CD exchange |
| HAS_HOTLIST                   | Y/N       | Y if the device reports that it is using a hotlist           |
| HAS_ACTIONLIST                | Y/N       | Y if the device reports that it is using an ActionList       |
| CONNECTION_PROBLEMS           | Y/N       | Y if the latest UD received from this bus is more than 3 days older than the date the bus last connected to a yard |
| TRIGGERED_MISSING_UD          | Int       | Number of financial transaction UD missing for the device for the past one year, since the day the report was executed/run (only shown if over 20) |
| CID_DEVICE_TYPE               | Str       | Type of CID - The two types of Customer Inter Face Devices are CID1B and CID5.<br/>The CID1B pairs with DC DEVICE ID = “DC”. There could be multiple CID1B devices per DC operator control units.<br/>The CID5 pairs with the DC DEVICE ID = “DC3”. There could be multiple CID5 devices per DC3 operator control units. |
| PARTICIPANT                   | Str       | Operator abbreviation                                        |
| LAST_CONNECTION_DATETIME      | Date      | Last Connected date and time. Note - this could be an initial connection and the bus may not be in the yard long enough to exchange a full set of CD and UD. |
| CD_VERSION_DISTRIBUTED        | Int       | Latest distributed Action and Hotlist version number         |
| CD_DISTRIBUTION_DATE          | Date      | Latest Action/Hot List distributed date - Distributed daily at 10 PM PST |
| APP_VERSION_DISTRIBUTED       | Int       | Latest distributed Application version number                |
| APP_DISTRIBUTION_DATE         | Date      | Latest Application distributed date                          |



## Automation Code

Using Windows Task Scheduler, this code is scheduled to run each morning at 9am. It downloads yesterday's Bus Report from the Cubic SFTP server to a local 'Downloads' folder. It unzips the file and uploads the csv to the S3 folder, so it can be added to the Data Lake. The zipped file remains on the local computer as a backup. 



```python
#!/usr/bin/env python
# coding: utf-8

import sys
sys.dont_write_bytecode = True

import getpass
user = getpass.getuser()

sys.path.insert(0, '/Users/{}/Box/Utility Code'.format(user))
from utils_io import *

import pysftp
from datetime import datetime, timedelta
import gzip
import shutil
import logging

def download_bus_report(date_to_get,directory):
    
    remote_file_loc = f'SF_SUMM/BUS_STATUS/{date_to_get}_BusStatus.csv.gz'
    local_file_loc = f'{directory}/Downloads/{date_to_get}_BusStatus.csv.gz'
    filename_csv = f'{directory}/Downloads/{date_to_get}_BusStatus.csv'

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load(f'C:\cygwin64\home\{user}\.ssh\known_hosts')
    datastore = ''

    with pysftp.Connection(host=datastore, username ='',cnopts=cnopts,private_key='') as srv:
        log.info('Connection successful')
        srv.get(remote_file_loc,local_file_loc)
        log.info(f'File downloaded to {local_file_loc}')

    with gzip.open(local_file_loc, 'rb') as f_in:
        with open(filename_csv, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
    # copy it to S3
    bucket = 'mtc-redshift-upload'
    key = f'bus_report/{date_to_get}_BusStatus.csv'

    copy_file_to_s3(filename_csv, bucket, key)

    # delete local csv file (keep the gzip file though, for backup)
    os.remove(filename_csv)
            
    
if __name__ == "__main__":

    directory = ''
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')

    log = logging.getLogger()    
    logname = f'SFTP_download_for_{yesterday}'
    debug_fileHandler = logging.FileHandler(directory + "\\Log\\DEBUG_" + logname + ".log")
    warning_fileHandler = logging.FileHandler(directory + "\\Log\\WARNING_" + logname + ".log")
    consoleHandler = logging.StreamHandler(sys.stdout)


    debug_fmt = logging.Formatter("%(asctime)s : %(module)s - %(funcName)s - %(lineno)s \n  \t  %(message)s \n")
    info_fmt = logging.Formatter("%(name)s - %(asctime)s - %(message)s")
    warning_fmt = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")

    debug_fileHandler.setFormatter(debug_fmt)
    warning_fileHandler.setFormatter(warning_fmt)
    consoleHandler.setFormatter(info_fmt)


    debug_fileHandler.setLevel(logging.DEBUG)    
    warning_fileHandler.setLevel(logging.WARNING)
    consoleHandler.setLevel(logging.INFO)
    log.setLevel(logging.INFO)

    log.addHandler(consoleHandler)
    log.addHandler(debug_fileHandler)
    log.addHandler(warning_fileHandler)    
    

    #do this every day at 9 am    
    try:
        download_bus_report(yesterday,directory)
    except Exception:
        log.exception('Unexpected Error in Main function')

    logging.shutdown()
```



## How to get access to Cubic SFTP server

1. Aquire SFTP Client (aka Cygwin OpenSSH)
2. Create RSA key pair by entering this command into Cygwin (ssh-keygen -t rsa)
3. Provide id_rsa.pub file to Cubic
4. Get Cubic to add IP address to their firewall



## Tags

#operations #tableau #bus_report #automation
