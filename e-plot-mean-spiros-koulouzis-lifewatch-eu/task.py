from minio import Minio
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os
import rioxarray

import argparse
import json
import os
arg_parser = argparse.ArgumentParser()

secret_minio_access_key = os.getenv('secret_minio_access_key')
secret_minio_secret_key = os.getenv('secret_minio_secret_key')

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--merged_tifs', action='store', type=str, required=True, dest='merged_tifs')

arg_parser.add_argument('--param_climate_model', action='store', type=str, required=True, dest='param_climate_model')
arg_parser.add_argument('--param_habitat_name', action='store', type=str, required=True, dest='param_habitat_name')
arg_parser.add_argument('--param_minio_endpoint', action='store', type=str, required=True, dest='param_minio_endpoint')
arg_parser.add_argument('--param_minio_user_prefix', action='store', type=str, required=True, dest='param_minio_user_prefix')
arg_parser.add_argument('--param_species_class', action='store', type=str, required=True, dest='param_species_class')

args = arg_parser.parse_args()
print(args)

id = args.id

merged_tifs = json.loads(args.merged_tifs)

param_climate_model = args.param_climate_model.replace('"','')
param_habitat_name = args.param_habitat_name.replace('"','')
param_minio_endpoint = args.param_minio_endpoint.replace('"','')
param_minio_user_prefix = args.param_minio_user_prefix.replace('"','')
param_species_class = args.param_species_class.replace('"','')

conf_x = 0.95

conf_y = 0.95

conf_arrow_length = 0.1

conf_data_path = '/tmp/data/'


conf_x = 0.95
conf_y = 0.95
conf_arrow_length = 0.1
conf_data_path = '/tmp/data/'
print(merged_tifs)
frames = []


for tif_file in merged_tifs:
    print(tif_file)
    data_mean = rioxarray.open_rasterio(tif_file)
    frames.append(data_mean[0])    



fig, ax = plt.subplots(figsize=(10, 8))
img = frames[0].plot(ax=ax, cmap="Spectral", add_colorbar=True)
ax.grid(True, linestyle="--", linewidth=0.5)

ax.annotate( "N",
    xy=(conf_x, conf_y),
    xytext=(conf_x, conf_y - conf_arrow_length),
    arrowprops=dict(facecolor="black", width=5, headwidth=15),
    ha="center",
    va="center",
    fontsize=12,
    xycoords=ax.transAxes,
)

def update(frame_idx):
    img.set_array(frames[frame_idx].values)
    ax.set_title(
        f"Mean Species Distribution for {param_species_class} in {param_habitat_name} "
        f"for {param_climate_model}\nFrame {frame_idx + 1}"
    )
    return img

ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=1000, blit=False)
output_gif = conf_data_path + os.path.basename(tif_file)
ani.save(output_gif, writer="pillow", fps=2)

print(f"Animation saved as {output_gif}")

mc = Minio(endpoint=param_minio_endpoint,
           access_key=secret_minio_access_key,
           secret_key=secret_minio_secret_key)


mc.fput_object(bucket_name="naa-vre-user-data", file_path=output_gif, object_name=f"{param_minio_user_prefix}/merged_output.tif")

