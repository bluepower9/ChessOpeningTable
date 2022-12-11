from pymongo import MongoClient
from data.database.db import connect
from alive_progress import alive_bar
import pymongo
import json
import os
import glob
import chess
import chess.pgn
import argparse



def play_game( db:MongoClient, moves:list, format: str, elo: int, result:str, max_moves=10, aggregate=True):
    '''
    plays through the first MAX_MOVES in the game and adds the game states to the database.

    ARGS:
        db: database object
        moves: list of chess.Move.uci moves
        format: format of the game (bullet, blitz, standard)
        elo: average elo of the 2 players rounded to nearest 100th
        result: string of game result (ex: 1-2)
        max_moves: maximum depth of game
        aggregate: whether or not to aggregate game state when added to database.  (sum up the white, black, and draw scores)
    '''
    count = 0
    board = chess.Board()
    docs = []

    result = result.strip()
    white = 1 if result == '1-0' else 0
    black = 1 if result == '0-1' else 0
    draw = 1 if result == '1/2-1/2' else 0

    while count < max_moves*2 and count < len(moves):
        board.push(moves[count])
        count += 1
        if not aggregate:
            docs.append({'game_state': board.fen(), 'elo': elo, 'format': format, 'white': white, 'black': black, 'draw': draw})
        else:
            db.update_one(
                {'game_state': board.fen(), 'elo': elo, 'format': format}, 
                {'$inc': {'white': white, 'black': black, 'draw': draw}},
                upsert=True
            )
    if not aggregate:
        db.insert_many(docs)



def insert_data(filename: str, max_games:int=100000, db_name:str='chess', collection:str='games', aggregate=True):
    '''
    iterates over all the games in the /lichess/uci directory and adds them to MongoDB.

    ARGS:
        filename: name of pgn file to extract games from.
        max_games: maximum number of games to add to database
        db_name: name of database
        collection: name of collection
        aggregate: whether or not to aggregate games as they are added to database (sum up the white, black, and draw scores)
    '''

    print('connecting to database...')
    client = connect()
    db = client[db_name][collection]

    print('creating index...')
    db.create_index([('game_state', pymongo.ASCENDING), ('elo', pymongo.ASCENDING), ('format', pymongo.ASCENDING)], unique=True)
    
    with open(filename, 'r') as file:
        print('importing games from file: ', filename)
        game = chess.pgn.read_game(file)
        count = 0
        with alive_bar(max_games) as bar:   #adds really cool progress bar!
            while game and count < max_games:
                moves = list(game.mainline_moves())

                #if game was abandoned or is too short, move on to next game
                if game.headers['Termination'] == 'Abandoned' or len(moves) < 4:
                    game = chess.pgn.read_game(file)
                    continue
                
                #extracts game metadata
                white_elo = int(game.headers['WhiteElo'])
                black_elo = int(game.headers['BlackElo'])
                elo = round((white_elo+black_elo)/200) * 100    #gets the average elo and then rounds to nearest 100th
                result = game.headers['Result']
                event = game.headers['Event']
                #defaults to standard, switches format if it detects bullet or blitz
                format = 'standard'
                if 'Bullet' in event:
                    format = 'bullet'
                elif 'Blitz' in event:
                    format = 'blitz'

                #plays through game and adds game states to database
                play_game(db, moves, format, elo, result)

                game = chess.pgn.read_game(file)
                count += 1
                bar()
            



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-d', '--db', default='chess')
    parser.add_argument('-c', '--collection', default='games')
    parser.add_argument('-g', '--games', type=int, default=100000)
    args = parser.parse_args()
    

    insert_data(args.file, db_name=args.db, max_games=args.games, collection=args.collection, aggregate=True)
    
