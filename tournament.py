#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM match_pairings")
    DB.commit()
    DB.close()
    """Remove all the match records from the database."""
    print "All matches have been deleted"


def deletePlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()
    """Remove all the player records from the database."""
    print "All Player data has been deleted"


# UP TO HERE
def countPlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM players")
    row = c.fetchone()
    DB.commit()
    DB.close()
    print row[0]
    return row[0]
    """Returns the number of players currently registered."""


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name, ))
    DB.commit()
    DB.close()
    print "inserted player into database"


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM standings")
    playerRanks = [(row[0], row[1],
                   row[2], row[3]) for row in c.fetchall()]
    DB.commit()
    DB.close()
    return playerRanks


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO match_pairings (winner,loser) VALUES (%s,%s)",
              (winner, loser))
    DB.commit()
    DB.close()


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
    standings = playerStandings()
    numOfPlayers = len(standings)
    if (numOfPlayers % 2 != 0):
        numOfPlayers -= 1
        playerHasBye = (standings[-1][0], standings[-1][1])
        print "Player has bye: " + playerHasBye

    i = 0
    listOfPairs = []
    while i < numOfPlayers:
        firstPlayer_id = standings[i][0]
        firstPlayer_name = standings[i][1]
        secondPlayer_id = standings[i+1][0]
        secondPlayer_name = standings[i+1][1]
        pairing = (firstPlayer_id, firstPlayer_name,
                   secondPlayer_id, secondPlayer_name)
        listOfPairs.append(pairing)
        i += 2
    return listOfPairs
