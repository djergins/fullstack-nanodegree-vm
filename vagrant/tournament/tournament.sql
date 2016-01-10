-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (
id serial primary key,
name text  
);

-- update matches to record tie games
create table matches (
id serial primary key,
winner integer  references players(id),
loser integer references players(id),
tie_player_1 integer references players(id),
tie_player_2 integer references players(id)
);

-- credit to babak for asking how to go about doing this on stack overflow.
-- https://discussions.udacity.com/t/how-to-prevent-rematches-between-players-without-using-python/38190
-- also have index acount for tie games
create unique index matches_unique_index 
	on matches (greatest(winner, loser, tie_player_1, tie_player_2), 
		least(winner, loser, tie_player_1, tie_player_2));

create view standings as
	-- select the first two columns as simply the id and name from players
	select p.id, p.name, 
	coalesce(w.wins, 0) as wins,
	coalesce(m.match, 0) as match
	from players p
	left join
	-- append column that counts wins for a player 
	(select winner, count(winner) as wins from
		matches
		group by winner) w
	on p.id = w.winner
	left join
	-- append column that counts matches for a player,
	-- including tie games. 
	(select m.winner, m.loser, m.tie_player_1,
	m.tie_player_2, count(p.id) as match from
	players p, matches m
	where p.id = m.winner or
	p.id = m.loser or
	p.id = m.tie_player_1 or
	p.id = m.tie_player_2
	group by p.id, m.winner, m.loser, m.tie_player_1, m.tie_player_2) m
	on p.id = m.winner
	or p.id = m.loser
	or p.id = m.tie_player_1
	or p.id = m.tie_player_2
	group by p.id,w.wins,m.match
	order by m.match - w.wins desc;

-- self join on standings to pair up players with matching records
create view pairings as
	select a.id as player_id_1, a.name as player_name_1,
	b.id as player_id_2, b.name as player_name_2
	from standings a, standings b
	where (a.match - a.wins) = (b.match - b.wins)
	and a.id < b.id


	


	






	
	 

