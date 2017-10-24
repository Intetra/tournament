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
      h1 { text-align: center; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
		 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>Tournament</h1>
    <h3>Players - %s</h3>
    <form method=post action="/registerPlayer">
      <div><textarea id="newPlayerName" name="newPlayerName" placeholder="name"></textarea></div>
      <div><button id="go" type="submit">Register Player</button></div>
      %s
<br>
    </form>
        <form method=post action="/deletePlayers">
          <div><button id="go" type="submit">delete all players</button></div>
        </form>
    <h3>Matches</h3>
    <form method=post action="/reportMatch">
    <div><textarea id="round" name="round" placeholder="Round #"></textarea></div>
    <div><textarea id="playerOne" name="playerOne" placeholder="Player One ID"></textarea></div>
      <div><textarea id="playerTwo" name="playerTwo" placeholder="Player Two ID"></textarea></div>
      <div><textarea id="winner" name="winner" placeholder="Winner ID"></textarea></div>
      <div><button type="submit">Report Match</button></div>
    </form>
    %s
    <br>
    <form method=post action="/deleteMatches">
      <div><button id="go" type="submit">delete all matches</button></div>
    </form>
    <br>
    <br>
    <h3>Pairs</h3>
    <form method=post action="/makePairs">
      <div><button id="go" type="submit">Make Pairs</button></div>
    </form>
    <hr>
    %s
  </body>
</html>
'''

HOLDER = '''\
    <div class=player><br>%s</div>
'''

def connect():
    return psycopg2.connect("dbname=tournament")

def Front(env, resp):
    players = tdb.playerStandings()
    matches = tdb.GetMatches()
    playerCount = tdb.countPlayers()
    pairs = tdb.swissPairings()
    # send results
    headers = [('Content-type', 'text/html')]
    resp('200 OK', headers)
    return [HTML_WRAP % (playerCount,
                        ''.join(HOLDER % (str(p) + '<hr>') for p in players),
                        ''.join(HOLDER % (str(m) + '<hr>') for m in matches),
                        ''.join(str(p2) + '<hr>' for p2 in pairs))]

def deleteMatches(env, resp):
        tdb.del_all_matches()
        headers = [('Location', '/'),
                   ('Content-type', 'text/plain')]
        resp('302 REDIRECT', headers)
        return ['Redirecting']



def deletePlayers(env, resp):
    tdb.del_all_players()
    headers = [('Location', '/'),
               ('Content-type', 'text/plain')]
    resp('302 REDIRECT', headers)
    return ['Redirecting']


def registerPlayer(env, resp):
        input = env['wsgi.input']
        length = int(env.get('CONTENT_LENGTH', 0))
        # If length is zero, post is empty - don't save it.
        if length > 14:
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


def reportMatch(env, resp):
    input = env['wsgi.input']
    length = int(env.get('CONTENT_LENGTH', 0))
    # If length is zero, post is empty - don't save it.
    if length > 36:
        postdata = input.read(length)
        fields = cgi.parse_qs(postdata)
        matchRound = fields['round'][0]
        p1 = fields['playerOne'][0]
        p2 = fields['playerTwo'][0]
        winner = fields['winner'][0]
        # If the post is just whitespace, don't save it.
        matchRound = matchRound.strip()
        p1 = p1.strip()
        p2 = p2.strip()
        winner = winner.strip()
        if winner and p1 and p2 and matchRound:
            # Save it in the database
            tdb.rep_match(matchRound, p1, p2, winner)
    # 302 redirect back to the main page
    headers = [('Location', '/'),
               ('Content-type', 'text/plain')]
    resp('302 REDIRECT', headers)
    return ['Redirecting']


def makePairs(env, resp):
    tdb.swissPairings()
    headers = [('Location', '/'),
               ('Content-type', 'text/plain')]
    resp('302 REDIRECT', headers)
    return ['Redirecting']

## Dispatch table - maps URL prefixes to request handlers
DISPATCH = {'': Front,
            'registerPlayer': registerPlayer,
            'deleteMatches': deleteMatches,
            'deletePlayers': deletePlayers,
            'reportMatch': reportMatch,
            'makePairs': makePairs}

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
