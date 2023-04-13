"""empty message

Revision ID: 9e41724b61ad
Revises: 813457f02584
Create Date: 2023-04-13 00:54:05.504285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e41724b61ad'
down_revision = '813457f02584'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['avatar'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###