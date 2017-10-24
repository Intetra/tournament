-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players ( player_id serial primary key,
  name text, wins int, matches int );

create table matches (
  match_id serial primary key,
  round int,
  winner serial references players(player_id),
  player_one serial references players(player_id),
  player_two serial references players(player_id));
