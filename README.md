Tournament
=============

Common code for the Relational Databases and Full Stack Fundamentals courses

BEFORE RUNNING: You must generate the schema for the database in tournament.sql. To do this:
type "psql",
type "\i tournament.sql"

To run this project, i.e., validate that the python code passes the requirements for the course,
type, "python tournament_test.py" and validate that all tests pass up  to "Success! All tests pass!"

I attempted extra credit by the following:

Prevent rematches: This was done by adding a unique index on the matches table to prevent both combinations
of players from facing one another again in a tournament.

Allow for a bye: This is done via a function, insertBye(), it counts the players in a tournament when called,
if the count is odd, then it registers a "bye" player. Rematches against the bye player will not happen thanks
to the unique index added to the matches player. 

Allow for tie games: This is done by adding tie_player_1 and tie_player_2 to the matches table on the sql end.
On the api side, I modified all function parameters to default to None so that it can handle winner and loser
being none and the tie fields being passed id's. This also allows for tie_player_1 and tie_player_2 not
being passed any values. 

As is currently set, all of the original tests pass.

I wrote the following tests to test for extra credit items:

testPreventRematches()
testRoundBye()
testDrawMatch()

The goal is to do this well and to exceeds specifications. I look forward to and welcome any feedback! :)
