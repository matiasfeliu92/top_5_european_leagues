import logging
import os
import pandas as pd

from src.config.settings import Settings
from src.helpers.utils import Utils
from src.scripts.load import Load


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Extract:
    def __init__(self):
        self.load = Load()
        self.settings = Settings()
        self.utils = Utils()
        self.base_dir = self.settings.BASE_DIR

    def extract_files(self):
        files_dir = os.path.join(self.base_dir, "data", "input")
        files_list = [os.path.join(files_dir, file) for file in os.listdir(files_dir) if "links" in file]
        df_all_links = pd.read_csv(files_list[0], sep=";")
        for _, row in df_all_links.iterrows():
            file_link = row["link"]
            league = row["tournament"]
            season = row["season"]
            country = row["country"]
            logging.info(f"-------------------------LEAGUE: {league}, FILE: {file_link}-------------------------")
            df = self.utils.read_csv_files(file_link)
            df["league"] = league
            df["season"] = season
            df["country"] = country
            df_renamed = self.utils.rename_columns(df, {"ï»¿Div": "Div"})
            logging.info(df_renamed.info())
            self.load.load_data_in_DB(df_renamed, league, season)