# FasTrak Exploration

The purpose of this directory is to house all scripts related to FasTrak data cleaning and analysis.

## Contents 

1. [Summary of bridge transactions](https://github.com/BayAreaMetro/usf-practicum/blob/master/fastrak-exploration/README.md) - This scripts takes monthly aggregated bridge transactions reports from July 2015 to June 2017 and cleans data in preparation for analysis. Data cleaning processes include:
	* Aggregating disparate reports
	* Fixing dates
	* Attaching bridge name to bridge ID
	* Cleaning zip codes
	* Label Fiscal Year
	
2. Transaction ETL Script
This script processes and loads transaction data into AWS Data Lake (Redshift DB).
