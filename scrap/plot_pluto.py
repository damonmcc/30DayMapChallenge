# python -m scrap.plot_pluto
import pandas as pd
from src.utils import setup_logging, log_header
from src.data_io import (
    construct_file_suffix_now,
    load_nyc_city_council_districts,
    load_nyc_pluto,
    load_nyc_borough_boundaries,
    save_plot_to_png,
)
from src.transform import (
    decode_borough_code_to_name,
    merge_boundaries_and_data,
    zeroes_to_nan,
    outliers_to_ceiling,
)
from src.vizualize import (
    map_choropleth,
    histogram_pluto_field,
    histogram_pluto_field_facets,
    bihistogram_pluto_field_facets,
    map_ploto_field,
)

pd.options.display.float_format = "{:,.2f}".format


if __name__ == "__main__":
    logger = setup_logging()
    # interest = "resarea"
    # interest_label= "square feet for residential use"
    interest = "unitsres"
    interest_label = "residential units"

    log_header(logger, "city_council_districts")
    borough_boundaries = load_nyc_city_council_districts()
    # log_header(logger, "borough_boundaries")
    # borough_boundaries = load_nyc_borough_boundaries()
    logger.info(sorted(borough_boundaries.columns))
    boundaries_area_column = "CounDist"
    # boundaries_area_column = "BoroName"
    borough_boundaries[boundaries_area_column] = borough_boundaries[
        boundaries_area_column
    ].astype(float)
    # logger.info(borough_boundaries.value_counts([boundaries_area_column], dropna=False))
    # logger.info(borough_boundaries.value_counts(["council"]))

    log_header(logger, "load pluto")
    pluto = load_nyc_pluto()
    logger.info(sorted(pluto.columns))
    logger.info(f"Describe '{interest}'\n{pluto[interest].describe()}\n")

    log_header(logger, "transform pluto")
    pluto = zeroes_to_nan(pluto, interest)
    pluto = outliers_to_ceiling(
        data=pluto,
        field=interest,
        # ceiling=5_000,
        ceiling=100,
    )
    logger.info(f"Describe '{interest}'\n{pluto[interest].describe()}\n")

    log_header(logger, "histogram")
    ax_pluto_histogram = histogram_pluto_field(
        data=pluto,
        field=interest,
        log_x=True,
        # bins=50,
    )
    save_plot_to_png(
        ax_pluto_histogram,
        f"pluto_histo_{interest}_{construct_file_suffix_now()}",
    )
    fig_pluto_histogram = histogram_pluto_field_facets(
        data=pluto,
        field=interest,
        column_facet="borough",
        log_x_base=10,
    )
    # fig_pluto_bihistogram = bihistogram_pluto_field_facets(
    #     data=pluto,
    #     field_x="unitsres",
    #     column_facet="borough",
    # )
    save_plot_to_png(
        fig_pluto_histogram,
        f"pluto_histofacets_{interest}_{construct_file_suffix_now()}",
    )

    log_header(logger, "map")
    # print(pluto.value_counts(["council"]))
    ax_pluto_map = map_ploto_field(
        data=pluto,
        field=interest,
        field_label=interest_label,
    )
    save_plot_to_png(ax_pluto_map, f"pluto_{interest}_{construct_file_suffix_now()}")

    # # data_area_column = "council"
    # # # data_area_column = "borough"
    # # pluto = map_borough_code_to_name(pluto, data_area_column)
    # logger.info(pluto.value_counts([data_area_column], dropna=False))
    # # print(pluto.value_counts(["council"]))

    # log_header(logger, "pluto_and_boundaries")
    # pluto_and_boundaries = merge_boundaries_and_data(
    #     data=pluto,
    #     data_area_column=data_area_column,
    #     boundaries=borough_boundaries,
    #     boundaries_area_column=boundaries_area_column,
    # )
    # logger.info(sorted(pluto_and_boundaries.columns))

    # log_header(logger, "map_choropleth")
    # log_header(logger, "map_choropleth")
    # pluto_ax = map_choropleth(
    #     data=pluto_and_boundaries,
    #     boundary_column=data_area_column,
    # )
    # save_plot_to_png(pluto_ax, f"pluto_{interest}_{construct_file_suffix_now()}")

    # geo_name = "NYC City Council Districts"

    # geo_ax = map_boundaries(geo, geo_name)
    # save_plot_to_png(geo_ax, f"{geo_name}_{construct_file_suffix_now()}")
