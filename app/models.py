from app import app, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    rank = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Player %r>' % (self.email)

class GamePlayer(db.Model):
    __tablename__ = 'game_player'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    player_id = db.Column(UUID(as_uuid=True), db.ForeignKey('player.id'))
    player = db.relationship(
        'Player',
        backref=db.backref('games', lazy='dynamic'),
    )
    score = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Player %r>' % (self.id)

class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    winner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('game_player.id'))
    winner = db.relationship(
        'GamePlayer',
        foreign_keys=[winner_id],
        backref=db.backref('wins', lazy='dynamic'),
    )
    loser_id = db.Column(UUID(as_uuid=True), db.ForeignKey('game_player.id'))
    loser = db.relationship(
        'GamePlayer',
        foreign_keys=[loser_id],
        backref=db.backref('losses', lazy='dynamic'),
    )
    date = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Game %r>' % (self.id)