"""empty message

Revision ID: 1b05f529c629
Revises: 81df3081c0a7
Create Date: 2024-06-27 19:29:19.870472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b05f529c629'
down_revision = '81df3081c0a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.Text(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)

    # ### end Alembic commands ###
