"""empty message

Revision ID: 878c27afe28d
Revises: d9c063f17558
Create Date: 2019-10-11 10:49:43.610686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '878c27afe28d'
down_revision = 'd9c063f17558'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'rfID',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'rfID',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
