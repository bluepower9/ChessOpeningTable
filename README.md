# CPSC 531 Chess Opening Table Project

### By: Jarrod Leong

## ABOUT
Welcome to my chess opening table big data project!  Here you will be able to populate a MongoDB with chess games using pymongo and you will be able to access it via a webservice
created with flask. The mainpage can be found on localhost:5000 where you can input a board position to generate the opening table. The website uses lichess embedded into it to 
display the current position. You will be able to cycle through the moves by clicking on them to quickly navigate through the opening table.  The table will show the number of games
each move has been played as well as the win and draw percentages for the position. 


## REQUIREMENTS
#### - requires python 3 (developed on 3.10)
#### - dependencies can be found in requirements.txt
#### - must have MongDB Community version installed and running.  Program will hang if it is not running
#### - visit https://database.lichess.org/ to download a .pgn file of games. *you may want to find a small file as it will be decompressed and increase in size dramatically*

---

## Setting Up and Populating Database
#### - create a database in MongoDB (ex. 'chess')
#### - create a collection in the database you just created (ex. 'games')
#### - navigate to /src and run `python3 setupDB.py -f <pgn filepath: required> -d <database name> -c <collection name: default> -g <max number of games>`
####        -only the filepath is required. the database name will default to `chess` collection will default to `games` and the number of games will default to `100000`
##### *It will take a long time to add all the games.  In the meantime, you can still run the program and test it*

---

## Running Website and Service and How to Use
#### - the project is entirely using Flask so to run, you only need to start `python3 app.py`
#### - navigate to localhost:5000 to view homepage and follow instructions.  To get a FEN, you can navigate to https://lichess.org/analysis and get the FEN from the bottom.
#### - on the analysis page, it displays the top 5 moves on the right as well as the parameters you searched for on top.
#### - Click on any of the moves on the right to play the move and view the statistics for that position. If you want to restart, click "Opening Table" at the top.