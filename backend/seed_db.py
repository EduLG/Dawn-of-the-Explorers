from app import create_app
from app.extensions import db
from werkzeug.security import generate_password_hash

from app.models.job import Job
from app.models.user import User
from app.models.party import Party
from app.models.character import Character
from app.models.equipment import Equipment
from app.models.character_equipment import CharacterEquipment

app = create_app()

with app.app_context():

    db.drop_all()
    db.create_all()

    # -------------------------------
    # Create party
    # -------------------------------
    party = Party(name="Heroes Party", level=1, experience=0)
    db.session.add(party)
    db.session.commit()

    # -------------------------------
    # Create user
    # -------------------------------
    user = User(
        username="eduladron",
        email="edu@example.com",
        password=generate_password_hash("12345678"),
        party_id=party.id
    )
    db.session.add(user)
    db.session.commit()

    # -------------------------------
    # Create jobs
    # -------------------------------
    job_names = [
        "engineer", "gunslinger", "adventurer", "alchemist",
        "warrior", "fender", "sage", "assasin", "scholar", "beastmaster"
    ]

    jobs = []
    for name in job_names:
        icon_path = f"/character-templates/{name}_male.png"
        jobs.append(Job(name=name, icon=icon_path))
        
    db.session.add_all(jobs)
    db.session.commit()

    # -------------------------------
    # Create characters
    # -------------------------------
    characters = [
        Character(name="Firion", current_job_id=jobs[4].id, party_id=party.id),      # warrior
        Character(name="Sabin", current_job_id=jobs[3].id, party_id=party.id),       # alchemist
        Character(name="Balthier", current_job_id=jobs[0].id, party_id=party.id),   # engineer
        Character(name="Locke", current_job_id=jobs[2].id, party_id=party.id)       # adventurer
    ]

    db.session.add_all(characters)
    db.session.commit()

    # -------------------------------
    # Create equipments
    # -------------------------------
    equipments = [
        # Firion (warrior)
        Equipment(name="Iron Helmet", type="head", rating=5, job_id=jobs[4].id),
        Equipment(name="Chain Mail", type="chest", rating=12, job_id=jobs[4].id),
        Equipment(name="Steel Sword", type="primary_hand", rating=10, job_id=jobs[4].id),
        Equipment(name="Wooden Shield", type="secondary_hand", rating=3, job_id=jobs[4].id),
        Equipment(name="Ring of Luck", type="accesory", rating=7, job_id=jobs[4].id),

        # Sabin (alchemist)
        Equipment(name="Alchemist Hood", type="head", rating=4, job_id=jobs[3].id),
        Equipment(name="Mystic Robe", type="chest", rating=9, job_id=jobs[3].id),
        Equipment(name="Crystal Staff", type="primary_hand", rating=11, job_id=jobs[3].id),
        Equipment(name="Focus Orb", type="secondary_hand", rating=2, job_id=jobs[3].id),
        Equipment(name="Amulet of Healing", type="accesory", rating=8, job_id=jobs[3].id),

        # Balthier (engineer)
        Equipment(name="Engineer Goggles", type="head", rating=3, job_id=jobs[0].id),
        Equipment(name="Utility Vest", type="chest", rating=7, job_id=jobs[0].id),
        Equipment(name="Titan Wrench", type="primary_hand", rating=9, job_id=jobs[0].id),
        Equipment(name="Reinforced Bracer", type="secondary_hand", rating=4, job_id=jobs[0].id),
        Equipment(name="Pocket Compass", type="accesory", rating=5, job_id=jobs[0].id),

        # Locke (adventurer)
        Equipment(name="Straw Hat", type="head", rating=1, job_id=jobs[2].id),
        Equipment(name="Work Tunic", type="chest", rating=2, job_id=jobs[2].id),
        Equipment(name="Pitchfork", type="primary_hand", rating=6, job_id=jobs[2].id),
        Equipment(name="Wooden Buckler", type="secondary_hand", rating=1, job_id=jobs[2].id),
        Equipment(name="Lucky Clover", type="accesory", rating=3, job_id=jobs[2].id),
    ]
    db.session.add_all(equipments)
    db.session.commit()

    # -------------------------------
    # Asign equipments to characters
    # -------------------------------
    firion = characters[0]
    sabin = characters[1]
    balthier = characters[2]
    locke = characters[3]

    char_equipments = [
        # Firion
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[0].id, slot="head"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[1].id, slot="chest"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[2].id, slot="primary_hand"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[3].id, slot="secondary_hand"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[4].id, slot="accesory"),

        # Sabin
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[5].id, slot="head"),
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[6].id, slot="chest"),
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[7].id, slot="primary_hand"),
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[8].id, slot="secondary_hand"),
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[9].id, slot="accesory"),

        # Balthier
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[10].id, slot="head"),
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[11].id, slot="chest"),
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[12].id, slot="primary_hand"),
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[13].id, slot="secondary_hand"),
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[14].id, slot="accesory"),

        # Locke
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[15].id, slot="head"),
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[16].id, slot="chest"),
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[17].id, slot="primary_hand"),
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[18].id, slot="secondary_hand"),
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[19].id, slot="accesory"),
    ]
    db.session.add_all(char_equipments)
    db.session.commit()

    print("Seeding data inserted successfully")
