import pandas as pd
import numpy as np

#import anonymized data
fastrak = pd.read_csv("~/Desktop/anonym_fastrak.csv", encoding = 'utf-8')
clipper = pd.read_csv("~/Desktop/anonym_clipper.csv", encoding = 'utf-8')
missings = pd.read_csv("~/Desktop/missing.csv", encoding='utf-8')

dictionary = np.load("/Users/ksmith/Box/USF_Data_Science_Practicum/Analytics/cities_dictionary.npy")

#remove "unnamed" col
fastrak = fastrak.drop(fastrak.columns[0], axis = 1)
clipper = clipper.drop(clipper.columns[0], axis = 1)
missings = missings.drop(missings.columns[0], axis = 1)

clipper[["address_1", "address_2", "state", "city" , "phone", "zip", "email"]]= clipper[["address_1", "address_2", "state", "city" , "phone", "zip", "email"]].fillna(value = "missing")
fastrak[["address_1", "address_2", "state", "city" , "zip"]]= fastrak[["address_1", "address_2", "state", "city" , "zip"]].fillna(value = "missing")

def fix_city(x):
    if x in dictionary.item():
        return(dictionary.item().get(x))
    else:
        return(x)

fastrak['city'] = fastrak['city'].apply(fix_city)
clipper['city'] = clipper['city'].apply(fix_city)

def match(clipperdf, fastrakdf, vars):
    '''
    Get unique records in both dataframes based on the selected fields (vars)
    
    If there is a unique match between the datasets based on those field, return in dataset matches_to_keep
    
    acct_matches returns just the Clipper and Fastrak IDs of the matched accounts
    
    Remove those matches from original dataframes and return as c_remaining and f_remaining
    '''
    
    c_orig = clipperdf.shape[0]
    c_unique_df = clipperdf.drop_duplicates(subset = vars, keep=False)

    clipper_ind = ['(c_unique_df["'+col+'"]!='+str(int(missings[col])) +')' if missings[col].dtype == 'int64' 
                   else '(c_unique_df["'+col+'"]!="missing")' for col in vars]
    clipper_index = " & ".join(clipper_ind)
    c_unique_df = c_unique_df[eval(clipper_index)]
    
#     print c_dropped_missing.shape
    c_new = c_unique_df.shape[0]
    print 'Orginial Clipper: {}, Unique Clipper: {}'.format(c_orig, c_new)
    f_orig = fastrakdf.shape[0]
    f_unique_df = fastrakdf.drop_duplicates(subset = vars, keep=False)
    
    fastrak_ind = ['(f_unique_df["'+col+'"]!='+str(int(missings[col])) +')' if missings[col].dtype == 'int64' 
                   else '(f_unique_df["'+col+'"]!="missing")' for col in vars]
    
    fastrak_index = " & ".join(fastrak_ind)
    f_unique_df = f_unique_df[eval(fastrak_index)]
    
    f_new = f_unique_df.shape[0]
    print 'Orginial Fastrak: {}, Unique Fastrak: {}'.format(f_orig, f_new)
    matches_to_keep = c_unique_df.merge(f_unique_df, how = 'inner', on = vars)
    print 'Unique matches found: {}'.format(matches_to_keep.shape[0])
    acct_matches = matches_to_keep[['Record_id_c', 'Record_id_f']]
    c_remaining = clipperdf[~clipperdf["Record_id_c"].isin(matches_to_keep["Record_id_c"])]
    f_remaining = fastrakdf[~fastrakdf["Record_id_f"].isin(matches_to_keep["Record_id_f"])]
    print 'Clipper remaining: {}'.format(c_remaining.shape[0])
    print 'Fastrak remaining: {}'.format(f_remaining.shape[0])
    
    return acct_matches, matches_to_keep, c_remaining, f_remaining


# Level 1 - First Name, Last Name, Address, city, zip
print('level 1')
acct_matches1, matches_to_keep1, clipper1, fastrak1 = match(clipperdf = clipper, fastrakdf = fastrak, vars = ["first_name", "last_name", "address_1", "zip", "city"])

print('level 2')
# Level 2 - First Name, Last Name, Address, Zip
acct_matches2, matches_to_keep2, clipper2, fastrak2 = match(clipperdf = clipper1, fastrakdf = fastrak1, vars = ["first_name", "last_name", "address_1", "zip"])

print('level 3')
# Level 3 - First Name, Last Name, City, Address
acct_matches3, matches_to_keep3, clipper3, fastrak3 = match(clipperdf = clipper2, fastrakdf = fastrak2, vars = ["first_name", "last_name", "city", "address_1"])

print('level 4')
#Level 4 - First name, Last name, Address
acct_matches4, matches_to_keep4, clipper4, fastrak4 = match(clipperdf = clipper3, fastrakdf = fastrak3, vars = ["first_name", "last_name", "address_1"])

print('level 5')
#Level 5 - First name, Last name, email
acct_matches5, matches_to_keep5, clipper5, fastrak5 = match(clipperdf = clipper4, fastrakdf = fastrak4, vars = ["first_name", "last_name", "email"])

print('level 6')
fastrak5['phone'] = fastrak5['Day Phone Number']
#Level 6 - First name, Last name, phone
acct_matches6, matches_to_keep6, clipper6, fastrak6 = match(clipperdf = clipper5, fastrakdf = fastrak5, vars = ["first_name", "last_name", "phone"])

print('level 7')
fastrak6['phone'] = fastrak6['Evening Phone']
#Level 7 - First name, Last name, phone
acct_matches7, matches_to_keep7, clipper7, fastrak7 = match(clipperdf = clipper6, fastrakdf = fastrak6, vars = ["first_name", "last_name", "phone"])

print('level 8')
fastrak7['phone'] = fastrak7['Mobile Number']
#Level 8 - First name, Last name, phone
acct_matches8, matches_to_keep8, clipper8, fastrak8 = match(clipperdf = clipper7, fastrakdf = fastrak7, vars = ["first_name", "last_name", "phone"])

print('level 9')
#Level 9 - email, Last name, adrress
acct_matches9, matches_to_keep9, clipper9, fastrak9 = match(clipperdf = clipper8, fastrakdf = fastrak8, vars = ["email", "last_name", "address_1"])

print('level 10')
fastrak9['phone'] = fastrak9['Day Phone Number']
#Level 10 - First name, Last name, phone
acct_matches10, matches_to_keep10, clipper10, fastrak10 = match(clipperdf = clipper9, fastrakdf = fastrak9, vars = ["email", "last_name", "phone"])

print('level 11')
fastrak10['phone'] = fastrak10['Evening Phone']
#Level 1 - First name, Last name, phone
acct_matches11, matches_to_keep11, clipper11, fastrak11 = match(clipperdf = clipper10, fastrakdf = fastrak10, vars = ["email", "last_name", "phone"])

print('level 12')
fastrak11['phone'] = fastrak11['Mobile Number']
#Level 12 - First name, Last name, phone
acct_matches12, matches_to_keep12, clipper12, fastrak12 = match(clipperdf = clipper11, fastrakdf = fastrak11, vars = ["email", "last_name", "phone"])

print('level 13')
fastrak12['phone'] = fastrak12['Day Phone Number']
#Level 13 - First name, Last name, phone
acct_matches13, matches_to_keep13, clipper13, fastrak13 = match(clipperdf = clipper12, fastrakdf = fastrak12, vars = ["address_1", "last_name", "phone"])

print('level 14')
fastrak13['phone'] = fastrak13['Evening Phone']
#Level 14 - First name, Last name, phone
acct_matches14, matches_to_keep14, clipper14, fastrak14 = match(clipperdf = clipper13, fastrakdf = fastrak13, vars = ["address_1", "last_name", "phone"])

print('level 15')
fastrak14['phone'] = fastrak14['Mobile Number']
#Level 15 - First name, Last name, phone
acct_matches15, matches_to_keep15, clipper15, fastrak15 = match(clipperdf = clipper14, fastrakdf = fastrak14, vars = ["address_1", "last_name", "phone"])

print('level 16')
#Level 16 - First name, Last name, phone
acct_matches16, matches_to_keep16, clipper16, fastrak16 = match(clipperdf = clipper15, fastrakdf = fastrak15, vars = ["address_1", "last_name", "first_name", "email"])

print('level 17')
#Level 17 - First name, Last name, phone
acct_matches17, matches_to_keep17, clipper17, fastrak17 = match(clipperdf = clipper16, fastrakdf = fastrak16, vars = ["first_name", "email"])

print('level 18')
fastrak17['phone'] = fastrak17['Day Phone Number']
#Level 18 - First name, Last name, phone
acct_matches18, matches_to_keep18, clipper18, fastrak18 = match(clipperdf = clipper17, fastrakdf = fastrak17, vars = ["first_name", "phone"])

print('level 20')
fastrak18['phone'] = fastrak18['Evening Phone']
#Level 20 - First name, Last name, phone
acct_matches19, matches_to_keep19, clipper19, fastrak19 = match(clipperdf = clipper18, fastrakdf = fastrak18, vars = ["first_name", "phone"])

print('level 21')
fastrak19['phone'] = fastrak19['Mobile Number']
#Level 21 - First name, Last name, phone
acct_matches20, matches_to_keep20, clipper20, fastrak20 = match(clipperdf = clipper19, fastrakdf = fastrak19, vars = ["first_name", "phone"])

matched_so_far = pd.concat([acct_matches1, acct_matches2, acct_matches3, acct_matches4, acct_matches5, 
                            acct_matches6, acct_matches7, acct_matches8, acct_matches9, acct_matches10,
                            acct_matches11, acct_matches12, acct_matches13, acct_matches14, acct_matches15,
                            acct_matches16, acct_matches17, acct_matches18, acct_matches19, acct_matches20])


print("Number of matches found : " + str(matched_so_far.shape[0]))
matched_so_far.to_csv("~/Desktop/matches.csv", encoding='utf-8')
























