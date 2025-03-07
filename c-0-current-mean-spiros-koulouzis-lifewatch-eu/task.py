
import argparse
import json
import os
arg_parser = argparse.ArgumentParser()


arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id





current_mean = "http://opendap.biodt.eu/ias-pdt/0/outputs/hab3/predictions/Current/Sp_0171_mean.tif"

file_current_mean = open("/tmp/current_mean_" + id + ".json", "w")
file_current_mean.write(json.dumps(current_mean))
file_current_mean.close()
