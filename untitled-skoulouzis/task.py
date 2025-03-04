from pyproj import Transformer
import numpy as np
import rioxarray

import argparse
import json
import os
arg_parser = argparse.ArgumentParser()


arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--random_points_csv_path', action='store', type=str, required=True, dest='random_points_csv_path')

arg_parser.add_argument('--param_maxx', action='store', type=float, required=True, dest='param_maxx')
arg_parser.add_argument('--param_maxy', action='store', type=float, required=True, dest='param_maxy')
arg_parser.add_argument('--param_minx', action='store', type=float, required=True, dest='param_minx')
arg_parser.add_argument('--param_miny', action='store', type=float, required=True, dest='param_miny')

args = arg_parser.parse_args()
print(args)

id = args.id

random_points_csv_path = args.random_points_csv_path.replace('"','')

param_maxx = args.param_maxx
param_maxy = args.param_maxy
param_minx = args.param_minx
param_miny = args.param_miny

conf_current_mean = 'http://opendap.biodt.eu/ias-pdt/0/outputs/hab3/predictions/Current/Sp_0171_mean.tif'


conf_current_mean = 'http://opendap.biodt.eu/ias-pdt/0/outputs/hab3/predictions/Current/Sp_0171_mean.tif'
tif_data = rioxarray.open_rasterio(conf_current_mean)
tif_data = tif_data.rio.reproject("EPSG:4326")
subset4 = tif_data.rio.clip_box(minx=param_minx, miny=param_miny, maxx=param_maxx, maxy=param_maxy)
random_points4 = np.loadtxt(random_points_csv_path, delimiter=",")
transformer4 = Transformer.from_crs(subset4.rio.crs, "EPSG:4326", always_xy=True)

coordinates_list = []
for point in random_points4:
    lon, lat = transformer4.transform(point[0], point[1])
    coordinates_list.append({"lat": lat, "lon": lon})

print(coordinates_list)

file_coordinates_list = open("/tmp/coordinates_list_" + id + ".json", "w")
file_coordinates_list.write(json.dumps(coordinates_list))
file_coordinates_list.close()
