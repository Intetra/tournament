import psycopg2
import bleach
from operator import itemgetter

# get players
def playerStandings():
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute('SELECT player_id, name, wins, matches FROM players ORDER BY wins DESC, player_id DESC')
    players = [{'Player id': str(row[0]), 'Name': str(bleach.clean(row[1])), 'Wins': str(row[2]), 'Matches': str(row[3])}
             for row in c.fetchall()]
    l = 0
    for x in players:
        y = ((str(x.keys()[3]) + ': ' +  str(x.values()[3])),
             (str(x.keys()[2]) + ': ' +  str(x.values()[2])),
             (str(x.keys()[1]) + ': ' +  str(x.values()[1])),
             (str(x.keys()[0]) + ': ' +  str(x.values()[0])))
        players[l] = y
        l+=1
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
    l = 0
    for x in matches:
        y = ((str(x.keys()[3]) + ': ' +  str(x.values()[3])),
             (str(x.keys()[1]) + ': ' +  str(x.values()[1])),
             (str(x.keys()[4]) + ': ' +  str(x.values()[4])),
             (str(x.keys()[0]) + ': ' +  str(x.values()[0])),
             (str(x.keys()[2]) + ': ' +  str(x.values()[2])))
        matches[l] = y
        l+=1
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
    c.execute("INSERT INTO players (name, wins, matches) VALUES ('%s', 0, 0);" % bleach.clean(name))
    DB.commit()
    DB.close()

#delete all matches
def del_all_matches():
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM matches cascade;")
    DB.commit()
    DB.close()

def del_all_players():
    del_all_matches()
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM players cascade;")
    DB.commit()
    DB.close()

def rep_match(r, p1, p2, w):
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO matches (round, player_one, player_two, winner) VALUES (%s, %s, %s, %s);" % (r, p1, p2, w))
    c.execute("UPDATE players SET wins = wins + 1 WHERE player_id = %s;" % w)
    c.execute("UPDATE players SET matches = matches + 1 WHERE player_id = %s OR player_id = %s;" % (p1, p2))
    DB.commit()
    DB.close()

def countPlayers():
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT COUNT(player_id) FROM players;")
    x = c.fetchone()
    return x[0]

def swissPairings():
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute('SELECT player_id, name FROM players ORDER BY wins DESC, player_id DESC')
    players = [{'player id': str(row[0]), 'name': str(bleach.clean(row[1]))}
             for row in c.fetchall()]
    n = 2
    x = [players[i:i+n] for i in range(0, len(players), n)]
    for y in x:
        if len(y) % 2 != 0:
            return x
    l = 0
    for y in x:
        x[l] = (y[0].values()[1], y[0].values()[0], y[1].values()[1], y[1].values()[0])
        l+=1
    DB.close()
    return x
