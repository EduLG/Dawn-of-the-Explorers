from app import create_app
from app.extensions import db
from werkzeug.security import generate_password_hash

from app.models.job import Job
from app.models.user import User
from app.models.party import Party
from app.models.character import Character
from app.models.equipment import Equipment
from app.models.party_character import PartyCharacter
from app.models.character_equipment import CharacterEquipment

app = create_app()

with app.app_context():

    db.drop_all()
    db.create_all()

    party = Party(name="Heroes Party", level=1, experience=0, rating=0)
    db.session.add(party)
    db.session.commit()

    user = User(username="eduladron", email="edu@example.com",
                password=generate_password_hash("12345678"),
                party_id=party.id)
    db.session.add(user)
    db.session.commit()

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

    characters = [
        Character(name="Firion", current_job_id=jobs[4].id),      # warrior
        Character(name="Sabin", current_job_id=jobs[3].id),      # alchemist
        Character(name="Balthier", current_job_id=jobs[0].id),      # engineer
        Character(name="Locke", current_job_id=jobs[2].id)    # adventurer
    ]
    db.session.add_all(characters)
    db.session.commit()


    # Create equipment pool (5 items per character so each can be fully equipped)
    equipments = [
        # Firion's gear
        Equipment(name="Iron Helmet", type="HEAD", rating=5),
        Equipment(name="Chain Mail", type="CHEST", rating=12),
        Equipment(name="Steel Sword", type="PRIMARY_ARM", rating=10),
        Equipment(name="Wooden Shield", type="SECONDARY_ARM", rating=3),
        Equipment(name="Ring of Luck", type="ACCESSORY", rating=7),

        # Sabin's gear
        Equipment(name="Alchemist Hood", type="HEAD", rating=4),
        Equipment(name="Mystic Robe", type="CHEST", rating=9),
        Equipment(name="Crystal Staff", type="PRIMARY_ARM", rating=11),
        Equipment(name="Focus Orb", type="SECONDARY_ARM", rating=2),
        Equipment(name="Amulet of Healing", type="ACCESSORY", rating=8),

        # Balthier's gear
        Equipment(name="Engineer Goggles", type="HEAD", rating=3),
        Equipment(name="Utility Vest", type="CHEST", rating=7),
        Equipment(name="Titan Wrench", type="PRIMARY_ARM", rating=9),
        Equipment(name="Reinforced Bracer", type="SECONDARY_ARM", rating=4),
        Equipment(name="Pocket Compass", type="ACCESSORY", rating=5),

        # Locke's gear
        Equipment(name="Straw Hat", type="HEAD", rating=1),
        Equipment(name="Work Tunic", type="CHEST", rating=2),
        Equipment(name="Pitchfork", type="PRIMARY_ARM", rating=6),
        Equipment(name="Wooden Buckler", type="SECONDARY_ARM", rating=1),
        Equipment(name="Lucky Clover", type="ACCESSORY", rating=3),
    ]
    db.session.add_all(equipments)
    db.session.commit()


    # Assign equipments to each character (5 items each: head, chest, primary, secondary, accessory)
    firion = characters[0]
    sabin = characters[1]
    balthier = characters[2]
    locke = characters[3]

    char_equipments = [
        # Firion (indices 0-4)
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[0].id, slot="head"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[1].id, slot="chest"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[2].id, slot="right_hand"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[3].id, slot="left_hand"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[4].id, slot="accessory"),

        # Sabin (indices 5-9)
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[5].id, slot="head"),
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[6].id, slot="chest"),
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[7].id, slot="right_hand"),
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[8].id, slot="left_hand"),
        CharacterEquipment(character_id=sabin.id, equipment_id=equipments[9].id, slot="accessory"),

        # Balthier (indices 10-14)
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[10].id, slot="head"),
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[11].id, slot="chest"),
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[12].id, slot="right_hand"),
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[13].id, slot="left_hand"),
        CharacterEquipment(character_id=balthier.id, equipment_id=equipments[14].id, slot="accessory"),

        # Locke (indices 15-19)
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[15].id, slot="head"),
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[16].id, slot="chest"),
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[17].id, slot="right_hand"),
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[18].id, slot="left_hand"),
        CharacterEquipment(character_id=locke.id, equipment_id=equipments[19].id, slot="accessory"),
    ]
    db.session.add_all(char_equipments)
    db.session.commit()


    party_chars = [
        PartyCharacter(party_id=party.id, character_id=c.id, party_slot=i+1)
        for i, c in enumerate(characters)
    ]
    db.session.add_all(party_chars)
    db.session.commit()

    
    print("Seeding data inserted successfully")
