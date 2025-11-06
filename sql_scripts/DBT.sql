SELECT COUNT(id) FROM raw_data."Top5EuropeanLeagues"

SELECT * FROM raw_data."Top5EuropeanLeagues" LIMIT 10;

WITH all_teams AS
(SELECT
	"HomeTeam" AS team
FROM
	raw_data."Top5EuropeanLeagues"
UNION ALL
SELECT
	"AwayTeam" AS team
FROM
	raw_data."Top5EuropeanLeagues")
SELECT
	DISTINCT
		"team"
FROM
	all_teams


------------------------------STAGING-------------------------------------------------------------------------------

-- models/staging/stg_football_data.sql

SELECT
	MD5(CAST("Date" AS TEXT) || "HomeTeam" || "AwayTeam") AS match_id_key,
	"Season" AS season,
	"Div" AS division,
	TO_DATE("Date", 'DD/MM/YY') AS match_date,
	COALESCE("Time", '15:00') AS kick_off_time, --HORA DE INICIO
	(TO_DATE("Date", 'DD/MM/YY') + (COALESCE("Time", '15:00') || ':00')::INTERVAL) AS match_timestamp,
	"HomeTeam" AS home_team,
	"AwayTeam" AS away_team,
	"FTHG" AS full_time_home_goals,
	"FTAG" AS full_time_away_goals,
	"FTR" AS full_time_result,
	COALESCE("HTHG", 0) AS half_time_home_goals,
	COALESCE("HTAG", 0) AS half_time_away_goals,
	COALESCE("HTR", 'Unknown') AS half_time_result,
	COALESCE("Referee", 'Unknown') AS referee,
	COALESCE("HS", 0) AS home_shots,
    COALESCE("AS", 0) AS away_shots,
	COALESCE("HST", 0) AS home_team_target_shots,
	COALESCE("AST", 0) AS away_team_target_shots,
	COALESCE("HF", 0) AS home_team_fouls_committed,
	COALESCE("AF", 0) AS away_team_fouls_committed,
	COALESCE("HC", 0) AS home_team_corners,
	COALESCE("AC", 0) AS away_team_corners,
	COALESCE("HY", 0) AS home_team_yellow_cards,
	COALESCE("AY", 0) AS away_team_yellow_cards,
	COALESCE("HR", 0) AS home_team_red_cards,
	COALESCE("AR", 0) AS away_team_red_cards
FROM
    raw_data."Top5EuropeanLeagues"
LIMIT 5

------------------------------INTERMEDIATE-------------------------------------------------------------------------------

WITH 
	home_teams AS (
		SELECT
			stg.match_id_key,
			stg.season,
			stg.division,
	        stg.match_date,
	        stg.match_timestamp,
			stg.home_team AS team_name,
	        stg.away_team AS opponent_name,
	        TRUE AS is_home_game,
			stg.full_time_home_goals AS goals_scored,
        	stg.full_time_away_goals AS goals_conceded,
			CASE
				WHEN stg.full_time_result = 'H' THEN 3
				WHEN stg.full_time_result = 'D' THEN 1
				ELSE 0
			END AS match_points,
			stg.home_shots AS shots_total,
	        stg.home_team_target_shots AS shots_on_target,
	        stg.home_team_corners AS corners,
	        stg.home_team_fouls_committed AS fouls_committed,
	        stg.home_team_yellow_cards AS yellow_cards,
	        stg.home_team_red_cards AS red_cards
		FROM 
			dbt.stg_football_data AS stg
		LIMIT 5
	),
	away_teams AS (
		SELECT
			stg.match_id_key,
			stg.season,
			stg.division,
	        stg.match_date,
			stg.match_timestamp,
			stg.away_team AS team_name,
	        stg.home_team AS opponent_name,
	        FALSE AS is_home_game,
        	stg.full_time_away_goals AS goals_scored,
			stg.full_time_home_goals AS goals_conceded,
			CASE
				WHEN stg.full_time_result = 'A' THEN 3
				WHEN stg.full_time_result = 'D' THEN 1
				ELSE 0
			END AS match_points,
			stg.away_shots AS shots_total,
	        stg.away_team_target_shots AS shots_on_target,
	        stg.away_team_corners AS corners,
	        stg.away_team_fouls_committed AS fouls_committed,
	        stg.away_team_yellow_cards AS yellow_cards,
	        stg.away_team_red_cards AS red_cards
		FROM 
			dbt.stg_football_data AS stg
		LIMIT 5
	)
SELECT * FROM home_teams
UNION ALL
SELECT * FROM away_teams

------------------------------INTERMEDIATE-------------------------------------------------------------------------------

SELECT 
	*, 
	SUM(match_points) OVER (
        PARTITION BY team_name, division, season
        ORDER BY match_timestamp -- Ordenar por fecha y hora
    ) AS cumulative_points 
FROM 
	dbt.int_team_match_performance