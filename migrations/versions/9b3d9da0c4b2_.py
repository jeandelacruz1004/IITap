"""empty message

Revision ID: 9b3d9da0c4b2
Revises: ae6ef090ca32
Create Date: 2019-10-22 17:36:37.454106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b3d9da0c4b2'
down_revision = 'ae6ef090ca32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('rfID', sa.String(length=255), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('public_id'),
    sa.UniqueConstraint('rfID'),
    sa.UniqueConstraint('username')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eventName', sa.String(length=100), nullable=False),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.Column('eventDate', sa.DateTime(), nullable=False),
    sa.Column('eventStartTime', sa.Time(), nullable=True),
    sa.Column('eventEndTime', sa.Time(), nullable=True),
    sa.Column('eventDescription', sa.Text(), nullable=True),
    sa.Column('location', sa.Text(), nullable=False),
    sa.Column('fee', sa.Integer(), nullable=True),
    sa.Column('public_id', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    op.drop_table('user')
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###
