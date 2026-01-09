import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.config.settings import Settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Parser:
    def __init__(self):
        self.settings = Settings()
        self.driver = self.settings.get_chrome_driver()

    # def extract_data_from_elements(
    #     self, by, selector_path, multiple=False, default="", timeout=10
    # ):
    #     try:
    #         wait = WebDriverWait(self.driver, timeout)
    #         if multiple:
    #             print(f"MULTIPLES ELEMENTS BY {by}")
    #             wait.until(EC.presence_of_all_elements_located((by, selector_path)))
    #             elements = self.driver.find_elements(by, selector_path)
    #             return elements if elements else []
    #         else:
    #             print(f"ELEMENT BY {by}")
    #             wait.until(EC.presence_of_element_located((by, selector_path)))
    #             element = self.driver.find_element(by, selector_path)
    #             return element if element else None
    #     except Exception as e:
    #         logging.warning(f"ELEMENTS WITH SELECTOR {selector_path} BY {by} WAS NOT FOUND")
    #         return default

    def extract_data_from_elements(
        self,
        by,
        selector_path,
        multiple=False,
        default=None,
        timeout=10,
    ):
        wait = WebDriverWait(self.driver, timeout)

        try:
            if multiple:
                elements = wait.until(
                    EC.presence_of_all_elements_located((by, selector_path))
                )
                return elements

            element = wait.until(
                EC.visibility_of_element_located((by, selector_path))
            )
            return element

        except TimeoutException:
            logging.warning(
                f"NOT FOUND | by={by} | selector={selector_path}"
            )
            return [] if multiple else default