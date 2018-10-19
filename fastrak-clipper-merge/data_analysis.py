# This script contains the code for agreegating fastrak and clipper data to do the analysis of customers' location
import pandas as pd
import numpy as np

fastrak = pd.read_csv("./anonym_fastrak.csv", encoding = 'utf-8', index_col='Unnamed: 0')
clipper = pd.read_csv("./anonym_clipper.csv", encoding = 'utf-8', index_col='Unnamed: 0')
relationship = pd.read_csv("./matched_ids.csv", encoding = 'utf-8', index_col='Unnamed: 0')
zip_lon_lat = pd.read_csv("./2017_Gaz_zcta_national.txt", sep = '\t')

zip_lon_lat = zip_lon_lat.rename(columns = {'GEOID':'zip'})
relationship['same_id'] = range(len(relationship))

# merging fastrak/clipper to get the same id
fastrak_joined = fastrak.merge(relationship, on='Record_id_f', how='right')
clipper_joined = clipper.merge(relationship, on='Record_id_c', how='right')

zip_id = fastrak_joined[['city', 'state', 'zip', 'same_id']]
zip_id = zip_id[zip_id['zip']!= 'missing']
zip_id['zip'] = zip_id['zip'].astype('int64')
zip_id = zip_id.merge(zip_lon_lat, on = 'zip', how = 'left')
zip_id1 = zip_id[zip_id['state'] == 'ca']
zip_id2 = zip_id1.dropna()
zip_id2 = zip_id2.rename(columns = {'INTPTLONG                                                                                                                                  ':'INTPTLONG'})


merged_feq_zip = pd.DataFrame(zip_id2.groupby(['INTPTLAT', 'INTPTLONG'], )['same_id'].count())
merged_feq_zip = merged_feq_zip.reset_index()
merged_feq_zip = merged_feq_zip.rename(columns = {'same_id':'frequency'})

# Fastrak

fastrak = fastrak[['city', 'state', 'zip', 'Record_id_f']]
fastrak = fastrak[fastrak['zip']!= 'missing']
fastrak['zip'] = fastrak['zip'].astype('int64')
fastrak = fastrak.merge(zip_lon_lat, on = 'zip', how = 'left')
fastrak = fastrak[fastrak['state'] == 'ca']
fastrak = fastrak.dropna()
fastrak = fastrak.rename(columns = {'INTPTLONG                                                                                                                                  ':'INTPTLONG'})
fastrak = pd.DataFrame(fastrak.groupby(['INTPTLAT', 'INTPTLONG'], )['Record_id_f'].count())
fastrak = fastrak.reset_index()
fastrak = fastrak.rename(columns = {'Record_id_f':'frequency'})

# Clipper

clipper = clipper[clipper['zip']!= 'missing']
clipper['zip'] = clipper[['zip']].convert_objects(convert_numeric=True)
clipper = clipper.dropna()
clipper['zip'] = clipper['zip'].astype('int64')
clipper = clipper.merge(zip_lon_lat, on = 'zip', how = 'left')
clipper = clipper[clipper['state'] == 'ca']
clipper = clipper.dropna()
clipper = clipper.rename(columns = {'INTPTLONG                                                                                                                                  ':'INTPTLONG'})
clipper = pd.DataFrame(clipper.groupby(['INTPTLAT', 'INTPTLONG'], )['Record_id_c'].count())
clipper = clipper.reset_index()
clipper = clipper.rename(columns = {'Record_id_c':'frequency'})
#clipper[(clipper['INTPTLAT'] == 32.553021)&(clipper['INTPTLONG'] == -117.042454)]
#fastrak[(fastrak['INTPTLAT'] == 32.553021)&(fastrak['INTPTLONG'] == -117.042454)]


# Frequency all

allzip = pd.concat([fastrak, clipper])
#allzip[(allzip['INTPTLAT'] == 32.553021)&(allzip['INTPTLONG'] == -117.042454)]
all_feq_zip = pd.DataFrame(allzip.groupby(['INTPTLAT', 'INTPTLONG'], )['frequency'].sum())
all_feq_zip = all_feq_zip.reset_index()
#all_feq_zip[(all_feq_zip['INTPTLAT'] == 32.553021)&(all_feq_zip['INTPTLONG'] == -117.042454)]
all_feq_zip = all_feq_zip.rename(columns = {'frequency':'frequency_all'})
final = merged_feq_zip.merge(all_feq_zip, on = ['INTPTLAT','INTPTLONG'], how = 'left')
final['percent'] = final['frequency']/final['frequency_all']
#final[(final['INTPTLAT'] == 32.553021)&(final['INTPTLONG'] == -117.042454)]
final.to_csv("~/Desktop/frequncy_all.csv", encoding='utf-8')


# # Only FasTrak

fastrak_only = merged_feq_zip.merge(fastrak, on = ['INTPTLAT','INTPTLONG'], how = 'left')
fastrak_only['percent'] = fastrak_only['frequency_x']/fastrak_only['frequency_y']
#fastrak_only[(fastrak_only['INTPTLAT'] == 32.553021)&(fastrak_only['INTPTLONG'] == -117.042454)]
fastrak_only.to_csv("~/Desktop/frequncy_fastrak.csv", encoding='utf-8')


# # Clipper Only

clipper_only = merged_feq_zip.merge(clipper, on = ['INTPTLAT','INTPTLONG'], how = 'left')
clipper_only['percent'] = clipper_only['frequency_x']/clipper_only['frequency_y']
#clipper_only[(clipper_only['INTPTLAT'] == 32.553021)&(clipper_only['INTPTLONG'] == -117.042454)]
clipper_only.to_csv("~/Desktop/frequncy_clipper.csv", encoding='utf-8')




