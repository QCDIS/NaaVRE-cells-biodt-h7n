
import argparse
import json
import os
arg_parser = argparse.ArgumentParser()


arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--anomaly_url', action='store', type=str, required=True, dest='anomaly_url')

arg_parser.add_argument('--cov_url', action='store', type=str, required=True, dest='cov_url')

arg_parser.add_argument('--mean_url', action='store', type=str, required=True, dest='mean_url')

arg_parser.add_argument('--sd_url', action='store', type=str, required=True, dest='sd_url')


args = arg_parser.parse_args()
print(args)

id = args.id

anomaly_url = args.anomaly_url.replace('"','')
cov_url = args.cov_url.replace('"','')
mean_url = args.mean_url.replace('"','')
sd_url = args.sd_url.replace('"','')



print(mean_url)
print(sd_url)
print(cov_url)
print(anomaly_url)

