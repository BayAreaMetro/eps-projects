# FasTrak-Clipper Merge

The purpose of this project is to merge Clipper and FasTrak account datasets. By identifying users who use both Clipper and FasTrak, MTC can provide better customer service by understanding this user set and their ridership patterns. 

## Contents 

1. [Anonymization script](https://github.com/BayAreaMetro/usf-practicum/blob/master/fastrak-clipper-merge/anonymization_script.py) - This scripts takes Clipper and FasTrak user account data and anonymizes the PII information (first name, last name, address, phone number, email). The only variables that were not anonymized but included on the cleaned account data are city, state, and zip code. 

### Technique
This script uses a technique called Label Encoding to anonymize the desired columns to numbers. This is a one-way process that transforms unique values for each column to a unique numerical value. For example, the first name of "Bob" will be transformed to the same number every time it appears in the Clipper and FasTrak data. This allows for preservation of unique values to be merged on, while masking their actual value.

### Input/Output Data
Input - Cleaned FasTrak and Clipper Account data 
	* fastrak_.csv
	* clipper_.csv
Output - Anonymized FasTrak and Clipper Account data and file containing anonymized labels for missing values
	* anonym_fastrak.csv
	* anonym_clipper.csv
	* missing.csv

