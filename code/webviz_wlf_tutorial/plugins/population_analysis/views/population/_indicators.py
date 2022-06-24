from typing import List

from dash import callback, Input, Output
import pandas as pd
import plotly.colors
from webviz_config.webviz_plugin_subclasses import ViewABC

from ..._plugin_ids import PluginIds
from ...view_elements import Graph

class PopulationIndicators(ViewABC):
    class Ids:
        # pylint: disable=too-few-public-methods
        POPULATION = "population"
        POPULATION_GROWTH = "population-growth"
        RURAL_VS_URBAN_POPULATION = "rural-vs-urban-population"
        RURAL_VS_URBAN_POPULATION_GROWTH = "rural-vs-urban-population-growth"

    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Population indicators")

        self.df_population_absolute = population_df[
            population_df["Indicator Code"].isin(
                ["SP.POP.TOTL", "SP.POP.TOTL.FE.IN", "SP.POP.TOTL.MA.IN"]
            )
        ]

        self.df_population_relative = population_df[
            population_df["Indicator Code"].isin(
                ["SP.POP.TOTL.FE.ZS", "SP.POP.TOTL.MA.ZS"]
            )
        ]

        self.df_population_growth = population_df[
            population_df["Indicator Code"] == "SP.POP.GROW"
        ]

        self.df_rural_urban_population_absolute = population_df[
            population_df["Indicator Code"].isin(
                ["SP.RUR.TOTL", "SP.URB.TOTL"]
            )
        ]

        self.df_rural_urban_population_relative = population_df[
            population_df["Indicator Code"].isin(
                ["SP.RUR.TOTL.ZS", "SP.URB.TOTL.IN.ZS"]
            )
        ]

        self.df_rural_urban_population_growth = population_df[
            population_df["Indicator Code"].isin(
                ["SP.RUR.TOTL.ZG", "SP.URB.GROW"]
            )
        ]

        column = self.add_column()

        first_row = column.make_row()
        first_row.add_view_element(Graph(), PopulationIndicators.Ids.POPULATION)
        first_row.add_view_element(Graph(), PopulationIndicators.Ids.POPULATION_GROWTH)

        second_row = column.make_row()
        second_row.add_view_element(Graph(), PopulationIndicators.Ids.RURAL_VS_URBAN_POPULATION)
        second_row.add_view_element(Graph(), PopulationIndicators.Ids.RURAL_VS_URBAN_POPULATION_GROWTH)

    def set_callbacks(self) -> None:
        @callback(
            Output(self.view_element(PopulationIndicators.Ids.POPULATION).component_unique_id(Graph.Ids.GRAPH).to_string(), "figure"),
            Input(self.get_store_unique_id(PluginIds.Stores.SELECTED_COUNTRIES), "data"),
            Input(self.get_store_unique_id(PluginIds.Stores.SELECTED_YEARS), "data"),
        )
        def _update_plots(countries: List[str], years: List[int]) -> dict:
            colors = plotly.colors.DEFAULT_PLOTLY_COLORS

            df_population = self.df_population_absolute

            title = (
                "Population"
                if True else "Population (% of total population)"
            )

            population = {
                "data":
                    [
                    {
                        "x": list(
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[df_population["Indicator Code"] == "SP.POP.TOTL"]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[df_population["Indicator Code"] == "SP.POP.TOTL"]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, total",
                        "line": {
                            "color": colors[i % len(colors)]
                        }
                    }
                    for i, x in enumerate(countries)
                ] + [
                    {
                        "x": list(
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[df_population["Indicator Code"] == "SP.POP.TOTL.FE.IN"]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[df_population["Indicator Code"] == "SP.POP.TOTL.FE.IN"]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, female",
                        "line": {
                            "color": colors[i % len(colors)],
                            "dash": "dash"
                        }
                    }
                    for i, x in enumerate(countries)
                ] + [
                    {
                        "x": list(
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[df_population["Indicator Code"] == "SP.POP.TOTL.MA.IN"]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[df_population["Indicator Code"] == "SP.POP.TOTL.MA.IN"]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, male",
                        "line": {
                            "color": colors[i % len(colors)],
                            "dash": "dot"
                        }
                    }
                    for i, x in enumerate(countries)
                ],
                "layout": {
                    "title": title,
                    "xaxis": {
                        "range": years
                    }
                }
            }

            return population
