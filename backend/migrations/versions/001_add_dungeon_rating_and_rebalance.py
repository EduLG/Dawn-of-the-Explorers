"""add dungeon rating column and rebalance all dungeon values

Revision ID: 001
Revises:
Create Date: 2026-05-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

DUNGEON_VALUES = [
    ("Primeval Dense Forest",           40,   0,   0),
    ("The Infinite Observation Tower",  100,  24,  0),
    ("Canyon of Eternal Storms",        180,  60,  24),
    ("Archipelago of Wandering Clouds", 280,  108, 60),
    ("Abyssal Steam Pit",               400,  168, 108),
    ("Sunken Bronze City",              560,  240, 168),
    ("Isle of the Fallen Engineers",    760,  336, 240),
    ("Resonant Crystal Desert",         1000, 456, 336),
    ("Airship Graveyard",               1300, 600, 456),
    ("Etherized Caldera Volcano",       1640, 780, 600),
    ("Ether Core",                      1640, 984, 780),
]


def upgrade():
    conn = op.get_bind()

    result = conn.execute(text(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name='dungeon' AND column_name='rating'"
    ))
    if not result.fetchone():
        op.add_column('dungeon', sa.Column('rating', sa.Integer(), nullable=False, server_default='0'))

    for name, rating, min_rating, visibility_rating in DUNGEON_VALUES:
        conn.execute(text(
            "UPDATE dungeon SET rating=:r, min_rating=:mr, visibility_rating=:vr WHERE name=:n"
        ), {"r": rating, "mr": min_rating, "vr": visibility_rating, "n": name})


def downgrade():
    op.drop_column('dungeon', 'rating')
