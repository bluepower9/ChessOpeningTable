from api.routes.games import app as games

import flask
import logging
import json


app = flask.Flask(__name__)

app.logger.setLevel(logging.INFO)
app.register_blueprint(games)
with open('config.json', 'r') as f:
    config = json.load(f)
app.config.update(config)


if __name__ == '__main__':
    app.run(debug=True)