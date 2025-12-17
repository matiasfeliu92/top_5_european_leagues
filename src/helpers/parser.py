import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    #     self, by, path, multiple=False, default="", timeout=10
    # ):
    #     try:
    #         wait = WebDriverWait(self.driver, timeout)
    #         if multiple:
    #             print("MULTIPLE")
    #             wait.until(EC.presence_of_all_elements_located((by, path)))
    #             elements = self.driver.find_elements(by, path)
    #             return elements if elements else []
    #         else:
    #             print("ELEMENT")
    #             wait.until(EC.presence_of_element_located((by, path)))
    #             element = self.driver.find_element(by, path)
    #             return element if element else None
    #     except Exception as e:
    #         print("Fallo al obtener el texto:", e)
    #         return default
        
    def extract_data_from_elements(
        self, by, selector_path, multiple=False, default="", timeout=10
    ):
        try:
            wait = WebDriverWait(self.driver, timeout)
            if multiple:
                print(f"MULTIPLES ELEMENTS BY {by}")
                wait.until(EC.presence_of_all_elements_located((by, selector_path)))
                elements = self.driver.find_elements(by, selector_path)
                return elements if elements else []
            else:
                print(f"ELEMENT BY {by}")
                wait.until(EC.presence_of_element_located((by, selector_path)))
                element = self.driver.find_element(by, selector_path)
                return element if element else None
        except Exception as e:
            logging.warning(f"ELEMENTS WITH SELECTOR {selector_path} BY {by} WAS NOT FOUND")
            return default

    # def extract_data_from_elements(
    #     self, key, selector, by, multiple=False, web_element=None
    # ):
    #     if by == "ID":
    #         element = self.safe_find_elements(By.ID, selector)
    #         if element:
    #             logging.info(f"----------------ELEMENT FOUND----------------")
    #             return element
    #         else:
    #             logging.warning(f"ELEMENT {key} WITH SELECTOR {selector} WAS NOT FOUND")
    #     elif by == "CLASS_NAME":
    #         elements = self.safe_find_elements(By.CLASS_NAME, selector, multiple=True)
    #         if elements:
    #             logging.info(f"----------------ELEMENTS FOUND----------------")
    #             return elements
    #         else:
    #             logging.warning(
    #                 f"ELEMENTS {key} WITH SELECTOR {selector} WAS NOT FOUND"
    #             )
    #     elif by == "CSS_SELECTOR":
    #         if multiple == False:
    #             elements = self.safe_find_elements(By.CSS_SELECTOR, selector)
    #             if elements:
    #                 logging.info(f"----------------ELEMENTS FOUND----------------")
    #                 return elements
    #             else:
    #                 logging.warning(
    #                     f"ELEMENTS {key} WITH SELECTOR {selector} WAS NOT FOUND"
    #                 )
    #         else:
    #             elements = self.safe_find_elements(
    #                 By.CSS_SELECTOR, selector, multiple=True
    #             )
    #             if elements:
    #                 logging.info(f"----------------ELEMENTS FOUND----------------")
    #                 return elements
    #             else:
    #                 logging.warning(
    #                     f"ELEMENTS {key} WITH SELECTOR {selector} WAS NOT FOUND"
    #                 )
    #     elif by == "XPATH":
    #         if multiple == False:
    #             elements = self.safe_find_elements(By.XPATH, selector)
    #             if elements:
    #                 logging.info(f"----------------ELEMENTS FOUND----------------")
    #                 return elements
    #             else:
    #                 logging.warning(
    #                     f"ELEMENTS {key} WITH SELECTOR {selector} WAS NOT FOUND"
    #                 )
    #         else:
    #             elements = self.safe_find_elements(By.XPATH, selector, multiple=True)
    #             if elements:
    #                 logging.info(f"----------------ELEMENTS FOUND----------------")
    #                 return elements
    #             else:
    #                 logging.warning(
    #                     f"ELEMENTS {key} WITH SELECTOR {selector} WAS NOT FOUND"
    #                 )
    #     elif by == "TAG NAME":
    #         if multiple == False:
    #             elements = self.safe_find_elements(By.TAG_NAME, selector)
    #             if elements:
    #                 logging.info(f"----------------ELEMENTS FOUND----------------")
    #                 return elements
    #             else:
    #                 logging.warning(
    #                     f"ELEMENTS {key} WITH SELECTOR {selector} WAS NOT FOUND"
    #                 )
    #         else:
    #             elements = self.safe_find_elements(By.TAG_NAME, selector, multiple=True)
    #             if elements:
    #                 logging.info(f"----------------ELEMENTS FOUND----------------")
    #                 return elements
    #             else:
    #                 logging.warning(
    #                     f"ELEMENTS {key} WITH SELECTOR {selector} WAS NOT FOUND"
    #                 )
