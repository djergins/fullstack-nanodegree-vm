#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament") 


def deleteMatches():
    """Remove all the match records from the database."""
    pg = connect()
    c = pg.cursor()
    c.execute("delete from matches")
    pg.commit()
    pg.close()


def deletePlayers():
    """Remove all the player records from the database."""
    pg = connect()
    c = pg.cursor()
    c.execute("delete from players")
    pg.commit()
    pg.close()


def countPlayers():
    """Returns the number of players currently registered."""
    pg = connect()
    c = pg.cursor()
    c.execute("select count(name) from players")
    result = c.fetchall()[0][0]
    pg.close()
    return result

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    pg = connect()
    c = pg.cursor()
    query = "insert into players (name) values (%s)"
    c.execute(query, (name,))
    pg.commit()
    pg.close()

def countMatches():
    """Returns a list of matches. This is used to confirm 
    that our code is preventing rematches in the 
    testPreventRematches function.
    """
    pg = connect()
    c = pg.cursor()
    c.execute('select count(id) from matches')
    result = c.fetchall()[0][0]
    pg.close()
    return result

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
    players = countPlayers()
    if players % 2 == 0:
        pg = connect()
        c = pg.cursor()
        c.execute("select * from standings")
        result = c.fetchall()
        pg.commit()
        pg.close()

    else:
        registerPlayer('bye')
        pg = connect()
        c = pg.cursor()
        c.execute("select * from standings")
        result = c.fetchall()
        pg.commit()
        pg.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pg = connect()
    c = pg.cursor()
    query = "insert into matches (winner, loser) values (%s, %s)"
    try: 
        c.execute(query, (winner, loser,))
        pg.commit()

    except psycopg2.Error as e:
        pass
    pg.close() 
 
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
    
    pg = connect()
    c = pg.cursor()
    c.execute("select * from pairings")
    result = c.fetchall()
    pg.commit()
    pg.close()
    return result


