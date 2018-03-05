# FasTrak-Clipper Merge

The purpose of this project is to merge Clipper and FasTrak account datasets. By identifying users who use both Clipper and FasTrak, MTC can provide better customer service by understanding this user set and their ridership patterns. 

## Contents 

1. [Anonymization script](https://github.com/BayAreaMetro/usf-practicum/blob/master/fastrak-clipper-merge/anonymization_script.py) - This scripts takes Clipper and FasTrak user account data and anonymizes the PII information (first name, last name, address, phone number, email). The only variables that were not anonymized but included on the cleaned account data are city, state, and zip code. 

    ### Technique
    This script uses a technique called Label Encoding to anonymize the desired columns to numbers. This is a one-way process that transforms unique values for each column to a unique numerical value. For example, the first name of "Bob" will be transformed to the same number every time it appears in the Clipper and FasTrak data. This allows for preservation of unique values to be merged on, while masking their actual value.

    ### Inputs and Outputs
    *Input* - Cleaned FasTrak and Clipper Account data

    * fastrak_.csv
    * clipper_.csv
    
    *Output* - Anonymized FasTrak and Clipper Account data, files to link fake and real Account IDs for Clipper and FasTrak, and file containing anonymized labels for missing values

    * anonym_fastrak.csv
    * anonym_clipper.csv
    * fastrak_account_fakeID.csv
    * clipper_account_fakeID.csv
    * missing.csv  
    
     ### Notes
     
     * This script adds an anonymized Clipper and Fastrak Account ID (called Record_id_c and Record_id_f) since this information is considered PII. The link between the real and fake account ID's is crucial for identifying the users with both FasTrak and Clipper accounts on the transactions data. This link is exported in the files fastrak_account_fakeID.csv and clipper_account_fakeID.csv.


2. [Merge script](https://github.com/BayAreaMetro/usf-practicum/blob/master/fastrak-clipper-merge/merging_anonymized_data.py) - This script merges Clipper and FasTrak anonymized account data in an iterative process, making a series of matches using different subsets of columns. This approach was chosen because it is reliable, only making matches when there is one record in each dataset with the stated match criteria. Additionally, by iterating over different subsets of columns, this method picks up matches that has one column misspelled but otherwise has all records matching. 

    ### Technique
    For each level of merge, the match works as follows:

    1. Specify a subset of columns on which to match Clipper and FasTrak Account data
    2. Subset each dataset by taking only the rows that have unique values for each identified column in this match level.
    3. Match between datasets if all values for the specified columns are equal.
    
     ### Inputs and Outputs
    *Input* - Anonymized FasTrak and Clipper Account data, plus csv file containing anonymized labels for missing values

    * anonym_fastrak.csv
    * anonym_clipper.csv
    * missing.csv  
    
    *Output* - File of matched FasTrak and Clipper Accounts by fake account numbers, Record_id_c and Record_id_f

    * matches.csv
    
    ### Notes
   
   *  This code also does a clean-up on city misspellings by creating a dictionary that matches each unique city in the FasTrak and Clipper data sets to the correct city spelling. It does this by checking word similarly between each city on our data to the population of cities in CA (obtained from outside [data source](https://github.com/grammakov/USA-cities-and-states)) and returns the correctly-spelled city.
   

## Results
The results from the first merge are found [here](https://github.com/BayAreaMetro/usf-practicum/blob/master/fastrak-clipper-merge/Results.md)
   




