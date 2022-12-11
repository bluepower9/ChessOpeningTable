from data.database.db import connect
import pymongo
import chess


def aggregate_data(state: list, db_name:str = "chess", collection:str = 'games', min_elo=600, max_elo=3000, format=['blitz', 'bullet', 'standard']):
    '''
    performs aggregation pipeline for the data in MongoDB

    ARGS:
        state: list of all game states to analyze and gather data.
        db_name: database name
        collection: collection name
        min_elo: minimum elo to search
        max_elo: maximum elo to search
        format: game format
    '''
    pipeline = [
    {
        '$match': {
            'game_state': {"$in": state},
            'format': {'$in': format},
            'elo': {'$gte': min_elo, "$lte": max_elo}
        }
    }, {
        '$group': {
            '_id': {
                'game_state': '$game_state', 
            }, 
            'white': {
                '$sum': '$white'
            }, 
            'black': {
                '$sum': '$black'
            }, 
            'draw': {
                '$sum': '$draw'
            }
        }
    }, {
        '$addFields': {
            'total': {
                '$sum': [
                    '$white', '$black', '$draw'
                ]
            }
        }
    }, {
        '$sort': {
            'total': -1
        }
    }, {
        '$limit': 5
    }
]

    db = connect()

    return db[db_name][collection].aggregate(pipeline)


