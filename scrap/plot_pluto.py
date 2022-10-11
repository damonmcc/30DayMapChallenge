# python -m scrap.plot_pluto
from src.utils import setup_logging, log_header
from src.data_io import (
    construct_file_suffix_now,
    load_nyc_pluto,
    load_nyc_borough_boundaries,
    save_axis_to_png,
)
from src.transform import map_borough_code_to_name, merge_boundaries_and_data
from src.vizualize import map_choropleth


if __name__ == "__main__":
    logger = setup_logging()

    log_header(logger, "borough_boundaries")
    borough_boundaries = load_nyc_borough_boundaries()
    logger.info(sorted(borough_boundaries.columns))
    boundaries_area_column = "BoroName"
    logger.info(borough_boundaries.value_counts([boundaries_area_column]))

    log_header(logger, "pluto")
    pluto = load_nyc_pluto()
    logger.info(sorted(pluto.columns))
    data_area_column = "borough"
    logger.info(pluto.value_counts([data_area_column]))
    pluto = map_borough_code_to_name(pluto, data_area_column)

    log_header(logger, "pluto_borough_boundaries")
    pluto_borough_boundaries = merge_boundaries_and_data(
        data=pluto,
        data_area_column=data_area_column,
        boundaries=borough_boundaries,
        boundaries_area_column=boundaries_area_column,
    )
    logger.info(sorted(pluto_borough_boundaries.columns))

    log_header(logger, "map_choropleth")
    pluto_ax = map_choropleth(
        data=pluto_borough_boundaries,
        boundary_column=data_area_column,
    )
    save_axis_to_png(pluto_ax, f"pluto_{construct_file_suffix_now()}")

    # geo_name = "NYC City Council Districts"

    # geo_ax = map_boundaries(geo, geo_name)
    # save_axis_to_png(geo_ax, f"{geo_name}_{construct_file_suffix_now()}")
