Tournament Swiss Matcher

What is it?
----------

The project is Tournament Swiss - It is to pair a group of people in a tournament to 
determine the winner in a Swiss styled Tournament.

Latest Version
--------------

Version 1.0
Uploaded and cleaned folder. Not fully Udacious.. yet. 


Files
-----
The following are the key files:
- README
- tournament.py
- tournament.sql
- tournament_test.py


Code Snippet
------------
-- Create table containing player data: name and key.
CREATE TABLE players
(
	id serial PRIMARY KEY,
	name TEXT
);

-- Create a match table which holds the pairings,
-- the player match as a unique data
-- adding in delete cacade (corresponding data is removed!)
CREATE TABLE match_pairings
(
	id serial PRIMARY KEY,
	winner int REFERENCES players(id) ON DELETE CASCADE,
	loser int REFERENCES players(id) ON DELETE CASCADE
);

Running the program
-------------------
1. Ensure you have Vagrant and a VM set up - this was tested with Oracle VM VirtualBox
2. Under your chosen command line - run PSQL 
3. Run \i tournament.sql while in PSQL loading the tournament data.
4. \q to exit PSQL and return to command line.
5. Run python tournament_test.py
