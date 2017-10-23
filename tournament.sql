-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table tournaments (
  tournament_id serial primary key,
  name text
);
insert into tournaments (name) values ('first');

create table players ( player_id serial primary key,
  name text, wins int, matches int );

insert into players (name, wins, matches) values ('aubrey', 0, 0);
insert into players (name, wins, matches) values ('bob', 0, 0);

create table matches (
  match_id serial primary key,
  tournament serial references tournaments(tournament_id),
  round int,
  winner serial references players(player_id),
  player_one serial references players(player_id),
  player_two serial references players(player_id));

insert into matches (tournament, round, winner, player_one, player_two) values (1, 1, 1, 1, 2);
