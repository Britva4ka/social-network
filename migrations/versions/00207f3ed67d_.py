"""empty message

Revision ID: 00207f3ed67d
Revises: 9e41724b61ad
Create Date: 2023-04-24 22:09:43.711509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00207f3ed67d'
down_revision = '9e41724b61ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('fk_sender_id', sa.Integer(), nullable=False),
    sa.Column('fk_receiver_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=1000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fk_receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['fk_sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###
