import pandas as pd

import argparse
import json
import os
arg_parser = argparse.ArgumentParser()


arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--soil_data_csv_path', action='store', type=str, required=True, dest='soil_data_csv_path')


args = arg_parser.parse_args()
print(args)

id = args.id

soil_data_csv_path = args.soil_data_csv_path.replace('"','')




soil_data_df = pd.read_csv(soil_data_csv_path)

correlation_matrix = soil_data_df.corr()

species_soil_correlation = correlation_matrix["Species_Probability"]

print(species_soil_correlation)

