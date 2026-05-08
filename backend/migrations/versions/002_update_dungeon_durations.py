"""update dungeon durations

Revision ID: 002
Revises: 001
Create Date: 2026-05-08

"""
from alembic import op
from sqlalchemy import text

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

DUNGEON_DURATIONS = [
    ("Primeval Dense Forest",           20),
    ("The Infinite Observation Tower",  300),
    ("Canyon of Eternal Storms",        1200),
    ("Archipelago of Wandering Clouds", 2700),
    ("Abyssal Steam Pit",               3600),
    ("Sunken Bronze City",              6300),
    ("Isle of the Fallen Engineers",    10800),
    ("Resonant Crystal Desert",         18000),
    ("Airship Graveyard",               28800),
    ("Etherized Caldera Volcano",       43200),
    ("Ether Core",                      86400),
]

OLD_DUNGEON_DURATIONS = [
    ("Primeval Dense Forest",           60),
    ("The Infinite Observation Tower",  120),
    ("Canyon of Eternal Storms",        180),
    ("Archipelago of Wandering Clouds", 300),
    ("Abyssal Steam Pit",               420),
    ("Sunken Bronze City",              600),
    ("Isle of the Fallen Engineers",    900),
    ("Resonant Crystal Desert",         1200),
    ("Airship Graveyard",               1800),
    ("Etherized Caldera Volcano",       3600),
    ("Ether Core",                      7200),
]


def upgrade():
    conn = op.get_bind()
    for name, duration in DUNGEON_DURATIONS:
        conn.execute(
            text("UPDATE dungeon SET duration=:d WHERE name=:n"),
            {"d": duration, "n": name},
        )


def downgrade():
    conn = op.get_bind()
    for name, duration in OLD_DUNGEON_DURATIONS:
        conn.execute(
            text("UPDATE dungeon SET duration=:d WHERE name=:n"),
            {"d": duration, "n": name},
        )
