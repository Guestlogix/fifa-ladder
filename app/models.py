from app import app, db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
import uuid

class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.String(10), index=True, unique=True, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    rank = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Player %r>' % (self.email)

class GamePlayer(db.Model):
    __tablename__ = 'game_player'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    player_id = db.Column(db.String(10), db.ForeignKey('player.id'))
    player = db.relationship('Player')
    score = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Player %r>' % (self.id)

class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    player_a_id = db.Column(UUID(as_uuid=True), db.ForeignKey('game_player.id'))
    player_a = db.relationship('GamePlayer', foreign_keys=[player_a_id])
    player_b_id = db.Column(UUID(as_uuid=True), db.ForeignKey('game_player.id'))
    player_b = db.relationship('GamePlayer', foreign_keys=[player_b_id])
    date = db.Column(db.DateTime, index=True)

    @hybrid_property
    def outcome(self):
        return 'TIE' if self.player_a.score == self.player_b.score else 'CONCLUSION'

    def __repr__(self):
        return '<Game %r>' % (self.id)