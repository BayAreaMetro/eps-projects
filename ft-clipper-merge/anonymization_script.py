## First we are goign to clean the data
# renaming the columns for homogeneity between the two datesets

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

fastrak = pd.read_csv("/Users/danaiavg/Desktop/fastrak.csv", encoding = 'utf-8')
clipper = pd.read_csv("/Users/danaiavg/Desktop/clipper.csv", encoding = 'utf-8')

fastrak.rename(columns={ ' Last_Name ' : 'last_name',
                        ' First_Name ' : 'first_name',
                         ' STATE ' : 'state',
                         ' City ' : 'city',
                         ' ZIPCODE ' : 'zip_code'}
               , inplace=True)

clipper.rename(columns={ ' Last_Name ' : 'last_name',
                        ' First_Name ' : 'first_name',
                        ' STATE ': 'state',
                        ' City ': 'city',
                        ' ZIPCODE ' : 'zip_code'}
               , inplace=True)

# dropping the columns that are not going to be needed

# fastrak = fastrak.drop([" Account_Type "], axis=1)

fastrak = fastrak.drop([" Account_Type ", " Account_Status ", " Account_Opening_Data ",
                        " Device ", " Device Status ", " Account_Name "," Company_Name ", "same_with_Account_Name?1", "same_with_Account_Name?2",
                        "same_with_Account_Name?3", "last", "new", " Zip_4 "], axis=1)

clipper.drop(['CONTACTID', 'CARD_TYPE', 'STATUS'], axis=1)

# lowercasing: first name, last name, state, city.  

fastrak["last_name"] = fastrak["last_name"].str.lower()
fastrak["first_name"] = fastrak["first_name"].str.lower()
fastrak["state"] = fastrak["state"].str.lower()
fastrak["city"] = fastrak["city"].str.lower()

clipper["last_name"] = clipper["last_name"].str.lower()
clipper["first_name"] = clipper["first_name"].str.lower()
clipper["state"] = clipper["state"].str.lower()
clipper["city"] = clipper["city"].str.lower()

def process_dfs(fastrak1, clipper1, col):
    
    # crerating a dataframe with all the unique columns (names) to fit the model
    names = pd.DataFrame(clipper1[col].unique(), columns=[col]).append(pd.DataFrame(fastrak1[col].unique(), columns=[col]))
    names1 = pd.DataFrame(names[col].unique(), columns=[col])
    
    # fit the model
    le=LabelEncoder()
    le.fit(names1[col].values)
    
    # transform fastrak and clipper
    fastrak1[col]=le.transform(fastrak1[col])
    clipper1[col] = le.transform(clipper1[col])
    return fastrak1, clipper1

fastrak, clipper = process_dfs(fastrak, clipper, "last_name")
fastrak, clipper = process_dfs(fastrak, clipper, "first_name")

fastrak.to_csv("~/Desktop/anonym_fastrak.csv", encoding='utf-8')
clipper.to_csv("~/Desktop/anonym_clipper.csv", encoding='utf-8')



