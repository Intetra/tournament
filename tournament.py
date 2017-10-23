#!/usr/bin/env python
from wsgiref.simple_server import make_server
import tournamentdb as tdb
from wsgiref import util
import psycopg2
import cgi

HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Tournament</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
		 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>Tournament</h1>
    <h3>Players</h3>
%s
<form method=post action="/registerPlayer">
  <div><textarea id="newPlayerName" name="newPlayerName"></textarea></div>
  <div><button id="go" type="submit">Register Player</button></div>
</form>
    <h3>Matches</h3>
%s
<h3>Tournaments</h3>
%s
  </body>
</html>
'''

PLAYER = '''\
    <div class=player><br>%s</div>
'''

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def Front(env, resp):
    '''View is the 'main page' of the forum.

    It displays the submission form and the previously posted messages.
    '''
    # get posts from database
    players = tdb.GetPlayers()
    matches = tdb.GetMatches()
    tournaments = tdb.GetTournaments()
    # send results
    headers = [('Content-type', 'text/html')]
    resp('200 OK', headers)
    return [HTML_WRAP % (''.join(PLAYER % p for p in players), matches, tournaments)]

def deleteMatches():
    """Remove all the match records from the database."""


def deletePlayers():
    """Remove all the player records from the database."""


def countPlayers():
    """Returns the number of players currently registered."""


def registerPlayer(env, resp):
        input = env['wsgi.input']
        length = int(env.get('CONTENT_LENGTH', 0))
        # If length is zero, post is empty - don't save it.
        if length > 0:
            postdata = input.read(length)
            fields = cgi.parse_qs(postdata)
            content = fields['newPlayerName'][0]
            # If the post is just whitespace, don't save it.
            content = content.strip()
            if content:
                # Save it in the database
                tdb.reg_player(content)
        # 302 redirect back to the main page
        headers = [('Location', '/'),
                   ('Content-type', 'text/plain')]
        resp('302 REDIRECT', headers)
        return ['Redirecting']


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """


def swissPairings():
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

## Dispatch table - maps URL prefixes to request handlers
DISPATCH = {'': Front,
            'registerPlayer': registerPlayer}

## Dispatcher forwards requests according to the DISPATCH table.
def Dispatcher(env, resp):
    '''Send requests to handlers based on the first path component.'''
    page = util.shift_path_info(env)
    if page in DISPATCH:
        return DISPATCH[page](env, resp)
    else:
        status = '404 Not Found'
        headers = [('Content-type', 'text/plain')]
        resp(status, headers)
        return ['Not Found: ' + page]


# Run this bad server only on localhost!
httpd = make_server('', 8000, Dispatcher)
print("Serving HTTP on port 8000...")
httpd.serve_forever()
