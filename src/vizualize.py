import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import contextily as cx

DEFAULT_CRS = 3857
DEFAULT_OPCAITY = 0.3
BOUNDARIES_COLOR = "#67a9cf"
TITLE_TEXT_SIZE = 13
DEFAULT_BASEMAP = cx.providers.Stamen.TonerLite


def map_boundaries(
    boundaries: gpd.GeoDataFrame,
    name: str,
) -> Axes:
    _, ax = plt.subplots(
        figsize=(12, 12),
    )

    boundaries = boundaries.to_crs(DEFAULT_CRS)
    boundaries.plot(
        ax=ax,
        alpha=DEFAULT_OPCAITY,
        facecolor=BOUNDARIES_COLOR,
        edgecolor=BOUNDARIES_COLOR,
    )
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.set_title(name, fontsize=TITLE_TEXT_SIZE)
    cx.add_basemap(
        ax,
        source=DEFAULT_BASEMAP,
    )

    return ax
