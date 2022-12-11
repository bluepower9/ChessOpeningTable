from flask import Flask, Blueprint, request, current_app
from data.analyzedata import aggregate_data

import chess
import flask


app = Blueprint('games', __name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

    
@app.route('/games/analysis', methods=['GET'])
def get_game_state():
    '''
    calls the database and gets the top 5 moves from it based on how many times it has occured. Returns a template page.
    '''

    #gets the args from the query string
    args = request.args.to_dict()
    fen = args.get('fen')
    if not fen:
        fen = chess.Board().fen()
    min_elo = int(args['min_elo'])
    max_elo = int(args['max_elo'])

    # if min elo is less than max elo, gets all elos instead
    if min_elo > max_elo:
        min_elo = 600
        max_elo = 3000
    
    #gets game formats
    game_format = []
    if args.get('bullet'):
        game_format.append('bullet')
    if args.get('blitz'):
        game_format.append('blitz')
    if args.get('standard'):
        game_format.append('standard')
    
    if len(game_format) == 0:
        game_format = ['bullet', 'blitz', 'standard']


    board = chess.Board(fen)
    all_moves = {}  #dict of fen: move

    #gets all the FEN positions for all possible moves from the starting FEN position
    for move in board.legal_moves:
        board.push(move)
        all_moves[board.fen()] = move
        board.pop()

    #calls the aggregate data function to run realtime analysis to get data.
    data = aggregate_data(
        list(all_moves.keys()), 
        db_name=current_app.config.get('database').get('db_name'), 
        collection=current_app.config.get('database').get('collection'), 
        min_elo=min_elo, 
        max_elo=max_elo, 
        format=game_format
        )

    data = list(data)
    
    result = []
    for d in data:
        total = int(d['total'])
        #calculates win %
        white = round(int(d['white'])/total * 100)
        black = round(int(d['black'])/total *100)

        state = {
            'fen': d['_id']['game_state'],
            'move': all_moves[d['_id']['game_state']],
            'white': white,
            'black': black,
            'draw': 100 - white - black ,
            'total': total
        }

        result.append(state)
    
    return flask.render_template('analysis.html', min_elo=min_elo, max_elo=max_elo, format=game_format, fen=fen, moves=result)

   

