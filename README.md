# CPSC 531 Chess Opening Table Project

### By: Jarrod Leong

## About
Welcome to my chess opening table big data project!  Here you will be able to populate a MongoDB with chess games using pymongo and you will be able to access it via a webservice
created with flask. The mainpage can be found on localhost:5000 where you can input a board position to generate the opening table. The website uses lichess embedded into it to 
display the current position. You will be able to cycle through the moves by clicking on them to quickly navigate through the opening table.  The table will show the number of games
each move has been played as well as the win and draw percentages for the position. The program performs realtime analysis of the data in the database to aggregate the different positions and get the requested games with the selected parameters. White the project may look simple, it took a lot of effort to understand MongoDB and the best way to store, extract, and view the chess games. Setting up a large database takes a very long time (hours) because it has to play through each game. A lot of effort went into refining database document configuration, indexes as well as the aggregation pipeline because the service needs to be run in realtime and perform realtime analysis.  

---

## Functionalities
My project has a few different functionalities:
#### - populate database given a PGN file
#### - query and perform realtime analysis of data in database
#### - get results and view it from a webpage (localhost:5000)

My project provides a script to read a given PGN file and will populate a database with the games.  The application will perform realtime analysis of the data in the database when a specific game state is requested.  This data will be shown on a webpage along with a board that shows the current game state. 

---

## Architecture and Design
For my project, I decided to make a simple website application that allows a user to input a chess position and some parameters including the elo and format the user wants to search
for.  The application is built using Python and Flask for the API.  The api is simple, yet effective for its purposes.  I am using Flask templates which runs using Jinja that allowed me to create simple yet dynamic webpages for the opening table. My api has 2 endpoints: the homepage and /analysis which analyzes a given position and parameters and returns the results of the opening table. The analysis webpage allows a user to click on any of the moves on the right to quickly navigate to the next chess position.  A board is shown on the left that allows a user to visualize the position. The board is generated from https://lichess.org. 

My project will be using MongoDB Community version as the database. The community version allows me to store large amounts of data locally for testing and running the application without having to buy a service to run on Atlas. The free version of Atlas does not allow a large enough allowance of storage space for my application. In MongoDB, I created a database called "chess" and a collection called "games" as the default, but you can change it in the configs and parameters when setting up the database. The application will perform realtime data analysis to gather data about the next game states from the current queried game state. An aggregation pipeline is used to aggregate all possible next game states and their results from the database and returns the top 5 game states based on how many games were played. Realtime analysis must be used since the parameters for requested chess Opening Moves are dynamic and depends on the user's needs.  The pipeline can be found in `/database/analyzedata.py`. A document in my MongoDB project follows format: 

```
    {
        'game_state': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        'elo': 1000,
        'format': 'blitz',
        'white': 100,
        'black': 80,
        'draw': 20
    }
```
game_state: FEN representation of game state
elo: elo rating of the game
format: what format the game was played in (bullet, blitz, standard)
white: how many games white has won in that position
black: how many games black has won in that position
draw: how many games have been drawn in that position

My project connects to MongoDB via Pymongo in Python. There are 2 steps to running my application: setting up and storing data and running the full website and backend. Setting up and populating the database will take a very long time, however the web application can be used while it is populating. I recommend letting `setupDB.py` to run a few minutes before testing to ensure you have some games to view. Games are extracted by getting the game moves and the metadata from a game in the PGN file.  It then plays through the first 10 moves of the game (to save on storage space) and at each new game state, it adds/updates a document in the database.  A composite key is created using `(game_state, elo, format)` and for each key, it tracks the number of wins or draws the position has. When analyzing the data, one aggregation call is used to get the data every next game state possible instead of N number of aggregation calls.  For each game state in the call, it gathers all the documents of the game states and groups the documents by the game state which will combine all the requested elos and game formats that were searched for into a single document that adds the white, black, and draw fields and adds a count field tallying the total number of games that has reached that game state.

Example:

Take the game state above as well as the following one:

```
    {
        'game_state': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        'elo': 1200,
        'format': 'bullet',
        'white': 20,
        'black': 15,
        'draw': 5
    }
```

The aggregation of these 2 documents results in:

```
    {
        'game_state': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        'white': 120,
        'black': 95,
        'draw': 25,
        'total': 240
    }
```

## REQUIREMENTS
#### - requires python 3 (developed on 3.10)
#### - dependencies can be found in requirements.txt
#### - must have MongDB Community version installed and running.  Program will hang if it is not running. You can download it from: https://www.mongodb.com/try/download/community
#### - visit https://database.lichess.org/ to download a .pgn file of games and extract the pgn file. *you may want to find a small file as it will be decompressed and increase in size dramatically*

---

## Setting Up and Populating Database
#### - create a database in MongoDB (ex. 'chess')
#### - create a collection in the database you just created (ex. 'games')
#### - locate where you extracted the PGN file and get the path of it.
#### - navigate to /src and run `python3 setupDB.py -f <pgn filepath: required> -d <database name> -c <collection name> -g <max number of games>`
#### - only the filepath is required. the database name will default to `chess`, collection will default to `games` and the number of games will default to `100000`
##### *It will take a long time to add all the games.  In the meantime, you can still run the program and test it*

---

## Running Website and Service and Testing
#### - double check the configs in `config.json` are setup to match the database you populated earlier.
#### - the project is entirely built using Flask so to run, you only need to start the service using the command `python3 app.py`.
#### - navigate to http://localhost:5000 to view homepage and follow instructions.  To get a FEN, you can navigate to https://lichess.org/analysis and get the FEN from the bottom.
#### - on the analysis page, it displays the top 5 moves on the right as well as the parameters you searched for on top.
#### - Click on any of the moves on the right to play the move and view the statistics for that position. If you want to restart, click "Opening Table" at the top.