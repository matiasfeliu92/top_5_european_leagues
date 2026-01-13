import dlt
from pyspark.sql.functions import col, lit, when, count, sum

@dlt.table(
    name="standings_unstacked_gold",
    comment="Desdoblamiento de partidos: una fila por equipo por partido para cálculos de posiciones."
)
def standings_unstacked_gold():
    # Leemos de la capa Silver
    silver_df = dlt.read("football_data_silver")
    # --- EQUIPOS LOCALES ---
    home_teams = silver_df.select(
        col("match_id_key"),
        col("season"),
        col("division"),
        col("match_date"),
        col("home_team").alias("team_name"),
        col("away_team").alias("opponent_name"),
        lit(True).alias("is_home_game"),
        col("full_time_home_goals").alias("goals_scored"),
        col("full_time_away_goals").alias("goals_conceded"),
        when(col("full_time_result") == "H", 3)
        .when(col("full_time_result") == "D", 1)
        .otherwise(0).alias("match_points"),
        col("home_shots").alias("shots_total"),
        col("home_team_target_shots").alias("shots_on_target"),
        col("home_team_corners").alias("corners"),
        col("home_team_fouls_committed").alias("fouls_committed"),
        col("home_team_yellow_cards").alias("yellow_cards"),
        col("home_team_red_cards").alias("red_cards")
    )
    # --- EQUIPOS VISITANTES ---
    away_teams = silver_df.select(
        col("match_id_key"),
        col("season"),
        col("division"),
        col("match_date"),
        col("away_team").alias("team_name"),
        col("home_team").alias("opponent_name"),
        lit(False).alias("is_home_game"),
        col("full_time_away_goals").alias("goals_scored"),
        col("full_time_home_goals").alias("goals_conceded"),
        when(col("full_time_result") == "A", 3)
        .when(col("full_time_result") == "D", 1)
        .otherwise(0).alias("match_points"),
        col("away_shots").alias("shots_total"),
        col("away_team_target_shots").alias("shots_on_target"),
        col("away_team_corners").alias("corners"),
        col("away_team_fouls_committed").alias("fouls_committed"),
        col("away_team_yellow_cards").alias("yellow_cards"),
        col("away_team_red_cards").alias("red_cards")
    )
    return home_teams.union(away_teams)

@dlt.table(
    name="team_stats_gold",
    comment="Agrupacion de sesion, division y team, para suma de partidos"
)
def team_stats_gold():
    # Leemos de la capa Silver
    standings_unstacked_gold = dlt.read("standings_unstacked_gold")
    team_stats_gold = standings_unstacked_gold.groupBy(
        col("season"),
        col("division"),
        col("team_name")
    ).agg(
        count("match_id_key").alias("GP"),
        sum("match_points").alias("PTS"), 
        sum("goals_scored").alias("GF"),
        sum("goals_conceded").alias("GA"),
        sum("shots_total").alias("ST"),
        sum("shots_on_target").alias("SOT"),
        sum("corners").alias("C"),
        sum("fouls_committed").alias("FC"),
        sum("yellow_cards").alias("YC"),
        sum("red_cards").alias("RC")
    ).withColumn("GD", col("GF") - col("GA"))
    return team_stats_gold