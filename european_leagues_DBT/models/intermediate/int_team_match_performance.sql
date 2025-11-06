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
			{{ ref('stg_football_data') }} AS stg
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
			{{ ref('stg_football_data') }} AS stg
	)
SELECT * FROM home_teams
UNION ALL
SELECT * FROM away_teams