## First we are goign to clean the data
# renaming the columns for homogeneity between the two datesets

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import re


print("Loading data...")

fastrak = pd.read_csv("/Users/danaiavg/Desktop/fastrak.csv", encoding = 'utf-8')
clipper = pd.read_csv("/Users/danaiavg/Desktop/clipper.csv", encoding = 'utf-8')


print("Creating the record_id column")

fastrak["Record_id_f"] = np.random.choice(len(fastrak), size=len(fastrak), replace=False)
clipper["Record_id_c"] = np.random.choice(len(clipper), size=len(clipper), replace=False)

if len(fastrak) == len(fastrak["Record_id_f"].unique()):
    print("The Record_id for FasTrak works")
else:
    print("ERROR: The Record_id for FasTrak does not work")

if len(clipper) == len(clipper["Record_id_c"].unique()):
    print("The Record_id for Clipper works")
else:
    print("ERROR: The Record_id for CLipper does not work")

print("Saving the preanonymized data including the record_id")
fastrak.to_csv("~/Desktop/fastrak_.csv", encoding='utf-8')
clipper.to_csv("~/Desktop/clipper_.csv", encoding='utf-8')


print("Renaming columns")

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

print("dropping columns")

fastrak = fastrak.drop([" Account_Type ", " Account_Status ", " Account_Opening_Data ",
                        " Device ", " Device Status ", " Account_Name "," Company_Name ", "same_with_Account_Name?1", "same_with_Account_Name?2",
                        "same_with_Account_Name?3", "last", "new", " Zip_4 "], axis=1)

clipper = clipper.drop(["CARD_TYPE", "STATUS"], axis=1)

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

fastrak["zip_code"] = fastrak["zip_code"].apply(str)
clipper["zip_code"] = clipper["zip_code"].apply(str)

print("Label encoding first name")
fastrak, clipper = process_dfs(fastrak, clipper, "last_name")
print("Label encoding last name")
fastrak, clipper = process_dfs(fastrak, clipper, "first_name")
print("Label encoding zipcode")
fastrak, clipper = process_dfs(fastrak, clipper, "zip_code")

def phone_format(phone_number):
    clean_phone_number = re.sub('[^0-9]+', '', phone_number)
    formatted_phone_number = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_phone_number[:-1])) + clean_phone_number[-1]
    return formatted_phone_number

clipper["phone"] = clipper["phone"].apply(phone_format)
fastrak["phone"] = fastrak["phone"].apply(phone_format)

def phone_change(phone_num):
    if phone_num.startswith("1-"):
        return(phone_num[2:])
    else:
        return(phone_num)

clipper["phone"] = clipper["phone"].apply(phone_change)
fastrak["phone"] = fastrak["phone"].apply(phone_change)

print 'Total Clipper account rows : {}'.format(clipper.shape[0])
print 'Total FasTrak account rows : {}'.format(fastrak.shape[0])
#get unique accounts (there can be multiple cards associated with one account)
clipper_accts = clipper.drop_duplicates(subset = ['CONTACTID'])
print 'Total Clipper unique accounts : {}'.format(clipper_accts.shape[0])
#get unique accounts (there can be multiple cards associated with one account)
fastrak_accts = fastrak.drop_duplicates(subset = ['Account'])
print 'Total FasTrak unique accounts : {}'.format(fastrak_accts.shape[0])


fastrak_accts.to_csv("~/Desktop/anonym_fastrak.csv", encoding='utf-8')
clipper_accts.to_csv("~/Desktop/anonym_clipper.csv", encoding='utf-8')



