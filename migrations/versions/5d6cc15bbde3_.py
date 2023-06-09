"""empty message

Revision ID: 5d6cc15bbde3
Revises: 5dd2efc25e47
Create Date: 2023-05-01 14:00:25.329350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d6cc15bbde3'
down_revision = '5dd2efc25e47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('none_col', sa.Integer(), nullable=True))
        op.execute(
            '''
                update messages
                set sup_sender_id = fk_sender_id;
            '''
        )
        op.execute(
            '''
                update messages
                set sup_receiver_id = fk_receiver_id;
            '''
        )

        # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('none_col')
        op.execute(
            '''
                update messages
                set fk_sender_id = sup_sender_id;
            '''
        )
        op.execute(
            '''
                update messages
                set fk_receiver_id = sup_receiver_id;
            '''
        )
    # ### end Alembic commands ###
