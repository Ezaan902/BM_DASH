import os
import geopandas as gpd
import loguru
from tools import load_json_file
from src import geojson_layer, render_pdk, crs_checker, get_color, create_tooltip

# Load path containing data directories
current_dir = os.path.dirname(__file__)
path_file = os.path.join(current_dir, "path.json")
path = load_json_file(path_file)
loguru.logger.info("Loading path file")

# Load the GeoJSON file from the specified path
geodata_path = os.path.join(current_dir, path["data_path"])
gdf = gpd.read_file(geodata_path)
loguru.logger.info("Loading GeoJSON file")

# Load the configuration file
config_path = os.path.join(current_dir, path["config_path"])
config = load_json_file(config_path)
loguru.logger.info("Loading configuration file")

print(gdf.columns)

# Check the CRS of the GeoDataFrame
gdf = crs_checker(gdf)
loguru.logger.info("Checking CRS : {}".format(gdf.crs))

# Assign colors to the GeoDataFrame based on the specified column
gdf['color'] = gdf['df_clustered_cluster'].apply(get_color)
print(gdf[['df_clustered_ind_dens_scaled', 'color']].head())  # Print the cluster and color columns for verification

# Create pydeck layers
layer = geojson_layer(gdf, config)
loguru.logger.info("Creating PyDeck layers")

# Create the PyDeck map
view_state = config["view_state"]
loguru.logger.info("Creating PyDeck map")


# Render the PyDeck map
r = render_pdk(view_state, [layer], config)
loguru.logger.info("Rendering PyDeck map")

r.to_html("map.html")
loguru.logger.info("Saving map as HTML file")















