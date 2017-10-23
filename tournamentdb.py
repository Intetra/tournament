import psycopg2
import bleach


# get players
def GetPlayers():
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute('SELECT player_id, name FROM players ORDER BY player_id')
    players = [{'player id': str(row[0]), 'name': str(bleach.clean(row[1]))}
             for row in c.fetchall()]
    DB.close()
    return players


# get matches
def GetMatches():
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute('SELECT match_id, round, winner, player_one, player_two FROM matches ORDER BY match_id')
    matches = [{'match id': str(row[0]), 'round': str(row[1]), 'winner': str(row[2]),
    'player one': str(row[3]), 'player two': str(row[4])}
             for row in c.fetchall()]
    DB.close()
    return matches

#get tournaments
def GetTournaments():
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute('SELECT tournament_id, name FROM tournaments ORDER BY tournament_id')
    tournaments = [{'tournament id': str(row[0]), 'name': str(bleach.clean(row[1]))}
             for row in c.fetchall()]
    DB.close()
    return tournaments

#register a player
def reg_player(name):
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES ('%s');" % name)
    DB.commit()
    DB.close()
