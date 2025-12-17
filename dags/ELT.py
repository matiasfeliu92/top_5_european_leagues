from datetime import datetime, timedelta
import os
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from src.scripts.extract import Extract
from src.scripts.scrapper import Scrapper

# load_dotenv()

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
    print("FIRST STEP --> extract data")
    scrapper = Scrapper()
    scrapper.extract_links()
    scrapper.save_links()

def load():
    print("NEXT STEP --> transform data")
    extract = Extract()
    extract.extract_files()
    

with DAG(
    'Top5EuropeanLeagues_ETL',
    default_args=default_args,
    description='This process was created, for extract, load and transform data of Top 5 European Leagues',
    schedule_interval=timedelta(days=1),
    start_date=datetime.now(),
    tags=['Football'],
) as dag:
    extract_data = PythonOperator(
        task_id="extract_data", 
        python_callable=extract
    )
    load_data = PythonOperator(
        task_id="load_data", 
        python_callable=load
    )
    transform_with_DBT = BashOperator(
        task_id="transform_with_DBT",
        bash_command="cd /opt/airflow/european_leagues_DBT && dbt run --select stg_football_data int_team_match_performance --profiles-dir /home/airflow/.dbt",
        dag=dag,
    )

    extract_data >> load_data ##>> transform_with_DBT
