"""lab 5 tables

Revision ID: c51378d78d88
Revises: 
Create Date: 2022-12-19 16:03:13.949994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c51378d78d88'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('hometown', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_artist_hometown'), ['hometown'], unique=False)
        batch_op.create_index(batch_op.f('ix_artist_name'), ['name'], unique=True)

    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('location', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_venue_location'), ['location'], unique=False)
        batch_op.create_index(batch_op.f('ix_venue_name'), ['name'], unique=False)

    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('date', sa.String(length=120), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_event_date'), ['date'], unique=False)
        batch_op.create_index(batch_op.f('ix_event_name'), ['name'], unique=True)

    op.create_table('artist_to_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artist_to_event')
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_event_name'))
        batch_op.drop_index(batch_op.f('ix_event_date'))

    op.drop_table('event')
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_venue_name'))
        batch_op.drop_index(batch_op.f('ix_venue_location'))

    op.drop_table('venue')
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_artist_name'))
        batch_op.drop_index(batch_op.f('ix_artist_hometown'))

    op.drop_table('artist')
    # ### end Alembic commands ###
