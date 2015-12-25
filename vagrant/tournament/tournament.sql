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

create table matches (
id serial primary key,
winner integer references players(id),
loser integer references players(id)
);


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
	-- append column that counts matches for a player
	(select m.winner, m.loser, count(p.id) as match from
	players p, matches m
	where p.id = m.winner or
	p.id = m.loser
	group by p.id, m.winner, m.loser) m
	on p.id = m.winner
	or p.id = m.loser
	group by p.id,w.wins,m.match;

create view pairings as
	select a.id as player_id_1, a.name as player_name_1,
	b.id as player_id_2, b.name as player_name_2
	from standings a, standings b
	where a.wins = b.wins
	and a.id < b.id


	
	 

