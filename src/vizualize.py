from dataclasses import field
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import contextily as cx
import seaborn as sns

from src.transform import construct_coordinates

CRS_DEFAULT = 3857
OPCAITY_DEFAULT = 0.3
BASEMAP_DEFAULT = cx.providers.Stamen.TonerLite
BASEMAP_NO_LABELS = cx.providers.CartoDB.PositronNoLabels

pd.options.display.float_format = "{:,.2f}".format
sns.set_theme(style="darkgrid")
BOUNDARIES_FILL_COLOR = "#67a9cf"
BOUNDARIES_EDGE_COLOR = "#222222"
ANNOTATION_BACKGROUND_COLOR = "#eeeeee"

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
    data: gpd.GeoDataFrame,
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
    if len(data) < 10:
        for _, row in data.iterrows():
            plt.annotate(
                text=f"{row[boundary_column]}\n{row['count']:,}",
                xy=row["coords"],
                horizontalalignment="center",
                size=(DETAIL_TEXT_SIZE + 2) * (5 / len(data)),
                # size=DETAIL_TEXT_SIZE,
                bbox=dict(boxstyle="round", fc=annotation_background_color),
            )

    total_calls = data["count"].sum()
    plt.annotate(
        text=f"TOTAL \n{total_calls:,}",
        xy=(0.85, 0.1),
        xycoords="axes fraction",
        horizontalalignment="center",
        # size=(DETAIL_TEXT_SIZE + 2) * (5 / len(data)),
        size=DETAIL_TEXT_SIZE + 2,
        bbox=dict(boxstyle="round", fc=annotation_background_color),
    )

    return ax


def histogram_pluto_field(
    data: gpd.GeoDataFrame,
    field: str,
    bins: int = None,
    log_x: bool = False,
) -> Axes:
    if not bins:
        bins = "auto"
    # fig = plt.figure(figsize=(10, 10))  # _ x _ inch page
    # _, ax = plt.subplots(1)
    _, ax = plt.subplots(1, figsize=(10, 10))
    # gs_main = fig.add_gridspec(
    #     1,
    #     1,
    #     # width_ratios=[0.3, 0.3, 0.4],
    # )  # Overall: ? row, ? columns
    # ax.axis("off")
    # ax.set_title(
    #     f"Pluto records: {fields}",
    #     fontdict={
    #         "fontsize": TITLE_TEXT_SIZE,
    #         "fontweight": "3",
    #     },
    # )

    # for plot_index, field in enumerate(fields):
    #     print(f"{field}")
    #     x = data[field]
    #     ax_field = fig.add_gridspec(gs_main[plot_index])
    #     sns.distplot(
    #         x,
    #         ax=ax_field,
    #         # bins=num_bins,
    #     )
    # _, bins = np.histogram(x, bins=num_bins)
    # logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), len(bins))
    # plt.yscale("log", nonposy="clip")

    sns.histplot(
        x=data[field],
        ax=ax,
        bins=bins,
        binwidth=1,
        log=log_x,
    )
    # ax.hist(
    #     x,
    #     log=True,
    #     bins=num_bins,
    #     # bins=logbins,
    #     # bins="auto",
    # )
    # ax.set_yscale("log")

    # df_penguins = sns.load_dataset("penguins")
    # sns_ax = sns.displot(
    #     df_penguins,
    #     x="flipper_length_mm",
    #     col="species",
    #     row="sex",
    #     binwidth=3,
    #     height=3,
    #     facet_kws=dict(margin_titles=True),
    # )

    return ax


def histogram_pluto_field_facets(
    data: gpd.GeoDataFrame,
    field: str,
    column_facet: str = None,
    row_facet: str = None,
    log_x_base: bool = False,
):
    figure_displot = sns.displot(
        data,
        x=field,
        col=column_facet,
        row=row_facet,
        # log_scale=(log_x_base, False),
        binwidth=1,
        # height=3,
        # stat="frequency",
        facet_kws=dict(margin_titles=True),
    )
    return figure_displot


def bihistogram_pluto_field_facets(
    data: gpd.GeoDataFrame,
    field_x: str,
    field_y: str,
    column_facet: str = None,
    row_facet: str = None,
):
    figure_displot = sns.displot(
        data,
        x=field_x,
        y=field_y,
        col=column_facet,
        row=row_facet,
        # log_scale=10,
        # binwidth=3,
        # height=3,
        # stat="frequency",
        cbar=True,
        # cbar_kws=dict(shrink=0.75),
        facet_kws=dict(margin_titles=True),
    )
    return figure_displot


def map_ploto_field(
    data: gpd.GeoDataFrame,
    field: str,
    field_label: str = None,
) -> Axes:
    if not field_label:
        field_label = field
    # annotation_background_color = "#eeeeee"
    _, ax = plt.subplots(1, figsize=(10, 10))
    # ax.axis("off")
    ax.set_title(
        f"Pluto records: {field}",
        fontdict={
            "fontsize": TITLE_TEXT_SIZE,
            "fontweight": "3",
        },
    )
    # data_trimmed = data[["longitude", "latitude", field]]

    # data_trimmed_geometry = gpd.GeoDataFrame(
    #     data_trimmed,
    #     geometry=gpd.points_from_xy(
    #         data_trimmed["longitude"],
    #         data_trimmed["latitude"],
    #         crs=CRS_DEFAULT,
    #         #         crs=coordinates_crs,
    #     ),
    # )

    # # data_trimmed_geometry = data_trimmed_geometry.to_crs(CRS_DEFAULT)
    # data_trimmed_geometry.plot(
    #     ax=ax,
    #     column=field,
    #     cmap="Blues",
    #     # linewidth=1.5,
    #     alpha=0.9,
    #     # edgecolor="k",
    # )
    data["geometry"] = data[["latitude", "longitude"]].apply(
        lambda row: construct_coordinates(*row), axis=1
    )

    data_valid = data[pd.notnull(data["geometry"])]
    data_valid = gpd.GeoDataFrame(
        data_valid,
        geometry=gpd.points_from_xy(
            data_valid["longitude"],
            data_valid["latitude"],
            crs=CRS_DEFAULT,
            #         crs=coordinates_crs,
        ),
    )
    # pcm = ax.pcolor(
    #     X,
    #     Y,
    #     Z,
    #     norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),
    #     cmap="PuBu_r",
    #     shading="auto",
    # )
    # cmap_log = colors.LogNorm(vmin=Z.min(), vmax=Z.max())
    # plt.pcolormesh(ax=ax, data=data_valid)

    data_valid.plot(
        ax=ax,
        column=field,
        # cmap=cmap_log,
        cmap="Blues",
        # linewidth=1.5,
        markersize=1,
        alpha=0.9,
        # edgecolor="k",
    )

    vmin, vmax = min(data[field]), max(data[field])
    sm = plt.cm.ScalarMappable(
        cmap="Blues",
        norm=plt.Normalize(vmin=vmin, vmax=vmax),
    )
    sm.set_array([])
    ax_ins = inset_axes(
        ax,
        width="30%",  # X% of parent_bbox width
        height="2%",  # X% of parent_bbox heigh
        loc=8,
        bbox_to_anchor=(0, 0.08, 1, 1),
        bbox_transform=ax.transAxes,  #     borderpad=0,
    )
    cb1 = plt.colorbar(
        sm,
        cax=ax_ins,
        orientation="horizontal",
    )
    ax_ins.set_facecolor(ANNOTATION_BACKGROUND_COLOR)
    cb1.set_label(field_label, fontsize=DETAIL_TEXT_SIZE)

    # cx.add_basemap(
    #     ax,
    #     # crs=CRS_DEFAULT,
    #     source=BASEMAP_NO_LABELS,
    #     attribution=False,
    # )

    return ax
