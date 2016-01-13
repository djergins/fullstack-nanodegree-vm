#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in "
                         "playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names "
                         "should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players "
    "appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should "
                             "have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testPreventRematches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Goku")
    registerPlayer("Vegeta")
    registerPlayer("Krillin")
    registerPlayer("Piccolo")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    # try different combinations to make sure the
    # the rematch is prevented regardless of order.
    reportMatch(id2, id1)
    reportMatch(id4, id3)
    c = countMatches()
    if c != 2:
        raise ValueError(
            "Players should not be able to face each other again.")
    print "9. Players face each other only once in a tournament."


def testRoundBye():
    deleteMatches()
    deletePlayers()
    # Register an odd number of players for a tournament
    registerPlayer("Cyclops")
    registerPlayer("Magneto")
    registerPlayer("Wolverine")
    registerPlayer("Juggernaut")
    registerPlayer("Rogue")
    insertBye()
    # Standings will round out odd numbers of players
    # to even by registering a 'bye' player.
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    # due to the unique constraint preventing rematches
    # players cannot rematch the 'bye'.
    reportMatch(id5, id6)
    c = countMatches()
    if c != 3:
        raise ValueError(
            "Players should not be able to face the bye more than once.")
    print "10. Rounds with an odd number of players support a bye."


def testDrawMatch():
    deleteMatches()
    deletePlayers()
    registerPlayer("Unstoppable")
    registerPlayer("Force")
    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]
    reportMatch(None, None, id1, id2)
    db, cursor = connect()
    cursor.execute("SELECT SUM(wins) FROM standings")
    result = cursor.fetchone()[0]
    if result > 0:
        raise ValueError(
            "Tie games should not result in a win.")
    cursor.execute("SELECT SUM(match) FROM standings")
    result2 = cursor.fetchone()[0]
    if result2 != 2:
        raise ValueError(
            "Tie games should still update the number of matches.")
    print "11. Draw games are possible in matches."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testPreventRematches()
    testRoundBye()
    testDrawMatch()
    print "Success!  All tests pass!"
