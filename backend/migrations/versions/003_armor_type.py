"""add equipment_type (armor class), rename type->slot, drop job_id from equipment

Revision ID: 003
Revises: 002
Create Date: 2026-05-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

revision = '003'
down_revision = '002'
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

    # 1. Rename type -> slot (skip if already done)
    if column_exists(conn, 'equipment', 'type'):
        conn.execute(text("ALTER TABLE equipment RENAME COLUMN type TO slot"))

    # 2. Rename old slot check constraint (skip if already renamed)
    if constraint_exists(conn, 'equipment', 'ck_equipment_type'):
        conn.execute(text(
            "ALTER TABLE equipment RENAME CONSTRAINT ck_equipment_type TO ck_equipment_slot"
        ))

    # 3. Add equipment_type column (skip if already exists)
    if not column_exists(conn, 'equipment', 'equipment_type'):
        op.add_column('equipment', sa.Column('equipment_type', sa.String(), nullable=True))

        # 4. Populate from joined job name
        conn.execute(text("""
            UPDATE equipment
            SET equipment_type = CASE
                WHEN j.name IN ('warrior', 'fender') THEN 'plate'
                WHEN j.name IN ('adventurer', 'beastmaster', 'gunslinger', 'thief') THEN 'leather'
                WHEN j.name IN ('alchemist', 'engineer', 'sage', 'scholar') THEN 'cloth'
            END
            FROM job j
            WHERE equipment.job_id = j.id
        """))

        op.alter_column('equipment', 'equipment_type', nullable=False)

    # 5. Add check constraint (skip if already exists)
    if not constraint_exists(conn, 'equipment', 'ck_equipment_armor_type'):
        conn.execute(text(
            "ALTER TABLE equipment ADD CONSTRAINT ck_equipment_armor_type "
            "CHECK (equipment_type IN ('plate', 'leather', 'cloth'))"
        ))

    # 6. Drop job_id (skip if already dropped)
    if column_exists(conn, 'equipment', 'job_id'):
        conn.execute(text("ALTER TABLE equipment DROP CONSTRAINT IF EXISTS equipment_job_id_fkey"))
        op.drop_column('equipment', 'job_id')


def downgrade():
    conn = op.get_bind()

    if not column_exists(conn, 'equipment', 'job_id'):
        op.add_column('equipment', sa.Column('job_id', sa.Integer(), nullable=True))
        conn.execute(text("""
            UPDATE equipment
            SET job_id = (
                SELECT MIN(j.id) FROM job j WHERE
                (equipment.equipment_type = 'plate'   AND j.name IN ('warrior', 'fender')) OR
                (equipment.equipment_type = 'leather' AND j.name IN ('adventurer', 'beastmaster', 'gunslinger', 'thief')) OR
                (equipment.equipment_type = 'cloth'   AND j.name IN ('alchemist', 'engineer', 'sage', 'scholar'))
            )
        """))

    if constraint_exists(conn, 'equipment', 'ck_equipment_armor_type'):
        conn.execute(text("ALTER TABLE equipment DROP CONSTRAINT ck_equipment_armor_type"))

    if column_exists(conn, 'equipment', 'equipment_type'):
        op.drop_column('equipment', 'equipment_type')

    if constraint_exists(conn, 'equipment', 'ck_equipment_slot'):
        conn.execute(text(
            "ALTER TABLE equipment RENAME CONSTRAINT ck_equipment_slot TO ck_equipment_type"
        ))

    if column_exists(conn, 'equipment', 'slot'):
        conn.execute(text("ALTER TABLE equipment RENAME COLUMN slot TO type"))
