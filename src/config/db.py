import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from psycopg2 import sql, OperationalError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class ManageDB:
    def create_engine(cls, __conn_string__):
        try:
            cls.engine = create_engine(__conn_string__)
            with cls.engine.connect() as connection:
                print("CONNECTION ESTABISH SUCCESSFULLY")
            return cls.engine
        except SQLAlchemyError as e:
            print("THERE WAS AN ERROR WITH CONNECTION \n", str(e))

    def create_connection(cls, __conn_string_for_cursor__):
        try:
            conn = psycopg2.connect(__conn_string_for_cursor__)
            conn.autocommit = True
            print("CONNECTION ESTABISH SUCCESSFULLY")
            return conn
        except psycopg2.Error as ex:
            print(f"Error al conectar: {ex}")

    def create_database(cls, __conn__, __db_name__):
        try:
            with __conn__.cursor() as cur:
                cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [__db_name__])
                if cur.fetchone():
                    print(f"ℹ️ La base de datos '{__db_name__}' ya existe.")
                else:
                    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(__db_name__)))
                    print(f"✅ Base de datos '{__db_name__}' creada correctamente.")
        except Exception as e:
            print(f"❌ Error al crear la base de datos: {e}")

    def create_schema(cls, __conn__, __schema_name__):
        try:
            with __conn__.cursor() as cur:             
                cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(__schema_name__)))
                print(f"✅ Nuevo schema '{__schema_name__}' creado correctamente.")
        except Exception as e:
            print(f"❌ Error al crear el schema: {e}")
