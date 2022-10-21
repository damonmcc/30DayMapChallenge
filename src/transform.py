import geopandas as gpd
import numpy as np
import pandas as pd


def combine_geodataframes(geodataframes: list[gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
    return pd.concat(geodataframes)


def zeroes_to_nan(
    data: pd.DataFrame,
    field: str,
):
    data[field] = data[field].replace(0, np.nan)
    return data


def outliers_to_ceiling(
    data: pd.DataFrame,
    field: str,
    ceiling: float = None,
) -> pd.DataFrame:
    default_upper_quantile = 0.99
    if not ceiling:
        ceiling = data[field].quantile(default_upper_quantile)
    data[field].loc[data[field] > ceiling] = ceiling

    return data


def outliers_to_nan(
    data: pd.DataFrame,
    field: str,
) -> pd.DataFrame:
    upper_limit = data[field].quantile()

    field_transformed = data[field].dropna()
    field_transformed = field_transformed.sort_values()
    if outliers_to_drop[0]:
        field_transformed = field_transformed.iloc[outliers_to_drop[0] :]
    if outliers_to_drop[1]:
        field_transformed = field_transformed.iloc[: -outliers_to_drop[1]]
    data[field] = field_transformed

    return data


def decode_borough_code_to_name(
    data: pd.DataFrame,
    borough_code_column: str,
) -> pd.DataFrame:
    mapping_dict = {
        "BX": "Bronx",
        "BK": "Brooklyn",
        "MN": "Manhattan",
        "QN": "Queens",
        "SI": "Staten Island",
    }
    data[borough_code_column] = (
        data[borough_code_column].map(mapping_dict).fillna(data[borough_code_column])
    )

    return data


def aggregate_counts_by_fields(
    data: pd.DataFrame,
    fields_of_interest: list[str],
) -> pd.DataFrame:
    data_counts = (
        data.groupby(fields_of_interest)
        .size()
        .reset_index()
        .rename(columns={0: "count"})
    )

    return data_counts


# def aggregate_counts_across_area(
#     data: pd.DataFrame,
#     area_column: str,
# ) -> pd.DataFrame:
#     return


def construct_coordinates(lat, lon):
    if pd.isnull(lat) or pd.isnull(lon):
        return np.nan
    return ", ".join([str(lat), str(lon)])


def merge_boundaries_and_data(
    data: pd.DataFrame,
    data_area_column: str,
    boundaries: gpd.geodataframe.GeoDataFrame,
    boundaries_area_column: str,
) -> gpd.GeoDataFrame:

    # aggregate data by area
    data_counts = aggregate_counts_by_fields(data, [data_area_column])

    # align values to merge with
    data_counts[data_area_column] = (
        data_counts[data_area_column].astype(str).str.title()
    )
    boundaries[boundaries_area_column] = (
        boundaries[boundaries_area_column].astype(str).str.title()
    )

    # merge data and boundaries
    data_and_boundaries = gpd.GeoDataFrame(
        data_counts.merge(
            boundaries,
            how="left",
            left_on=data_area_column,
            right_on=boundaries_area_column,
        )
    )
    return data_and_boundaries
