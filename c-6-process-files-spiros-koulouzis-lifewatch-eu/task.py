import glob
import pandas as pd
import re

import argparse
import json
import os
arg_parser = argparse.ArgumentParser()


arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id






soil_data_prepared = 'soilDataPrepared'      
file_list = glob.glob(soil_data_prepared+'/*_soil.txt')

df_list = []

for file in file_list:
    match = re.search(r'lat([-\d.]+)_lon([-\d.]+)', file)
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
    
    df = pd.read_csv(file, sep='\t', skiprows=2)  # Assuming the files are tab-separated
    
    df['Latitude'] = lat
    df['Longitude'] = lon
    
    df_list.append(df)

soil_data_df = pd.concat(df_list, ignore_index=True)

df_list_csv_path =  'df_list.csv'
soil_data_df.to_csv(df_list_csv_path, index=False)


file_df_list_csv_path = open("/tmp/df_list_csv_path_" + id + ".json", "w")
file_df_list_csv_path.write(json.dumps(df_list_csv_path))
file_df_list_csv_path.close()
