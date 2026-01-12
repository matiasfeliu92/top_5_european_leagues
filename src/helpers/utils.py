from io import StringIO
import pandas as pd
import logging
import requests
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Utils:
    def season_is_after(cls, season_str: str, min_year: int) -> bool:
        years = list(map(int, re.findall(r"\d{4}", season_str)))
        return len(years) == 2 and years[0] > min_year and years[1] > min_year

    def read_csv_files(cls, __link__):
        try:
            r = requests.get(__link__, timeout=10)
            r.raise_for_status()
            csv_buffer = StringIO(r.text)
            df = pd.read_csv(csv_buffer, encoding='cp1252')
            return df
        except requests.exceptions.RequestException as e:
                logging.warning(f"Error de red o descarga para {__link__}: {e}")
                return None
        except pd.errors.ParserError as e:
            logging.warning(f"Error de formato CSV para {__link__}: {e}")
            try:
                csv_buffer.seek(0)
                df = pd.read_csv(csv_buffer, encoding='latin-1')
                return df
            except pd.errors.ParserError as e_alt:
                logging.error(f"Fallo el encoding alternativo (latin-1) para {__link__}. Error: {e_alt}")
                return None
        except UnicodeDecodeError as e:
            logging.warning(f"Error de decodificación de caracteres para {__link__}: {e}")
            return None
        except Exception as e:
            logging.error(f"Error inesperado al procesar {__link__}: {e}")
            return None

    def rename_columns(cls, __df__: pd.DataFrame, __columns_to_rename__: dict, __input_col__=None, __output_col__=None):
        logging.warning("ANTES DE RENOMBRAR COLUMNAS")
        logging.info(__df__.columns)
        logging.info(__df__.head())
        logging.info(f"COLUMNS TO RENAME - INPUT COLUMNS: {__columns_to_rename__.keys()}")
        if set(__columns_to_rename__).issubset(__df__.columns):
            df_renamed = __df__.rename(columns=__columns_to_rename__)
            logging.info(f"SE RENOMBRARON ESTAS COLUMNAS: {set(__columns_to_rename__)}")
            logging.info(df_renamed.columns)
            logging.info(df_renamed.head())
            return df_renamed
        else:
            logging.warning("NO SE RENOMBRO NINGUNA COLUMNA")
            return __df__