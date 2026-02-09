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
    # Crear party
    # -------------------------------
    party = Party(name="Heroes Party", level=1, experience=0, rating=0)
    db.session.add(party)
    db.session.commit()

    # -------------------------------
    # Crear user
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
    # Crear jobs
    # -------------------------------
    job_names = [
        "engineer", "gunslinger", "adventurer", "alchemist",
        "warrior", "fender", "sage", "assasin", "scholar", "beastmaster"
    ]

    jobs = []
    for name in job_names:
        icon_path = f"frontend-react/src/assets/resources/character_templates/{name}_male.png"
        jobs.append(Job(name=name, icon=icon_path))
        
    db.session.add_all(jobs)
    db.session.commit()

    # -------------------------------
    # Crear characters
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
    # Crear equipments
    # -------------------------------
    equipments = [
        # Firion
        Equipment(name="Iron Helmet", type="head", rating=5),
        Equipment(name="Chain Mail", type="chest", rating=12),
        Equipment(name="Steel Sword", type="primary_hand", rating=10),
        Equipment(name="Wooden Shield", type="secondary_hand", rating=3),
        Equipment(name="Ring of Luck", type="accesory", rating=7),

        # Sabin
        Equipment(name="Alchemist Hood", type="head", rating=4),
        Equipment(name="Mystic Robe", type="chest", rating=9),
        Equipment(name="Crystal Staff", type="primary_hand", rating=11),
        Equipment(name="Focus Orb", type="secondary_hand", rating=2),
        Equipment(name="Amulet of Healing", type="accesory", rating=8),

        # Balthier
        Equipment(name="Engineer Goggles", type="head", rating=3),
        Equipment(name="Utility Vest", type="chest", rating=7),
        Equipment(name="Titan Wrench", type="primary_hand", rating=9),
        Equipment(name="Reinforced Bracer", type="secondary_hand", rating=4),
        Equipment(name="Pocket Compass", type="accesory", rating=5),

        # Locke
        Equipment(name="Straw Hat", type="head", rating=1),
        Equipment(name="Work Tunic", type="chest", rating=2),
        Equipment(name="Pitchfork", type="primary_hand", rating=6),
        Equipment(name="Wooden Buckler", type="secondary_hand", rating=1),
        Equipment(name="Lucky Clover", type="accesory", rating=3),
    ]
    db.session.add_all(equipments)
    db.session.commit()

    # -------------------------------
    # Asignar equipments a characters
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
