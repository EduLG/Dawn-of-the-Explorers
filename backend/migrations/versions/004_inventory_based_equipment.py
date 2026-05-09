"""character_equipment references party_inventory instead of equipment

Revision ID: 004
Revises: 003
Create Date: 2026-05-09

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def column_exists(conn, table, column):
    result = conn.execute(text(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name=:t AND column_name=:c"
    ), {"t": table, "c": column})
    return result.fetchone() is not None


def constraint_exists(conn, table, constraint):
    result = conn.execute(text(
        "SELECT constraint_name FROM information_schema.table_constraints "
        "WHERE table_name=:t AND constraint_name=:c"
    ), {"t": table, "c": constraint})
    return result.fetchone() is not None


def upgrade():
    conn = op.get_bind()

    # Existing rows are stale under the new model — clear them
    conn.execute(text("DELETE FROM character_equipment"))

    # Drop old equipment_id FK and column
    if constraint_exists(conn, 'character_equipment', 'character_equipment_equipment_id_fkey'):
        conn.execute(text(
            "ALTER TABLE character_equipment DROP CONSTRAINT character_equipment_equipment_id_fkey"
        ))

    if column_exists(conn, 'character_equipment', 'equipment_id'):
        op.drop_column('character_equipment', 'equipment_id')

    # Add inventory_id FK column
    if not column_exists(conn, 'character_equipment', 'inventory_id'):
        op.add_column('character_equipment', sa.Column(
            'inventory_id', sa.Integer(), nullable=False
        ))
        conn.execute(text(
            "ALTER TABLE character_equipment ADD CONSTRAINT character_equipment_inventory_id_fkey "
            "FOREIGN KEY (inventory_id) REFERENCES party_inventory(id) ON DELETE CASCADE"
        ))


def downgrade():
    conn = op.get_bind()

    conn.execute(text("DELETE FROM character_equipment"))

    if constraint_exists(conn, 'character_equipment', 'character_equipment_inventory_id_fkey'):
        conn.execute(text(
            "ALTER TABLE character_equipment DROP CONSTRAINT character_equipment_inventory_id_fkey"
        ))

    if column_exists(conn, 'character_equipment', 'inventory_id'):
        op.drop_column('character_equipment', 'inventory_id')

    if not column_exists(conn, 'character_equipment', 'equipment_id'):
        op.add_column('character_equipment', sa.Column(
            'equipment_id', sa.Integer(), nullable=False
        ))
        conn.execute(text(
            "ALTER TABLE character_equipment ADD CONSTRAINT character_equipment_equipment_id_fkey "
            "FOREIGN KEY (equipment_id) REFERENCES equipment(id)"
        ))
