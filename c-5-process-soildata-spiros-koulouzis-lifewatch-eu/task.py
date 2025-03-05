from soilgrids import data_processing as dprc
import glob
import os
import shutil

import argparse
import json
import os
arg_parser = argparse.ArgumentParser()


arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--coordinates_list', action='store', type=str, required=True, dest='coordinates_list')


args = arg_parser.parse_args()
print(args)

id = args.id

coordinates_list = json.loads(args.coordinates_list)





for coord in coordinates_list:
    dprc.data_processing(coord)
    
soil_data_prepared = '/tmp/data/soilDataPrepared'        
if not os.path.exists(soil_data_prepared):
    os.makedirs(soil_data_prepared)
    
txt_files = glob.glob(os.path.join('soilDataPrepared', '*.txt'))
for txt_file in txt_files:
    try:
        target_path = os.path.join(soil_data_prepared, os.path.basename(txt_file))
        
        shutil.move(txt_file, target_path)
    except Exception as e:
        print(f"Error moving file {txt_file}: {e}")
        

file_soil_data_prepared = open("/tmp/soil_data_prepared_" + id + ".json", "w")
file_soil_data_prepared.write(json.dumps(soil_data_prepared))
file_soil_data_prepared.close()
