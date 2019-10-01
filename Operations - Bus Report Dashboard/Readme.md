-- Draft --

# Bus Report Dashboard

Define the Problem Statement

### Project Resources

https://10ay.online.tableau.com/#/site/metropolitantransportationcommission/views/BusReportDashboard/KPIs?:iid=2

Add links to:

- Activity, Project, or Task on Asana
- Box directory where any related work products are stored (if applicable)
- ArcGIS Online Working Group (if applicable)
- Any other location where important related work products are stored/saved

## Data Sources

Daily CSV obtained from Cubic SFTP server



### Bus Report Data Dictionary

| Field Name                    | Data Type | Description                                                  |
| ----------------------------- | --------- | ------------------------------------------------------------ |
| RUN_DATE                      | Date      | Report execution date                                        |
| CD_REFERENCE_DATE             | Date      | Date entered by user - report will look for the version of CD downloaded on this date to confirm if the devices are using it. |
| SOURCE_PARTICIPANT_ID         | Int       | Clipper unique Operator ID                                   |
| CID_FLEET_VOLUME              |           | Total number of CID devices that have been connected to a bus belonging to this participant sometime in the past 90 days |
| DC_FLEET_VOLUME               |           | Total number of DC devices that have been connected to a bus belonging to this participant sometime in the past 90 days |
| VEHICLE_FLEET_VOLUME          |           | Total number of distinct bus vehicle IDs reported by DC devices belonging to this participant in the past 90 days |
| SHORT_VEHICLE_ID              |           | Vehicle unique ID                                            |
| CID_DEVICE_ID                 |           | CID decimal number                                           |
| DC_DEVICE_ID                  |           | DC decimal number                                            |
| CID_DEVICE_ID_HEX             |           | CID hexadecimal ID (ESN)                                     |
| DC_DEVICE_ID_HEX              |           | DC hexadecimal ID (ESN)                                      |
| LATEST_UD_TIMESTAMP           |           | Latest UD received date; from the bus device                 |
| DAYS_SINCE_LAST_CONN          |           | Number of days between the RUN DATE of the report and the LAST_CONNECTION_DATETIME. |
| DAYS_SINCE_LAST_COMPLETE_EXCH |           |                                                              |
| LAST_CONNECTED_YARD           |           |                                                              |
| UNFILTERED_CONNECTED_YARD     |           |                                                              |
| WITH_CORRECT_CD               |           |                                                              |
| WITH_CORRECT_APP              |           |                                                              |
| UD_RECEIVED                   |           |                                                              |
| UD_RECEIVED_24HRS             |           |                                                              |
| UD_RECEIVED_1_5DAYS           |           |                                                              |
| UD_RECEIVED_5_10DAYS          |           |                                                              |
| UD_RECEIVED_10DAYS_PLUS       |           |                                                              |
| LAST_COMPLETE_EXCHANGE        |           |                                                              |
| HAS_HOTLIST                   |           |                                                              |
| HAS_ACTIONLIST                |           |                                                              |
| CONNECTION_PROBLEMS           |           |                                                              |
| TRIGGERED_MISSING_UD          |           |                                                              |
| CID_DEVICE_TYPE               |           |                                                              |
| PARTICIPANT                   |           |                                                              |
| LAST_CONNECTION_DATETIME      |           |                                                              |
| CD_VERSION_DISTRIBUTED        |           |                                                              |
| CD_DISTRIBUTION_DATE          |           |                                                              |
| APP_VERSION_DISTRIBUTED       |           |                                                              |
| APP_DISTRIBUTION_DATE         |           |                                                              |



## Automation Code

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



## Tags

#operations #tableau #bus_report