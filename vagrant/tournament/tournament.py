#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("SELECT COUNT(name) FROM players")
    result = cursor.fetchone()[0]
    db.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "INSERT INTO players (name) VALUES (%s)"
    cursor.execute(query, (name,))
    db.commit()
    db.close()


def countMatches():
    """Returns a list of matches. This is used to confirm
    that our code is preventing rematches in the
    testPreventRematches function.
    """
    db, cursor = connect()
    cursor.execute('SELECT COUNT(id) FROM matches')
    result = cursor.fetchone()[0]
    db.close()
    return result


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should
    be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    cursor.execute("SELECT id, name, wins, match FROM standings")
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result


def reportMatch(winner, loser,
                tie_player_1=None, tie_player_2=None):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Get the id of the bye player if there is one.
    bye = selectBye()
    if tie_player_1 is not None or tie_player_2 is not None:
        db, cursor = connect()
        query = "INSERT INTO matches (tie_player_1, tie_player_2) " \
                " VALUES (%s, %s)"
        try:
            cursor.execute(query, (tie_player_1, tie_player_2,))
            db.commit()

        except psycopg2.Error as e:
            pass
        db.close()
    # If the bye player is present, set them to winner and
    # set the loser to the winner.
    if winner == bye:
        winner = loser
        loser = bye
    db, cursor = connect()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    try:
        cursor.execute(query, (winner, loser,))
        db.commit()

    except psycopg2.Error as e:
        pass
    db.close()


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
    db, cursor = connect()
    cursor.execute("SELECT * FROM pairings")
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result


def insertBye():
    """Inserts a 'bye' in to the tournament if there is an odd
    number of players."""
    c = countPlayers()
    if c % 2 != 0:
        registerPlayer("bye")
    else:
        print("No bye is neccessary at this time.")


def selectBye():
    """Returns the id of the bye player."""
    db, cursor = connect()
    cursor.execute("SELECT id FROM players WHERE name=\'bye\'")
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result
