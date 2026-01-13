import dlt
from pyspark.sql.functions import col, md5, concat, coalesce, lit, to_date, expr

@dlt.table(
    name="football_data_silver",
    comment="Capa Silver: Datos limpios, tipados y con nombres descriptivos."
)
@dlt.expect("valid_match_id", "match_id_key IS NOT NULL")
@dlt.expect_or_drop("positive_goals", "full_time_home_goals >= 0 AND full_time_away_goals >= 0")
def football_data_silver():
    # Leemos de tu tabla Bronze unificada
    bronze_df = dlt.read("football_data_bronze")
    
    return (
        bronze_df.select(
            # Generación de match_id_key (MD5)
            md5(concat(col("Date"), col("HomeTeam"), col("AwayTeam"))).alias("match_id_key"),
            
            col("Season").alias("season"),
            col("Div").alias("division"),
            
            # Conversión de tipos
            to_date(col("Date"), "dd/MM/yyyy").alias("match_date"),
            coalesce(col("Time"), lit("15:00")).alias("kick_off_time"),
            
            # Nombres descriptivos y casteo numérico
            col("HomeTeam").alias("home_team"),
            col("AwayTeam").alias("away_team"),
            col("FTHG").cast("int").alias("full_time_home_goals"),
            col("FTAG").cast("int").alias("full_time_away_goals"),
            col("FTR").alias("full_time_result"),
            
            # Manejo de nulos (COALESCE)
            coalesce(col("HTHG").cast("int"), lit(0)).alias("half_time_home_goals"),
            coalesce(col("HTAG").cast("int"), lit(0)).alias("half_time_away_goals"),
            coalesce(col("HTR"), lit("Unknown")).alias("half_time_result"),
            coalesce(col("Referee"), lit("Unknown")).alias("referee"),
            
            # Estadísticas del partido
            coalesce(col("HS").cast("int"), lit(0)).alias("home_shots"),
            coalesce(col("AS").cast("int"), lit(0)).alias("away_shots"),
            coalesce(col("HST").cast("int"), lit(0)).alias("home_team_target_shots"),
            coalesce(col("AST").cast("int"), lit(0)).alias("away_team_target_shots"),
            coalesce(col("HF").cast("int"), lit(0)).alias("home_team_fouls_committed"),
            coalesce(col("AF").cast("int"), lit(0)).alias("away_team_fouls_committed"),
            coalesce(col("HC").cast("int"), lit(0)).alias("home_team_corners"),
            coalesce(col("AC").cast("int"), lit(0)).alias("away_team_corners"),
            coalesce(col("HY").cast("int"), lit(0)).alias("home_team_yellow_cards"),
            coalesce(col("AY").cast("int"), lit(0)).alias("away_team_yellow_cards"),
            coalesce(col("HR").cast("int"), lit(0)).alias("home_team_red_cards"),
            coalesce(col("AR").cast("int"), lit(0)).alias("away_team_red_cards")
        )
    )