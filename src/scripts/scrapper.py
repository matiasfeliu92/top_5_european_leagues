import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pyspark.sql import SparkSession

from src.config.settings import Settings
from src.helpers.utils import Utils

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Scrapper:
    def __init__(self, __year__):
        self.settings = Settings()
        self.utils = Utils()
        self.year = __year__
        self.extracted_links = []
        self.unified_data = pd.DataFrame()

    def extract_links(self):
        for path in self.settings.ENDPOINTS:
            current_season = None
            country = path.replace("m.php", "").replace("/", "").strip()
            try:
                complete_url = f"{self.settings.BASE_URL}{path}"
                logging.info(f"----------------------COMPLETE URL: {complete_url}----------------------")
                response = requests.get(complete_url)
                logging.info("ACCEDIENDO.....")
                logging.info(f"----------------------RESPONSE: {response.status_code}----------------------")
                soup = BeautifulSoup(response.text, 'html.parser')
                links_with_seasons = soup.find_all(['i', 'a'])
                for el in links_with_seasons:
                    tag = el.name
                    text = el.text.strip()
                    href = el.get('href') if tag == 'a' else None

                    if tag == "i" and "Season" in text:
                        current_season = text

                    elif tag == "a" and href and ".csv" in href and current_season and self.utils.season_is_after(current_season, int(self.year)):
                        logging.info({
                            "country": country,
                            "season": current_season,
                            "tournament": text,
                            "link": f"{self.settings.BASE_URL}/{href}"
                        })
                        self.extracted_links.append({
                            "country": country,
                            "season": current_season,
                            "tournament": text,
                            "link": f"{self.settings.BASE_URL}/{href}"
                        })
            except Exception as e:
                logging.error(
                    f"Error: {str(e)}\nURL: {complete_url}"
                )

    def save_csv_files(self):
        # links_to_extract = [
        #     item
        #     for item in self.extracted_links
        #     if self.utils.season_is_after(item["season"], int(self.year))
        # ]
        logging.info(f"----------------------LINKS TO EXTRACT: {self.extracted_links}----------------------")
        for csv_file in self.extracted_links:
            logging.info(f"----------------------CSV FILE: {csv_file}----------------------")
            country = csv_file["country"]
            season = csv_file["season"]
            tournament = csv_file["tournament"]
            link = csv_file["link"]
            df = self.utils.read_csv_files(link)
            if not df.empty:
                df["country"] = country
                df["season"] = season
                df["tournament"] = tournament
                df["year"] = df["season"].apply(lambda s: int(s.split()[1].split("/")[0]))
                table_name = f"top_5_european_leagues.{tournament.replace(' ', '_').lower()}_{season.replace('/', '_').replace("Season ", "")}"
                spark = SparkSession.builder.getOrCreate()
                spark.createDataFrame(df).write.format("delta").mode("overwrite").saveAsTable(table_name)
                logging.info(f"----------------------TABLE: {table_name} WAS SAVED----------------------")
            else:
                logging.info(f"----------------------TABLE: {table_name} WAS NOT SAVED----------------------")