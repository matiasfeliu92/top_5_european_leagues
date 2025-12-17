import sys
# from src.config.db import ManageDB
# from src.config.settings import Settings
from src.scripts.load import Load
from src.scripts.scrapper import Scrapper
from src.scripts.extract import Extract

if __name__ == "__main__":
    if "E" in sys.argv:
        scrapper = Scrapper()
        scrapper.extract_links()
        scrapper.save_links()
    if "EF" in sys.argv:
        extract = Extract()
        extract.extract_files()
    load = Load()
    load.create_union_views()