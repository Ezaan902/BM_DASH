import os
import pydeck as pdk
import geopandas as gpd
from tools.tools import load_json_file

def geojson_layer(geodata: gpd.GeoDataFrame, config: dict, **kwargs) -> pdk.Layer:
    """
    Create a GeoJsonLayer from a GeoDataFrame.
    
    Parameters  
    ----------
    data : gpd.GeoDataFrame
        The GeoDataFrame to be visualized.
    **kwargs
        Additional arguments to pass to the GeoJsonLayer constructor.
        
    Returns
    -------
    pdk.Layer
        A PyDeck GeoJsonLayer.
    """
    layer_config = config.get('geojson_layer', {})
    layer_config.update(kwargs)
    
    return pdk.Layer(
        data=geodata,
        **layer_config
    )

def render_pdk(view_state: dict, layers: list, config: dict) -> pdk.Deck:
    """
    Render a PyDeck map.
    
    Parameters
    ----------
    view_state : dict
        The initial state of the map, including parameters like latitude, longitude, zoom, etc.
    layers : list
        A list of PyDeck layers to be rendered on the map.
    config : dict
        Configuration dictionary containing additional settings such as map style.
        
    Returns
    -------
    pdk.Deck
        A PyDeck map object configured with the specified view state, layers, and map style.
    """
    map_style = config['map_style']
    
    return pdk.Deck(
        initial_view_state=view_state,
        layers=layers,
        map_style=map_style
    )

def create_tooltip(row: gpd.GeoSeries) -> dict:
    """
    Create a tooltip text from a JSON dictionary.
    
    Parameters
    ----------
    json_data : dict
        The JSON dictionary containing the data for the tooltip.
        
    Returns
    -------
    dict
        A dictionary with the HTML content for the tooltip.
    """
    tooltip_text = {
        "html": (
            f"<b style='color: white;'>Identifiant: {row.get('idcar_200m', '')}</b><br>"
            f"Nombre d'individus: <b style='color: white;'>{row.get('ind', '')}</b><br>"
            f"Nombre de ménages: <b style='color: #EE776E;'>{row.get('men', '')}</b><br>"
            f"Somme des revenus winsorisés: <b style='color: #EE776E;'>{row.get('ind_snv', '')}</b><br>"
            f"Cluster: <b style='color: #EE776E;'>{row.get('cluster', '')}</b><br>"
            "<i style='font-size: 0.7em;'>Source: INSEE 2023 </i>"
        )
    }
    return tooltip_text

def get_color(cluster: int) -> list:
    """
    Get the color for a specific cluster.
    
    Parameters
    ----------
    cluster : int
        The cluster number for which to retrieve the color.
    colors : dict
        A dictionary mapping cluster numbers to color values.
        
    Returns
    -------
    list
        A list of RGBA color values.
    """
    if cluster == '1':
        return [255, 0, 0, 200]  # Red
    elif cluster == '2':
        return [0, 255, 0, 200]  # Green
    elif cluster == '3':
        return [0, 0, 255, 200]  # Blue
    else:
        return [255, 255, 255, 200]  # White

def crs_checker(geodata: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Check the CRS of a GeoDataFrame and reproject it if necessary.
    
    Parameters
    ----------
    geodata : gpd.GeoDataFrame
        The GeoDataFrame to check and reproject.
        
    Returns
    -------
    gpd.GeoDataFrame
        The reprojected GeoDataFrame.
    """
    try:
        if geodata.crs != "EPSG:4326":
            geodata = geodata.to_crs("EPSG:4326")
        return geodata
    except Exception as e:
        print(f"An error occurred while checking or reprojecting CRS: {e}")
        return geodata

    
