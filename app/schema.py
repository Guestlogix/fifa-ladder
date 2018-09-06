from marshmallow import fields
from app.models import Player, GamePlayer, Game
from app import ma

class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = Player

class GamePlayerSchema(ma.ModelSchema):
    class Meta:
        model = GamePlayer

class GameSchema(ma.ModelSchema):
    class Meta:
        model = Game
    winner = fields.Nested(GamePlayerSchema())
    loser = fields.Nested(GamePlayerSchema())
        
player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
game_schema = GameSchema()
games_schema = GameSchema(many=True)