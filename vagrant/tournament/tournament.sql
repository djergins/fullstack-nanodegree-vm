-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (
id serial primary key,
name text,
wins integer default 0,
matches integer default 0  
);

create table matches (
id serial primary key,
winner_id integer references players(id),
loser_id integer references players(id)
);

