from marshmallow import fields
from app.models import Player, GamePlayer, Game
from app import ma

class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = Player

class GamePlayerSchema(ma.ModelSchema):
    class Meta:
        model = GamePlayer
    player = fields.Nested(PlayerSchema)

class GameSchema(ma.ModelSchema):
    class Meta:
        model = Game
    player_a = fields.Nested(GamePlayerSchema)
    player_b = fields.Nested(GamePlayerSchema)
        
player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
game_schema = GameSchema()
games_schema = GameSchema(many=True)