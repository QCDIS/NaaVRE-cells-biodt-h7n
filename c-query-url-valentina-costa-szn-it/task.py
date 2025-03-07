from IPython.display import display
import pandas as pd

import argparse
import json
import os
arg_parser = argparse.ArgumentParser()


arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--habitat_number', action='store', type=str, required=True, dest='habitat_number')

arg_parser.add_argument('--os', action='store', type=str, required=True, dest='os')

arg_parser.add_argument('--param_species_class', action='store', type=str, required=True, dest='param_species_class')

arg_parser.add_argument('--selected_hab_abb', action='store', type=str, required=True, dest='selected_hab_abb')

arg_parser.add_argument('--shutil', action='store', type=str, required=True, dest='shutil')

arg_parser.add_argument('--param_climate_model', action='store', type=str, required=True, dest='param_climate_model')
arg_parser.add_argument('--param_climate_scenario', action='store', type=str, required=True, dest='param_climate_scenario')
arg_parser.add_argument('--param_habitat_name', action='store', type=str, required=True, dest='param_habitat_name')
arg_parser.add_argument('--param_species_name', action='store', type=str, required=True, dest='param_species_name')
arg_parser.add_argument('--param_time_period', action='store', type=str, required=True, dest='param_time_period')

args = arg_parser.parse_args()
print(args)

id = args.id

habitat_number = args.habitat_number.replace('"','')
os = args.os.replace('"','')
param_species_class = args.param_species_class.replace('"','')
selected_hab_abb = args.selected_hab_abb.replace('"','')
shutil = args.shutil.replace('"','')

param_climate_model = args.param_climate_model.replace('"','')
param_climate_scenario = args.param_climate_scenario.replace('"','')
param_habitat_name = args.param_habitat_name.replace('"','')
param_species_name = args.param_species_name.replace('"','')
param_time_period = args.param_time_period.replace('"','')

conf_data_path = '/tmp/data/'


conf_data_path = '/tmp/data/'
url_txt = f"http://opendap.biodt.eu/ias-pdt/0/outputs/hab{selected_hab_abb}/predictions/Prediction_Summary_Shiny.txt"
df_mod = pd.read_csv(url_txt, sep="\t")

hab_num = df_mod[df_mod["hab_name"] == param_habitat_name]["hab_abb"].values[0]
display(df_mod)

tif_path_mean = df_mod[
    (df_mod["hab_abb"] == hab_num) &
    (df_mod["climate_model"] == param_climate_model) &
    (df_mod["climate_scenario"] == param_climate_scenario) &
    (df_mod["time_period"] == param_time_period) &
    (df_mod["species_name"] == param_species_name)
]["tif_path_mean"].values[0]

tif_path_sd = df_mod[
    (df_mod["hab_abb"] == hab_num)
    & (df_mod["climate_model"] == param_climate_model)
    & (df_mod["climate_scenario"] == param_climate_scenario)
    & (df_mod["time_period"] == param_time_period)
    & (df_mod["species_name"] == param_species_name)
]["tif_path_sd"].values[0]

tif_path_cov = df_mod[
    (df_mod["hab_abb"] == hab_num)
    & (df_mod["climate_model"] == param_climate_model)
    & (df_mod["climate_scenario"] == param_climate_scenario)
    & (df_mod["time_period"] == param_time_period)
    & (df_mod["species_name"] == param_species_name)
]["tif_path_cov"].values[0]

tif_path_anomaly = df_mod[
    (df_mod["hab_abb"] == hab_num)
    & (df_mod["climate_model"] == param_climate_model)
    & (df_mod["climate_scenario"] == param_climate_scenario)
    & (df_mod["time_period"] == param_time_period)
    & (df_mod["species_name"] == param_species_name)
]["tif_path_anomaly"].values[0]


filtered_df = df_mod[
    (df_mod["hab_abb"] == habitat_number) &
    (df_mod["climate_model"] == param_climate_model) &
    (df_mod["class"] == param_species_class) 
]

filtered_df = df_mod[
    (df_mod["hab_abb"] == habitat_number) &
    (df_mod["climate_model"] == param_climate_model) &
    (df_mod["class"] == param_species_class) 
]


grouped_tif_paths = filtered_df.groupby("time_period")["tif_path_mean"].agg(list).to_dict()



base_dir = conf_data_path+"output_tif_groups"
shutil.rmtree(base_dir,ignore_errors=True)
os.makedirs(base_dir, exist_ok=True)

year_paths = []
for year, paths in grouped_tif_paths.items():
    year_dir = os.path.join(base_dir, str(year))  # Create a folder for each year
    os.makedirs(year_dir, exist_ok=True)  # Ensure folder exists
    year_paths.append(year_dir)
    file_path = os.path.join(year_dir, f"{year}_tif_paths.txt")  # File name
    with open(file_path, "w") as f:
        for path in paths:
            f.write(path + "\n")  # Write each path on a new line

    print(f"Saved {len(paths)} paths for {year} in {file_path}")





mean_url = f"http://opendap.biodt.eu/ias-pdt/0/outputs/hab{hab_num}/predictions/{tif_path_mean}"
sd_url = f"http://opendap.biodt.eu/ias-pdt/0/outputs/hab{hab_num}/predictions/{tif_path_sd}"
cov_url = f"http://opendap.biodt.eu/ias-pdt/0/outputs/hab{hab_num}/predictions/{tif_path_cov}"
anomaly_url = f"http://opendap.biodt.eu/ias-pdt/0/outputs/hab{hab_num}/predictions/{tif_path_anomaly}"

file_mean_url = open("/tmp/mean_url_" + id + ".json", "w")
file_mean_url.write(json.dumps(mean_url))
file_mean_url.close()
file_sd_url = open("/tmp/sd_url_" + id + ".json", "w")
file_sd_url.write(json.dumps(sd_url))
file_sd_url.close()
file_cov_url = open("/tmp/cov_url_" + id + ".json", "w")
file_cov_url.write(json.dumps(cov_url))
file_cov_url.close()
file_anomaly_url = open("/tmp/anomaly_url_" + id + ".json", "w")
file_anomaly_url.write(json.dumps(anomaly_url))
file_anomaly_url.close()
