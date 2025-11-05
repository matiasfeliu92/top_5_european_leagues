from datetime import datetime, timedelta
import kaggle as kg
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import os
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
# from helpers.manage_db import ManageDB
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

BASE_DIR = os.getcwd()

def extract():
    kaggle_username = os.getenv("KAGGLE_USERNAME")
    kaggle_api_key = os.getenv("KAGGLE_KEY")
    if not kaggle_username or not kaggle_api_key:
        raise ValueError("Las variables de entorno KAGGLE_USERNAME o KAGGLE_KEY no están definidas.")
    os.environ['KAGGLE_USERNAME'] = kaggle_username
    os.environ['KAGGLE_KEY'] = kaggle_api_key
    api = KaggleApi()
    api.authenticate()
    print("Conexión a Kaggle exitosa.")
    api.dataset_download_files(
        dataset="prateekchauhands/football-data-top-5-european-leagues", 
        path='/tmp/', 
        unzip=True
    )
    df = pd.read_csv('/tmp/past-data.csv', encoding='ISO-8859-1')
    print(df.head())
    files_dir = os.path.join(BASE_DIR, "data", "raw")
    df.to_csv(os.path.join(files_dir, "top_5_european_leagues.csv"), index=False)

def load():
    print("NEXT STEP --> transform data")
    print("BASE_DIR: ", BASE_DIR)
    postgresql_DBT_host = os.getenv("POSTGRES_HOST_DBT")
    postgresql_DBT_user = os.getenv("POSTGRES_USER_DBT")
    postgresql_DBT_password = os.getenv("POSTGRES_PASSWORD_DBT")
    postgresql_DBT_db_name = os.getenv("POSTGRES_DB_DBT")
    print("HOST:", postgresql_DBT_host)
    print("USER:", postgresql_DBT_user)
    print("PASSWORD:", postgresql_DBT_password)
    print("DB:", postgresql_DBT_db_name)
    required_vars = {
        'POSTGRES_PORT_HOST': postgresql_DBT_host,
        'POSTGRES_USER_DBT': postgresql_DBT_user,
        'POSTGRES_PASSWORD_DBT': postgresql_DBT_password,
        'POSTGRES_DB_DBT': postgresql_DBT_db_name
    }
    for var_name, value in required_vars.items():
        if value is None:
            raise ValueError(f"La variable de entorno {var_name} no está definida.")
        os.environ[var_name] = value
    db_url = f"postgresql://{postgresql_DBT_user}:{postgresql_DBT_password}@{postgresql_DBT_host}:5432/{postgresql_DBT_db_name}"
    engine = create_engine(db_url)
    print("POSTGRESQL URL: ", engine.url)
    files_dir = os.path.join(BASE_DIR, "data", "raw")
    print("FILES_DIR: ", files_dir)
    files_list = os.listdir(files_dir)
    for file_ in files_list:
        print("FILE_NAME: ", file_)
        df = pd.read_csv(os.path.join(files_dir, file_), sep=",")
        df.index.name = "id"
        print(df.head())
        print(df.info())
        table_name = "Top5EuropeanLeagues"
        df.to_sql(table_name, con=engine, schema="raw_data", if_exists="replace", index=True)

with DAG(
    'Top5EuropeanLeagues_ETL',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime.now(),
    tags=['example'],
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    load_task = PythonOperator(task_id="load", python_callable=load)

    extract_task >> load_task
