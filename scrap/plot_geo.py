# python -m scrap.plot_geo

from src.data_io import (
    construct_file_suffix_now,
    load_nyc_city_council_districts,
    save_axis_to_png,
)
from src.vizualize import map_boundaries


if __name__ == "__main__":
    geo = load_nyc_city_council_districts()
    geo_name = "NYC City Council Districts"

    geo_ax = map_boundaries(geo, geo_name)
    save_axis_to_png(geo_ax, f"{geo_name}_{construct_file_suffix_now()}")
