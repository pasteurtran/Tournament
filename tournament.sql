-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop dat database if it exists!
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament

-- Create table containing player data: name and key.
CREATE TABLE players
(
	id serial PRIMARY KEY,
	name TEXT
);

-- Create a match table which holds the pairings,
-- the player match as a unique data
-- adding in delete cacade (corresponding data is removed!)
CREATE TABLE match_pairings
(
	id serial PRIMARY KEY,
	winner int REFERENCES players(id) ON DELETE CASCADE,
	loser int REFERENCES players(id) ON DELETE CASCADE
);

-- Create a View to find the number of matches each player plays.
-- Select the players, find the winner in the match pairings,
-- then join and group by the player id
CREATE VIEW m_wins AS (
	SELECT 
		players.id,
		players.name,
		COUNT(match_pairings.winner) AS wins
	FROM 
		match_pairings
	RIGHT JOIN
		players ON match_pairings.winner = players.id
	GROUP BY
		players.id
	ORDER BY
		wins desc
);

-- As with the above view, arrange and sort based on losing games.
CREATE VIEW m_loses AS(
	SELECT
		players.id,
		players.name,
		COUNT(match_pairings.loser) AS loses
	FROM
		match_pairings
	RIGHT JOIN
		players ON match_pairings.loser = players.id
	GROUP BY
		players.id
	ORDER BY
		loses desc

);

-- Based primarily on wins
-- so we can arrange them on the amoutn of wins using m_wins
-- Give total of matchtes
CREATE VIEW standings AS(
	SELECT 
		m_wins.id,
		m_wins.name,
		m_wins.wins,
		m_loses.loses + m_wins.wins as matches_played,
		m_loses.loses
	FROM 
		m_wins, m_loses
	WHERE
		m_wins.id = m_loses.id
	ORDER BY 
		m_wins.wins DESC

);
