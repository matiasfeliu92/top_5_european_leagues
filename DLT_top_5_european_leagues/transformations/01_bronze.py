import dlt
from pyspark.sql.functions import col, lit
from functools import reduce

# Definición estricta de columnas para la tabla Bronze
TARGET_COLS = [
    "Season", "Div", "Date", "Time", "HomeTeam", "AwayTeam",
    "FTHG", "FTAG", "FTR", "HTHG", "HTAG", "HTR",
    "Referee", "HS", "AS", "HST", "AST",
    "HF", "AF", "HC", "AC",
    "HY", "AY", "HR", "AR",
    "tournament"
]

def normalize_column_names(df):
    """Limpia caracteres especiales como el BOM (ï»¿) de los encabezados."""
    for c in df.columns:
        clean = c.replace("ï»¿", "").strip()
        if c != clean:
            df = df.withColumnRenamed(c, clean)
    return df

@dlt.table(
    name="football_data_bronze",
    comment="Tabla unificada con todas las ligas y columnas estandarizadas."
)
def football_data_bronze():
    # 1. Obtener la lista de tablas a procesar dinámicamente
    patterns = [
        "championship", "conference", "league_1", "league_2",
        "premier_league", "serie_a", "serie_b",
        "la_liga_primera", "la_liga_segunda"
    ]
    
    sql_likes = " OR ".join([f"table_name LIKE '%{p}%'" for p in patterns])
    
    # Consultamos el information_schema para encontrar las tablas creadas por el scraper
    tables_df = spark.sql(f"""
        SELECT table_name 
        FROM workspace.information_schema.tables 
        WHERE table_schema = 'top_5_european_leagues'
        AND ({sql_likes})
    """).collect()

    if not tables_df:
        # Retorna un DataFrame vacío con el esquema correcto si no hay tablas
        return spark.createDataFrame([], schema=",".join([f"{c} STRING" for c in TARGET_COLS]))

    dfs = []
    for t in tables_df:
        full_name = f"top_5_european_leagues.{t.table_name}"
        df = spark.read.table(full_name)
        
        # Limpieza inicial de nombres de columnas
        df = normalize_column_names(df)
        
        # Estandarización de 'season' (algunas tablas pueden venir en minúscula)
        if "season" in df.columns and "Season" not in df.columns:
            df = df.withColumn("Season", col("season"))
            
        dfs.append(df)

    # 2. Unión de todas las tablas manejando columnas faltantes de forma automática
    # unionByName con allowMissingColumns=True rellena con NULL lo que no existe
    final_df = reduce(lambda a, b: a.unionByName(b, allowMissingColumns=True), dfs)

    # 3. Garantizar que existan todas las TARGET_COLS antes de la selección final
    # Si alguna columna de TARGET_COLS no existía en NINGUNA tabla, la creamos vacía
    for c in TARGET_COLS:
        if c not in final_df.columns:
            final_df = final_df.withColumn(c, lit(None).cast("string"))

    # 4. Selección final para asegurar el orden y las columnas exactas solicitadas
    return final_df.withColumn("Div", col("tournament")).select(*TARGET_COLS)