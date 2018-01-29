# importing the libraries
import numpy as np
import pandas as pd


# reading the csv file, which is "|" seperated

FasTrak = pd.read_csv('/Users/danaiavg/Downloads/Profile.csv', sep='|', error_bad_lines=False)

#FasTrak.dtypes
#FasTrak.shape
#FasTrak.columns


#Droping all record that have NAs for specific fields

FasTrak_clean_from_NA  = FasTrak.dropna(subset = ['Account ',' First_Name ',' Last_Name ',' City ',' STATE ',' ZIPCODE '], how = "any")


#FasTrak_clean_from_NA.shape
#FasTrak_clean_from_NA.head()
#FasTrak.isnull().sum()
#FasTrak_clean_from_NA.isnull().sum()


#Getting rid of very big values, if excisting

fastrak_1 = FasTrak_clean_from_NA[~(FasTrak_clean_from_NA[" First_Name "].str.len() > 50)]

#fastrak_1.index = fastrak_1[' First_Name '].str.len()
#fastrak_1 = fastrak_1.sort_index(ascending=False).reset_index(drop=True)
#print (fastrak_1)
#FasTrak_clean_from_NA.shape
#fastrak_1.shape
#fastrak_1.head()

fastrak_2 = fastrak_1[~(fastrak_1[" Last_Name "].str.len() > 50)]

#fastrak_2.shape
#fastrak_2.head()

fastrak_3 = fastrak_2[~(fastrak_2[" Account_Name "].str.len() > 100)]

#fastrak_3.shape
#fastrak_3.head()

fastrak_4 = fastrak_3

#fastrak_4.shape

#Exporing whether the Account_Name and Company_Name fields are going to be included in the anaysis

fastrak_4["new"] = fastrak_4[" First_Name "].str.cat(others=[fastrak_4[" Last_Name "]], sep=' ')

#fastrak_4

#Creating extra columns to see the overlap

fastrak_4['same_with_Account_Name?1'] = np.where(fastrak_4['new']==fastrak_4[' Account_Name '], 1, 0)
fastrak_4['same_with_Account_Name?2'] = np.where(fastrak_4['new']==fastrak_4[' Company_Name '], 1, 0)
fastrak_4['same_with_Account_Name?3'] = np.where(fastrak_4[' Account_Name ']==fastrak_4[' Company_Name '], 1, 0)

#fastrak_4.head()
#fastrak_4.shape

fastrak_4['same_with_Account_Name?1'].value_counts()

fastrak_4['same_with_Account_Name?2'].value_counts()

fastrak_4['same_with_Account_Name?3'].value_counts()

fastrak_4['last'] = np.where((fastrak_4['new']==0) & (fastrak_4[' Account_Name ']==0) & (fastrak_4[' Company_Name ']==0), 1, 0)

fastrak_4['last'].value_counts()

fastrak_4[(fastrak_4['same_with_Account_Name?3']==1)&(fastrak_4['same_with_Account_Name?1']==0)&(fastrak_4['same_with_Account_Name?2']==0)]

#Dropping the columns that are not considered useful

fastrak_5 = fastrak_3.drop([" Account_Name "," Company_Name ", "same_with_Account_Name?1", "same_with_Account_Name?2", "same_with_Account_Name?3", "last", "new", ' Zip_4 '], axis = 1)

#fastrak_5.head()

