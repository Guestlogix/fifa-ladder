import os
import json
import config
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Setup App
app = Flask(__name__)
configuration_file = os.environ.get('ENV_VAR_DETERMINING_PROD', 'config.DevelopmentConfig') #determine config
app.config.from_object(configuration_file)

# Setup + SQLAlchemy + Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Import Models + Schema
from models import Player, GamePlayer, Game
from schema import players_schema, game_schema

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/players', methods=['GET'])
def players():
  players = Player.query.all()
  return players_schema.jsonify(players)

@app.route('/game', methods=['POST'])
def record_game():
  # Obtain JSON
  json_data = request.get_json()
  if not json_data:
    return jsonify({'message': 'No input data provided'}), 400

  # Find Players
  winner = Player.query.get(json_data['winner_id'])
  loser = Player.query.get(json_data['loser_id'])
  if not winner or not loser:
    return jsonify({'message': 'Players not found'}), 401

  # Create the GamePlayers
  winning_gameplayer = GamePlayer(player_id=winner.id, score=1)
  losing_gameplayer = GamePlayer(player_id=loser.id, score=0)

  # Create the Game
  game = Game(winner=winning_gameplayer, loser=losing_gameplayer, date=datetime.now())
  db.session.add(game)

  # Update the rank if loser's rank is less than winners
  if loser.rank < winner.rank:
    temp_rank = winner.rank
    winner.rank = loser.rank
    loser.rank = temp_rank

  # Commit all DB Changes
  db.session.commit()

  # Generate Response
  result = game_schema.dump(Game.query.get(game.id))
  return jsonify({
        'message': 'Recorded new game.',
        'game': result,
    })


# Gunicorn Run
if __name__ == '__main__':
    app.run()