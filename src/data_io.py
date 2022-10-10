from datetime import datetime
import geopandas as gpd
from matplotlib.axes import Axes


def construct_file_prefix_now():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def load_nyc_borough_boundaries() -> gpd.GeoDataFrame:
    url_geojson = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Borough_Boundary/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    nyc_boundaries = gpd.read_file(url_geojson)
    return nyc_boundaries


def save_axis_to_png(
    plot_axis: Axes,
    filename: str,
) -> None:
    fig = plot_axis.get_figure()
    fig.savefig(
        f"data/plot/{filename}",
        bbox_inches="tight",
    )
