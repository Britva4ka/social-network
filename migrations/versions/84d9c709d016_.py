"""empty message

Revision ID: 84d9c709d016
Revises: 2ce419a08b4a
Create Date: 2023-03-29 18:39:50.178914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84d9c709d016'
down_revision = '2ce419a08b4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_column('email')

    # ### end Alembic commands ###
