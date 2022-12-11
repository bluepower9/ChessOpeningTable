import chess

def get_all_moves(fen: str) -> dict:
    '''
    Gets all the moves of a given FEN position and returns a dict of all the possible states and moves in the form: {FEN: move}

    ARGS:
        fen: the FEN string of the position

    RETURNS:
        dictionary of the game states and moves {FEN: move}
    '''

    board = chess.Board(fen)
    all_moves = {}  #dict of fen: move

    #gets all the FEN positions for all possible moves from the starting FEN position
    for move in board.legal_moves:
        board.push(move)
        all_moves[board.fen()] = move
        board.pop()

    return all_moves


def parse_data(data: list, all_moves: dict) -> list:
    '''
    Parses the data pulled from MongoDB and calculates the win percentages and returns a list of the states with the metadata.
    Gets the move that leads to the FEN position which is displayed to the user.

    ARGS:
        data: list of the data returned from MongoDB
        all_moves: dict of all the possible FEN game states mapped to the correesponding move. 

    RETURNS:
        list of dicts containing the different states with processed data.
    '''
    
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
    
    return result