from datetime import datetime
from flask import render_template, request, redirect, jsonify
from app.models import Player, GamePlayer, Game
from app.schema import players_schema, player_schema, game_schema
from app import app, db
import uuid

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/players', methods=['GET'])
def players():
  players = Player.query.all()
  return players_schema.jsonify(players)

@app.route('/players', methods=['POST'])
def create_player():
  # Obtain JSON
  json_data = request.get_json()
  if not json_data:
    return jsonify({'message': 'No input data provided'}), 400

  # Create Player
  next_rank = db.session.query(Player).count() + 1
  player = Player(email=json_data['email'], first_name=json_data['firstname'], last_name=json_data['lastname'], rank=next_rank)
  db.session.add(player)

  # Commit to DB
  db.session.commit()

  # Generate Response
  result = player_schema.dump(player)
  return jsonify(result)

@app.route('/game', methods=['POST'])
def record_game():
  # Obtain JSON
  json_data = request.get_json()
  if not json_data:
    return jsonify({'message': 'No input data provided'}), 400

  # Find Players
  winner = Player.query.filter_by(email=json_data['winner']).first()
  loser = Player.query.filter_by(email=json_data['loser']).first()
  
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