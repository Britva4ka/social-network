"""empty message

Revision ID: b91913fa39f7
Revises: 1b579f4eef0c
Create Date: 2023-05-01 14:10:16.188108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b91913fa39f7'
down_revision = '1b579f4eef0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.alter_column('sender_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('receiver_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('sup_sender_id')
        batch_op.drop_column('sup_receiver_id')
        batch_op.drop_column('none_col')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('none_col', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('sup_receiver_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('sup_sender_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.alter_column('receiver_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('sender_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
