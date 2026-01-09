import sys
from src.scripts.load import Load
from src.scripts.scrapper import Scrapper
from src.scripts.extract import Extract

if __name__ == "__main__":
    scrapper = Scrapper()
    scrapper.extract_links()
    scrapper.save_links()
    extract = Extract()
    extract.extract_files()
    load = Load()
    load.create_union_views()