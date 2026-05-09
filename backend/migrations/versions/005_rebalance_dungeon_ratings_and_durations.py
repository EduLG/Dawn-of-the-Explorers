"""rebalance dungeon ratings and durations

Revision ID: 005
Revises: 004
Create Date: 2026-05-09

"""
from alembic import op
from sqlalchemy import text

revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None

NEW_VALUES = [
    ("Primeval Dense Forest",           0,    60),
    ("The Infinite Observation Tower",  50,   210),
    ("Canyon of Eternal Storms",        125,  600),
    ("Archipelago of Wandering Clouds", 225,  1500),
    ("Abyssal Steam Pit",               350,  3000),
    ("Sunken Bronze City",              500,  5400),
    ("Isle of the Fallen Engineers",    700,  9900),
    ("Resonant Crystal Desert",         950,  14400),
    ("Airship Graveyard",               1250, 21600),
    ("Etherized Caldera Volcano",       1625, 32400),
    ("Ether Core",                      2050, 43200),
]

OLD_VALUES = [
    ("Primeval Dense Forest",           40,   20),
    ("The Infinite Observation Tower",  100,  300),
    ("Canyon of Eternal Storms",        180,  1200),
    ("Archipelago of Wandering Clouds", 280,  2700),
    ("Abyssal Steam Pit",               400,  3600),
    ("Sunken Bronze City",              560,  6300),
    ("Isle of the Fallen Engineers",    760,  10800),
    ("Resonant Crystal Desert",         1000, 18000),
    ("Airship Graveyard",               1300, 28800),
    ("Etherized Caldera Volcano",       1640, 43200),
    ("Ether Core",                      1640, 86400),
]


def upgrade():
    conn = op.get_bind()
    for name, rating, duration in NEW_VALUES:
        conn.execute(
            text("UPDATE dungeon SET rating=:r, duration=:d WHERE name=:n"),
            {"r": rating, "d": duration, "n": name},
        )


def downgrade():
    conn = op.get_bind()
    for name, rating, duration in OLD_VALUES:
        conn.execute(
            text("UPDATE dungeon SET rating=:r, duration=:d WHERE name=:n"),
            {"r": rating, "d": duration, "n": name},
        )
