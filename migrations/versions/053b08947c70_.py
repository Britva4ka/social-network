"""empty message

Revision ID: 053b08947c70
Revises: 5d6cc15bbde3
Create Date: 2023-05-01 14:04:52.386344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '053b08947c70'
down_revision = '5d6cc15bbde3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sender_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('receiver_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('messages_fk_sender_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('messages_fk_receiver_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('fk_sender_id', 'user', ['sender_id'], ['id'])
        batch_op.create_foreign_key('fk_receiver_id', 'user', ['receiver_id'], ['id'])
        batch_op.drop_column('none_col')
        batch_op.drop_column('fk_receiver_id')
        batch_op.drop_column('fk_sender_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_sender_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('fk_receiver_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('none_col', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint('fk_receiver_id', type_='foreignkey')
        batch_op.drop_constraint('fk_sender_id', type_='foreignkey')
        batch_op.create_foreign_key('messages_fk_receiver_id_fkey', 'user', ['fk_receiver_id'], ['id'])
        batch_op.create_foreign_key('messages_fk_sender_id_fkey', 'user', ['fk_sender_id'], ['id'])
        batch_op.drop_column('receiver_id')
        batch_op.drop_column('sender_id')

    # ### end Alembic commands ###
