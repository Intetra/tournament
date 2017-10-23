import psycopg2
import bleach


# get players
def playerStandings():
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute('SELECT player_id, name, wins, matches FROM players ORDER BY wins DESC, player_id DESC')
    players = [{'player id': str(row[0]), 'name': str(bleach.clean(row[1])), 'wins': str(row[2]), 'matches': str(row[3])}
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
    c.execute("INSERT INTO players (name, wins, matches) VALUES ('%s', 0, 0);" % name)
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
    print w
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
    pairs = []
    c.execute('SELECT player_id, name FROM players ORDER BY wins DESC, player_id DESC')
    players = [{'player id': str(row[0]), 'name': str(bleach.clean(row[1]))}
             for row in c.fetchall()]
    for x in players:
        print x;

    DB.close()
    return players

    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
