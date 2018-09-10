import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import re

# loading the data
print("Loading data...")
fastrak = pd.read_csv("~/Desktop/fastrak_.csv", encoding='utf-8')
clipper = pd.read_csv("~/Desktop/clipper_.csv", encoding='utf-8')

# filling missing values
clipper[["address_1", "address_2", "state", "city" , "phone", "zip", "email"]]= clipper[["address_1", "address_2", "state", "city" , "phone", "zip", "email"]].fillna(value = "missing")
fastrak[["address_1", "address_2", "state", "city" , "zip"]]= fastrak[["address_1", "address_2", "state", "city" , "zip"]].fillna(value = "missing")

# this function takes as an input the 2 data sets and the column that they have in common and returns the anonymized (with label encoding) dataframes
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
    
    missing_encoding = -1
    list_values_c = le.inverse_transform(clipper1[col])
    list_anon_c = clipper1[col]
    if 'missing' in list_values_c:
        missing_encoding = list(list_anon_c)[list(list_values_c).index('missing')]
    
        
    return fastrak1, clipper1, missing_encoding

# Applying the function
print("Anonymizing first name")
fastrak, clipper, missing_encoding_first = process_dfs(fastrak, clipper, "last_name")
print("Anonymizing last name")
fastrak, clipper, missing_encoding_last = process_dfs(fastrak, clipper, "first_name")
print("Anonymizing email")
fastrak, clipper, missing_encoding_email = process_dfs(fastrak, clipper, "email")
print("Anonymizing Address_1")
fastrak, clipper, missing_encoding_address1 = process_dfs(fastrak, clipper, "address_1")
print("Anonymizing Address_2")
fastrak, clipper, missing_encoding_address2 = process_dfs(fastrak, clipper, "address_2")


# crerating a dataframe with all the unique columns (names) to fit the model
names = pd.DataFrame(clipper['phone'].unique(), columns=['phone']).append(pd.DataFrame(fastrak['Day Phone Number'].unique(), columns=['phone']))
names1 = pd.DataFrame(fastrak['Mobile Number'].unique(), columns=['phone']).append(pd.DataFrame(fastrak['Evening Phone'].unique(), columns=['phone']))
names2 = pd.DataFrame(names1['phone'].unique(), columns=['phone']).append(pd.DataFrame(names['phone'].unique(), columns=['phone']))
names3 = pd.DataFrame(names2['phone'].unique(), columns=['phone'])

# fit the model
le=LabelEncoder()
le.fit(names3['phone'].values)

print("Anonymizing phone number")
# transform fastrak and clipper
fastrak['Mobile Number']=le.transform(fastrak['Mobile Number'])
fastrak['Day Phone Number']=le.transform(fastrak['Day Phone Number'])
fastrak['Evening Phone']=le.transform(fastrak['Evening Phone'])
clipper['phone'] = le.transform(clipper['phone'])

list_values = le.inverse_transform(clipper['phone'])
list_anon = clipper['phone']
missing_encoding_phone = list(list_anon)[list(list_values).index('missing')]

print('Anonymization is done')

missings = pd.DataFrame(data ={'first_name': [missing_encoding_first], 
                         'last_name' : [missing_encoding_last], 
                         'email' : [missing_encoding_email], 
                         'address_1' : [missing_encoding_address1],
                         'address_2' : [missing_encoding_address2],
                         'phone' : [missing_encoding_phone],
                        'zip': 'missing',
                        'city': 'missing',
                        'state': 'missing'
                        })

print('Exporting')
fastrak.to_csv("~/Desktop/anonym_fastrak.csv", encoding='utf-8')
clipper.to_csv("~/Desktop/anonym_clipper.csv", encoding='utf-8')
missings.to_csv("~/Desktop/missing.csv", encoding='utf-8')
























