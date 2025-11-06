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