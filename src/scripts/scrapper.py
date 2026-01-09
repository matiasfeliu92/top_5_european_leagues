import logging
import os
import random
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from src.config.settings import Settings
from src.helpers.parser import Parser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Scrapper:
    def __init__(self):
        self.settings = Settings()
        self.parser = Parser()
        self.driver = self.settings.get_chrome_driver()
        self.extracted_links = []

    def extract_links(self):
        for path in self.settings.ENDPOINTS:
            current_season = None
            country = path.replace("m.php", "").replace("/", "").strip()
            try:
                complete_url = f"{self.settings.BASE_URL}{path}"
                logging.info(f"----------------------COMPLETE URL: {complete_url}----------------------")
                self.driver.get(complete_url)
                time.sleep(random.uniform(2, 5))
                links_with_seasons = self.parser.extract_data_from_elements(By.XPATH, "//i | //a", multiple=True)
                for el in links_with_seasons:
                    tag = el.tag_name
                    text = el.text.strip()
                    href = el.get_attribute("href")

                    if tag == "i" and "Season" in text:
                        current_season = text

                    elif tag == "a" and href and ".csv" in href and current_season:
                        self.extracted_links.append({
                            "country": country,
                            "season": current_season,
                            "tournament": text,
                            "link": href
                        })
            except Exception as e:
                logging.error(
                    f"Error: {str(e)}\nURL: {complete_url}"
                )

    def save_links(self):
        df_links = pd.DataFrame(self.extracted_links)
        if not df_links.empty:
            df_links["year"] = df_links["season"].apply(lambda s: int(s.split()[1].split("/")[0]))
            df_links_final = df_links[df_links["year"] >= 2020]
            output_dir = self.settings.create_new_dir(["data", "input"])
            logging.info(output_dir)
            df_links_final.to_csv(
                os.path.join(output_dir, "all_matchs_links.csv"),
                sep=";",
                index=False,
                encoding="utf-8-sig",
            )
        else:
            logging.warning("THERE ARE NO LINKS TO SAVE")