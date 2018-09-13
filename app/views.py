import uuid, os, re
from datetime import datetime
from flask import render_template, request, redirect, jsonify
from app.exceptions import InvalidInput
from app.models import Player, GamePlayer, Game
from app.schema import players_schema, player_schema, games_schema, game_schema
from app import app, db
from slackclient import SlackClient


@app.errorhandler(InvalidInput)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def parse_json(request):
  json_data = request.get_json()
  if not json_data:
    return jsonify({'message': 'No input data provided'}), 400
  else:
    return json_data


def create_player_helper(id):
  # Get Slack Info
  slack_token = os.environ["SLACK_API_TOKEN"]
  sc = SlackClient(slack_token)
  slack_user = sc.api_call("users.info", user=id )
  name = slack_user['user']['real_name']

  # Create Player
  next_rank = db.session.query(Player).count() + 1
  player = Player(id=id, name=name, rank=next_rank)
  db.session.add(player)

  # Commit to DB
  db.session.commit()
  return player

# Tokenizes an returns as a dict message e.g `<@U831BB2JX|gpsarakis> 1 <@U60U7A0KW|hank> 2`
def parse_message(message_text):
  user_ids = re.findall('@(.*?)\|', message_text)
  scores = [int(s) for s in re.findall('([^[>]+)(?:$|<)(?:$|)', message_text)]

  if (len(user_ids) != 2 or len(scores) != 2):
    raise InvalidInput('Please send message of form "@username score @username score"', status_code=410)

  return {
    'player_a_id': user_ids[0],
    'player_a_score': scores[0],
    'player_b_id': user_ids[1],
    'player_b_score': scores[1],
  }



@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/players', methods=['GET'])
def get_players():
  players = Player.query.all()
  return players_schema.jsonify(players)

@app.route('/games', methods=['GET'])
def get_games():
  games = Game.query.all()
  return games_schema.jsonify(games)

@app.route('/games', methods=['POST'])
def record_game():
  payload = parse_json(request)
  data = parse_message(payload['text'])

  # Find Players
  player_a = Player.query.get(data['player_a_id'])
  player_b = Player.query.get(data['player_b_id'])
  
  # Make Player A if not in system already
  if not player_a:
    player_a = create_player_helper(data['player_a_id'])

  # Make Player B if not in system already
  if not player_b:
    player_b = create_player_helper(data['player_b_id'])

  # Create the GamePlayers
  player_a_gameplayer = GamePlayer(player_id=player_a.id, score=data['player_a_score'])
  player_b_gameplayer = GamePlayer(player_id=player_b.id, score=data['player_b_score'])

  # Create the Game
  game = Game(player_a=player_a_gameplayer, player_b=player_b_gameplayer, date=datetime.now())
  db.session.add(game)

  # Assign winner/loser
  if (player_a_gameplayer.score > player_b_gameplayer.score):
    winner = player_a
    loser = player_b
  elif (player_b_gameplayer.score > player_a_gameplayer.score):
    winner = player_b
    loser = player_a

  # Update the rank if loser's rank is less than winners
  if (winner and loser):
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