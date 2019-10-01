# Clipper Update Automation Project Overview

by Sarah Doggett (updated 10/1/2019)

[TOC]

## Problem Statement

The Clipper Card Monthly Report consists of operations data that allows the Clipper team to analyze trends and complete the monthly Clipper Update. Most of the charts and graphs in the Clipper update are based on the data contained in the Monthly Report. 

Before July 2019, the creation of this Monthly Report was an entirely manual process.  A consultant would collect data from a variety of sources (Crystal Reports, Google Analytics, emails from operators, etc.) and manually complied into a complex spreadsheet. There were several problems with this process:

- Because the spreadsheets were created manually, data entry errors were very likely.
- The process was very labor intensive.
- It was often unclear where the source of the data in the spreadsheet was. The documentation of the process was lacking and what existed was outdated.
- Much of the spreadsheet was no longer used for analysis or reporting purposes; however, this data was still being updated - which was a waste of resources.

For these reasons, I was tasked with creating an automated process for updating the spreadsheet. 

## The New Automated Process

Using Windows Task Scheduler, the code is executed automatically on my computer on the 8th of each month. It opens a computer controlled browser and signs into Crystal using my login information, then starts downloading the necessary files for the report on the previous month's clipper operations data. This is the longest running  part of the process. It may take up to 3 days to finish downloading all of the files. Once the files are downloaded, the rest of the code takes about 4 minutes to execute. Files are saved to their designated spots within the automation folder (see the next section). Data is gathered from other sources, including the NTD, Google Analytics, and manual data spreadsheets). Everything is complied and organized into the Monthly Spreadsheet, which contains charts and tables that can be used for the Clipper Update. When the spreadsheet is done, an email is sent to me to notify me that it is ready. If a error was detected during the codes execution, this email will contain the Warning level of the most recent log. 

## Organization of Clipper Monthly Report Automation Folder

The Clipper Monthly Report Automation folder can be found at https://mtcdrive.box.com/s/0bxcd2sv2sg3lk3uj2ev98ujt3yy2z37.

This folder contains all of the files needed to make the automation process work. They are organized into the following subfolders: 

- __Automation Code__ - This folder contains all of the  Python code needed for the automated process. *If anything in this folder is moved, deleted, or renamed, it may break the process.*
- __Log__ - This folder contains all of the log files generated when the code is run. Each time the code is run, 3 log files are created, each with different levels of detail from debugging to warning. If the warning log is not empty, there may be a problem with the code's execution and it needs to be checked.
- __Monthly Spreadsheets__ - This folder contains the final product of the code, the monthly spreadsheet. A new monthly spreadsheet is created each month, based on the spreadsheet from the previous months. *If anything in this folder is moved, deleted, or renamed, it may break the process.*
- __Emailed Reports__ - This folder contains copies of all of the reports that are emailed to me, instead of being obtained from Crystal. Currently, this includes the BART Monthly Ticket Type spreadsheet, the card counts spreadsheet, and the TLP012 combined report. *If anything in this folder is moved, deleted, or renamed, it may break the process.*
- __Manual Data Entry Spreadsheets__ - This folder contains spreadsheets where the data received from operator email can be entered and detected by the code. *If anything in this folder is moved, deleted, or renamed, it may break the process.*
- __Year Folders (2016,...,2019,etc)__ - These folders contain the raw data behind the Monthly Spreadsheet. Within each year, there are subfolders created for each month. Within those, there is a folder (Emails) that contains the relevant emailed reports for that month. There is also a Crystal Reports folder which is organized into subfolders by report type. *If anything in these folders is moved, deleted, or renamed, it may break the process.*

**In general, please make copies of the files instead of changing the original files!**

## Problems with the new process

__Higher Ridership than Before__

The ridership numbers obtained by the automated process are higher than those that were obtained by the manual process. I believe this is due to the consultant and I running the TLR reports at different times. The consultant ran the TLR reports every week, whereas I run them all at once. This means that my TLR reports tend to have higher ridership numbers than the ones that the consultant used, because ridership numbers can increase up until 21 days have passed. For this reason, when we switch from using the consultant's reports to my reports, there will probably be a jump in average weekday ridership that will cause the percent change from the previous month’s ridership to be abnormally large (around 4% instead of .4%). This may be misleading, so a footnote or something should probably explain the change.

__Holidays Cause Errors__

On holidays, several of the smaller operators do not provide any service. Currently this seems to be the case with the Napa Solano group, Sonoma, and Union City. However, it is unclear which holidays each operator takes off. 

When an operator has no ridership for a particular day, it is dropped from the TLR003 and TLR005 reports. This is problematic for my analysis of the TLR005 report because it messes up my code's logic. Unfortunately, when the TLR005 is exported into excel from Crystal, it lacks any indication of what operator each route is associated with. The routes themselves cannot be used to identify the operator because some numbers are used by more than one operator. However, the data is generally in alphabetical order by operator. Therefore, I identify the operator associated with a route by starting with AC Transit and moving through the list each time I detect a total row.

This works for most days, even Sundays, as all operators have at least one route running each day. But on holidays, when some operators do not operate, they are missing from the TLR005 but not from my list of operators. This causes the operators to be identified with incorrect routes. 

There are three possible solutions to this problem:

1. Manually check and enter the ridership for all holidays.
2. Get cubic to change the excel format of Crystal output to be more consistent, with no missing operators, or to included a column that identifies the operator of each route.
3. Determine if the operators that do not run on holidays are consistent with this policy. Create a new list of operators for each holiday and use this instead of the normal list when cleaning the TLR005 report.

__Dependent on my Computer__

Currently, the automated process is dependent on my computer being on the entire time the code is running. This may not be sustainable.



## Code Explanation

### Custom Modules

__*Automate_Crystal*__

```python
'''Automate_Crystal - This module contains functions that allow the downloading of Crystal Reports to be automated. 

## Functions

enable_download_in_headless_chrome(driver, download_dir)
    enables headless mode - I have not been able to get this to work yet

open_chrome(driver_path,output_location,headless=False)
    opens a remote controlled chrome browser

crystal_logon(usr,passwd,driver):
    Log on to Crystal Enterprise.

downloads_done(output_location):
    Determine if chrome has finished downloading the file. 

is_date_Mon_DD_YEAR(date):
    Check if date is in the correct format. I don't think I use this function.
    
is_date_Mon_YEAR(date):
    Check if date is in the correct format. I don't think I use this function.

get_TLR003(start_date,stop_date,output_location,driver):
    Download the TLR003 report for the requested time period.
    
get_TLR005(start_date,stop_date,output_location,driver):
    Download the TLR005 report for the requested time period.
    
get_TLF003(month_year,output_location,driver):
    Download the TLF003 report for the requested time period.

get_TLF005(month_year,output_location,driver):
    Download the TLF003 report for the requested time period.

get_TLF008(month_year,output_location,driver):
    Download the TLF003 report for the requested time period.

get_TLC010(output_location,driver):
   Download the TLC010 report (This is a snapshot report, does not have a time period option).

get_TLC060(output_location,driver):
   Download the TLC010 report (This is a snapshot report, does not have a time period option).

get_TLS003(start_date,stop_date,output_location,driver):
    Download the TLS003 report for the requested time period.

get_TLS004(start_date,stop_date,output_location,driver):
    Download the TLS003 report for the requested time period.

get_TLCU04(start_date,stop_date,output_location,driver):
    Download the TLCU04 report for the requested time period.
    '''
```

__*Crystal_Cleanup*__

```python
'''Crystal_Cleanup - This module contains functions that clean and extract data from downloaded Crystal Reports.

Functions
-----------
open_xls_as_xlsx(src_file_path):
    Open an xls file as an xlsx file.
    
clean_TLC010(TLC010):
    Clean the TLC010 report.   

clean_TLC060(TLC060):
    Clean the TLC060 report.

clean_TLCU04(TLCU04):
    Clean the TLC0U4 report.

extract_TLF003(TLF003):
    Gets data from the TLF003 report.

clean_TLF005(TLF005):
    Gets data from the TLF005 report.

extract_TLF008(TLF008):
    Extract the total TRU2 value from TLF008.

extract_TLR003(input_file):
    Get data from TLR003.

clean_TLR005(unclean_file,output_location):
    Clean the TLR005 report.
    
extract_TLR005(input_TLR005):
    Get data from the cleaned TLR005.
    
clean_TLS003(unclean_file):
    Get data from the cleaned TLS003.    

clean_TLS004(unclean_file,output_location):
    Get data from the TLS004 report.

extract_TLS004_summary(cleanTLS004):
    Get summary data from the TLS004 report.
   
'''
```

__*Google_Analytics*__

```python
"""Hello Analytics Reporting API V4.
Obtained from: https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py

Functions
---------
initialize_analyticsreporting(CLIENT_SECRETS_PATH):
  Initializes the analyticsreporting service object.

get_report(analytics, VIEW_ID,start_date,end_date,metrics):
  Use the Analytics Service Object to query the Analytics Reporting API V4.

print_response(response):
  Parses and prints the Analytics Reporting API V4 response.
  
parse_response(response):
  Parses and stores the Analytics Reporting API V4 response in a dataframe.
  
"""
```

__*Spreadsheet_Automation*__

```python
'''Spreadsheet_Automation - This module calls functions from Automate_Crystal, Crystal_Cleanup, and Google_Analytics along with 
functions from non-custom modules in order to automate the process of downloading data from Crystal and putting the data in the 
Monthly Spreadsheet.

Functions
---------
init_logger(logger_name, output_dir,):
    Given a logger_name and output_dir, sets the logging level to
    level and initializes logger to log to output_dir/<logger_name>.log
    and the console. I do not currently use this function.

identify_holidays(date_string,year):
    Identify if a date is a holiday.
    
allowed_to_run():
    Determine if a report can be run on Crystal.
    
find_first_empty_cell(start_row,column,ws):
    Find the first empty cell in the specified column.    
    
all_Fridays_in_Month(month,year):
    Get a list of all the fridays in a month.
    
get_BART_manual_data(datetime_to_find,manual_BART_path):
    Get BART manual data.

get_GGT_manual_data(datetime_to_find,manual_GGT_path):
    Get GGT manual data.
    
get_SFMTA_manual_data(datetime_to_find,manual_SFMTA_path):
    Get SFMTA manual data.

get_Vacaville_manual_data(datetime_to_find,manual_Vacaville_path):
    Get Vacaville manual data.

get_UC_manual_data(datetime_to_find,manual_UC_path):
    Get UC manual data.

update_clipper_monthly_spreadsheet(month,year,myusername,mypassword,directory,
	box_email_folder,CLIENT_SECRETS_PATH,driver_path,do_headless,spreadsheet_folder):
    
    This is the main function which coordinates the automation process. It is very long.
    
'''
```

__*Scheduled_Spreadsheet_Automation*__

This code will execute the update_clipper_monthly_spreadsheet function from Spreadsheet Automation whenever it is run.
The report will be run for the month previous to the current month. 

This file is where changes to inputs, such as username/password, and the directory path should be made.

This is where the logs are set up.

Windows Task Scheduler will run this code on the 5th of every month.

## Windows Task Scheduler

https://datatofish.com/python-script-windows-scheduler/



### Settings

- General:
  - Run whether user is logged on or not
    - NOTE: This causes the entire program to run in the __*background*__.
  - Run with highest privileges.
- Triggers:
  - Monthly at 8:15 AM on day 5 of January, February, March, April, etc...
- Actions:
  - Start a Program - scheduled automation bat file
- Conditions:
  - Uncheck "Start the task only if the computer is idle"
  - Uncheck "Start the task only if the computer is on AC power"
  - Check "Wake the computer to run this task"
- Settings:
  - Allow task to be run on demand
  - Run task as soon as possible after a scheduled start is missed
  - If task fails, restart every 1 minute and attempt to restart up to 3 times
  - Stop if it runs longer than 3 days
  - if the task does not end when requested, force it to stop



## Clipper Data Needed for EPS Dashboard

Fields the interns identified as necessary for dashboard ([source](https://github.com/BayAreaMetro/eps-projects/blob/master/data-lake/documentations/clipperreportetl.md)):

* Clipper_Total_Card_in_Circulation  *(in my code as "circulation")*
* Clipper_Total_Card_Active *(in my code as "total_active")*
* Clipper_Total_Unique_Cards *(in my code as "Clipper_Card_Count")*
* Clipper_Card_AutoLoads -- not used in their dashboard *(in my code as "CardsRegisteredForAutoload")*
* Clipper_Monthly_Saturation -- not used in their dashboard
* Clipper_Total_Transactions *(add "fare_payment" to "addvalue_refunds" to get this)*
* Clipper_Revenue_By_Channel_AutoLoad_AddValue *(get data from "sales_by_distribution_channel" dataframe)*
* Clipper_Revenue_By_Channel_Retailers *(get data from "sales_by_distribution_channel" dataframe)*
* Clipper_Revenue_By_Channel_Ticket_Machines *(get data from "sales_by_distribution_channel" dataframe)*
* Clipper_Revenue_By_Channel_Ticket_Office_Terminal *(get data from "sales_by_distribution_channel" dataframe)*
* Clipper_Total_Revenue *(get data from "cleanTLF003" dataframe)*
* Clipper_Total_Calls *(get data from "entered_calls")*
* Clipper_CSR_Calls_Handled *(get data from "CSR_calls")*
* **Clipper_IVR_Calls_Handled**
* **Clipper_Total_Calls_to_CSC**
* **Clipper_Total_CSC_Calls_to_CSR_Percent**
* **Clipper_Total_CSC_Calls_to_IVR_Percent**