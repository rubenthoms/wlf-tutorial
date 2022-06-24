from typing import Type
from pathlib import Path

from dash.development.base_component import Component
import pandas as pd
from webviz_config import WebvizPluginABC

from ._error import error
from ._plugin_ids import PluginIds
from .shared_settings import Filter
from .views.population import PopulationIndicators

class PopulationAnalysis(WebvizPluginABC):
    def __init__(self, path_to_population_data_csv_file: Path) -> None:
        super().__init__(stretch=True)

        self.error_message = ""

        try:
            self.population_df = pd.read_csv(path_to_population_data_csv_file)
        except PermissionError:
            self.error_message = (
                f"Access to file '{path_to_population_data_csv_file}' denied."
                "Please check your path for 'path_to_population_data_csv_file' and make sure you have access to it."
            )
            return
        except FileNotFoundError:
            self.error_message = (
                f"File '{path_to_population_data_csv_file}' not found."
                "Please check your path for 'path_to_population_data_csv_file'."
            )
            return

        self.add_store(PluginIds.Stores.SELECTED_COUNTRIES, WebvizPluginABC.StorageType.SESSION)
        self.add_store(PluginIds.Stores.SELECTED_YEARS, WebvizPluginABC.StorageType.SESSION)

        self.add_shared_settings_group(Filter(self.population_df), PluginIds.SharedSettings.FILTER)

        self.add_view(PopulationIndicators(self.population_df), PluginIds.Population.INDICATORS, PluginIds.Population.GROUP_NAME)

    @property
    def layout(self) -> Type[Component]:
        return error(self.error_message)
        