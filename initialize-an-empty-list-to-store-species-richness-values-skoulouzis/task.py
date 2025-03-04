from pyproj import Transformer
import numpy as np
import pandas as pd
import rioxarray

import argparse
import json
import os
arg_parser = argparse.ArgumentParser()


arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--df_list', action='store', type=str, required=True, dest='df_list')

arg_parser.add_argument('--random_points_csv_path', action='store', type=str, required=True, dest='random_points_csv_path')

arg_parser.add_argument('--param_maxx', action='store', type=float, required=True, dest='param_maxx')
arg_parser.add_argument('--param_maxy', action='store', type=float, required=True, dest='param_maxy')
arg_parser.add_argument('--param_minx', action='store', type=float, required=True, dest='param_minx')
arg_parser.add_argument('--param_miny', action='store', type=float, required=True, dest='param_miny')

args = arg_parser.parse_args()
print(args)

id = args.id

df_list = json.loads(args.df_list)
random_points_csv_path = args.random_points_csv_path.replace('"','')

param_maxx = args.param_maxx
param_maxy = args.param_maxy
param_minx = args.param_minx
param_miny = args.param_miny

conf_current_mean = 'http://opendap.biodt.eu/ias-pdt/0/outputs/hab3/predictions/Current/Sp_0171_mean.tif'


conf_current_mean = 'http://opendap.biodt.eu/ias-pdt/0/outputs/hab3/predictions/Current/Sp_0171_mean.tif'

tif_data = rioxarray.open_rasterio(conf_current_mean)
tif_data = tif_data.rio.reproject("EPSG:4326")
subset5 = tif_data.rio.clip_box(minx=param_minx, miny=param_miny, maxx=param_maxx, maxy=param_maxy)
random_points5 = np.loadtxt(random_points_csv_path, delimiter=",")
transformer5 = Transformer.from_crs(subset5.rio.crs, "EPSG:4326", always_xy=True)


species_richness_values = []
soil_data_df = pd.concat(df_list, ignore_index=True)

for index, row in soil_data_df.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    
    species_richness = subset5.sel(x=lon, y=lat, method='nearest').values[0]
    
    species_richness_values.append(species_richness)

soil_data_df['Species_Richness'] = species_richness_values

print(soil_data_df)
print(type(soil_data_df))
soil_data_csv_path = '/tmp/data/soil_data.csv'
soil_data_df.to_csv(soil_data_csv_path, sep=',')

file_soil_data_csv_path = open("/tmp/soil_data_csv_path_" + id + ".json", "w")
file_soil_data_csv_path.write(json.dumps(soil_data_csv_path))
file_soil_data_csv_path.close()
