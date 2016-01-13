-- Table definitions for the tournament project. 
-- 
-- Put your SQL 'create table' statements in this file; also 'create view' 
-- statements if you choose to use it. 
-- 
-- You can write comments in this file by starting them with two dashes, like 
-- these lines here. 
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players 
  ( 
     id   SERIAL PRIMARY KEY, 
     name TEXT 
  ); 

-- update matches to record tie games 
CREATE TABLE matches 
  ( 
     id           SERIAL PRIMARY KEY, 
     winner       INTEGER REFERENCES players(id), 
     loser        INTEGER REFERENCES players(id), 
     tie_player_1 INTEGER REFERENCES players(id), 
     tie_player_2 INTEGER REFERENCES players(id) 
  ); 

-- credit to babak for asking how to go about doing this on stack overflow. 
-- https://discussions.udacity.com/t/how-to-prevent-rematches-between-players-without-using-python/38190 
-- also have index acount for tie games 
CREATE UNIQUE INDEX matches_unique_index 
  ON matches (Greatest(winner, loser, tie_player_1, tie_player_2), 
Least(winner, loser, tie_player_1, tie_player_2)); 

CREATE VIEW standings AS 
  -- select the first two columns as simply the id and name from players 
  SELECT p.id, 
         p.name, 
         Coalesce(w.wins, 0)  AS wins, 
         Coalesce(m.match, 0) AS match,
         row_number() over (order by wins) as rank
  FROM   players p 
         left join 
         -- append column that counts wins for a player  
         (SELECT winner, 
                 Count(winner) AS wins 
          FROM   matches 
          GROUP  BY winner) w 
                ON p.id = w.winner 
         left join 
         -- append column that counts matches for a player, 
         -- including tie games.  
         (SELECT m.winner, 
                 m.loser, 
                 m.tie_player_1, 
                 m.tie_player_2, 
                 Count(p.id) AS match 
          FROM   players p, 
                 matches m 
          WHERE  p.id = m.winner 
                  OR p.id = m.loser 
                  OR p.id = m.tie_player_1 
                  OR p.id = m.tie_player_2 
          GROUP  BY p.id, 
                    m.winner, 
                    m.loser, 
                    m.tie_player_1, 
                    m.tie_player_2) m 
                ON p.id = m.winner 
                    OR p.id = m.loser 
                    OR p.id = m.tie_player_1 
                    OR p.id = m.tie_player_2 
  GROUP  BY p.id, 
            w.wins, 
            m.match
  ORDER BY wins desc;  


CREATE VIEW pairings AS
	SELECT a.id AS player_id_1, a.name AS player_name_1, 
	b.id AS player_id_2, b.name AS player_name_2
	FROM (SELECT id, name, rank,
		row_number() OVER (ORDER BY rank) AS row
		FROM standings
		WHERE rank % 2 = 1
		ORDER BY row) AS a
	FULL OUTER JOIN
	(SELECT id, name, rank,
		row_number() OVER (ORDER BY rank) AS row
		FROM standings
		WHERE rank % 2 = 0
		ORDER BY row) AS b
	ON a.row = b.row
	AND a.id <> b.id;
	



	



         
