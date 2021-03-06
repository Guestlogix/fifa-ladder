"""empty message

Revision ID: f5e4ff8e8b41
Revises: 835745a71d15
Create Date: 2018-09-14 18:40:49.359432

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'f5e4ff8e8b41'
down_revision = '835745a71d15'
branch_labels = None
depends_on = None


def upgrade():
    gameoutcome = postgresql.ENUM('win', 'loss', 'tie', name='gameoutcome')
    gameoutcome.create(op.get_bind())
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game_player', sa.Column('game_outcome', sa.Enum('win', 'loss', 'tie', name='gameoutcome'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game_player', 'game_outcome')
    op.execute("DROP TYPE gameoutcome;")
    # ### end Alembic commands ###
