"""empty message

Revision ID: 4dbdb4fea6d3
Revises: 7de856135982
Create Date: 2024-07-06 15:53:26.019702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dbdb4fea6d3'
down_revision = '7de856135982'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sms', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sms', schema=None) as batch_op:
        batch_op.drop_column('amount')

    # ### end Alembic commands ###
