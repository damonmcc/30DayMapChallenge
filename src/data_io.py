from datetime import datetime
import pandas as pd
import geopandas as gpd
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def construct_file_suffix_now():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def load_nyc_borough_boundaries() -> gpd.GeoDataFrame:
    url_geojson = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Borough_Boundary/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    nyc_borough_boundaries = gpd.read_file(url_geojson)
    return nyc_borough_boundaries


def load_nyc_city_council_districts() -> gpd.GeoDataFrame:
    url_geojson = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_City_Council_Districts/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    nyc_community_districts = gpd.read_file(url_geojson)
    return nyc_community_districts


def load_nyc_community_districts() -> gpd.GeoDataFrame:
    url_geojson = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Community_Districts/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    nyc_community_districts = gpd.read_file(url_geojson)
    return nyc_community_districts


def load_nyc_pluto() -> pd.DataFrame:
    def convert_dtype(x):
        # handle mixed-type columns
        if not x:
            return ""
        try:
            return str(x)
        except:
            return ""

    url_zip = "https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_pluto_22v2_csv.zip"
    nyc_pluto = pd.read_csv(
        url_zip,
        compression="zip",
        converters={
            21: convert_dtype,
            22: convert_dtype,
            24: convert_dtype,
            26: convert_dtype,
            28: convert_dtype,
        },
    )
    return nyc_pluto


def save_plot_to_png(
    plot: Axes | Figure,
    filename: str,
) -> None:
    if isinstance(plot, Axes):
        fig = plot.get_figure()
    else:
        fig = plot
    fig.savefig(
        f"data/plot/{filename}",
        bbox_inches="tight",
    )
