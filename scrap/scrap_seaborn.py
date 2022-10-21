import matplotlib.pyplot as plt
import seaborn as sns
from src.data_io import (
    construct_file_suffix_now,
    save_plot_to_png,
)
from src.vizualize import bihistogram_pluto_field_facets, histogram_pluto_field_facets

if __name__ == "__main__":
    df = sns.load_dataset("penguins")
    figure_seaborn = bihistogram_pluto_field_facets(
        df,
        "flipper_length_mm",
        "body_mass_g",
        "species",
        # "sex",
    )
    # figure_seaborn = sns.displot(
    #     df,
    #     x="flipper_length_mm",
    #     col="species",
    #     row="sex",
    #     binwidth=3,
    #     height=3,
    #     facet_kws=dict(margin_titles=True),
    # )

    save_plot_to_png(figure_seaborn, f"seaborn_{construct_file_suffix_now()}")
