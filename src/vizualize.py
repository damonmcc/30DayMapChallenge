import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import contextily as cx

CRS_DEFAULT = 3857
OPCAITY_DEFAULT = 0.3
BASEMAP_DEFAULT = cx.providers.Stamen.TonerLite
BASEMAP_NO_LABELS = cx.providers.CartoDB.PositronNoLabels

BOUNDARIES_FILL_COLOR = "#67a9cf"
BOUNDARIES_EDGE_COLOR = "#222222"

TITLE_TEXT_SIZE = 13
DETAIL_TEXT_SIZE = 10


def create_default_axis() -> Axes:
    _, ax = plt.subplots(
        figsize=(12, 12),
    )
    return ax


def map_boundaries(
    boundaries: gpd.GeoDataFrame,
    name: str,
) -> Axes:
    ax = create_default_axis()
    ax.set_title(name, fontsize=TITLE_TEXT_SIZE)

    boundaries = boundaries.to_crs(CRS_DEFAULT)
    boundaries.plot(
        ax=ax,
        alpha=OPCAITY_DEFAULT,
        facecolor=BOUNDARIES_FILL_COLOR,
        edgecolor=BOUNDARIES_EDGE_COLOR,
    )
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    cx.add_basemap(
        ax,
        source=BASEMAP_NO_LABELS,
    )

    return ax


def map_choropleth(
    data: gpd.geodataframe.GeoDataFrame,
    boundary_column: str,
) -> Axes:
    annotation_background_color = "#eeeeee"
    _, ax = plt.subplots(1, figsize=(10, 10))
    ax.axis("off")
    ax.set_title(
        f"# of Pluto records ",
        fontdict={
            "fontsize": TITLE_TEXT_SIZE,
            "fontweight": "3",
        },
    )

    data = data.to_crs(CRS_DEFAULT)
    data.plot(
        ax=ax,
        column="count",
        cmap="Blues",
        linewidth=1.5,
        alpha=0.9,
        edgecolor="k",
    )
    cx.add_basemap(
        ax,
        crs=CRS_DEFAULT,
        source=BASEMAP_NO_LABELS,
        attribution=False,
    )

    data["coords"] = data["geometry"].apply(
        lambda x: x.representative_point().coords[:]
    )
    data["coords"] = [coords[0] for coords in data["coords"]]
    for _, row in data.iterrows():
        plt.annotate(
            text=f"{row[boundary_column]}\n{row['count']:,}",
            xy=row["coords"],
            horizontalalignment="center",
            size=DETAIL_TEXT_SIZE,
            bbox=dict(boxstyle="round", fc=annotation_background_color),
        )

    total_calls = data["count"].sum()
    plt.annotate(
        text=f"TOTAL \n{total_calls:,}",
        xy=(0.85, 0.1),
        xycoords="axes fraction",
        horizontalalignment="center",
        size=DETAIL_TEXT_SIZE + 2,
        bbox=dict(boxstyle="round", fc=annotation_background_color),
    )

    return ax
