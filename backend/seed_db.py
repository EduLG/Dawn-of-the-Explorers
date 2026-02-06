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
        Character(name="Lenna", current_job_id=jobs[3].id),      # alchemist
        Character(name="Galuf", current_job_id=jobs[0].id),      # engineer
        Character(name="Farmer X", current_job_id=jobs[2].id)    # adventurer
    ]
    db.session.add_all(characters)
    db.session.commit()


    equipments = [
        Equipment(name="Iron Helmet", type="HEAD", rating=5),
        Equipment(name="Chain Mail", type="CHEST", rating=12),
        Equipment(name="Steel Sword", type="PRIMARY_ARM", rating=10),
        Equipment(name="Wooden Shield", type="SECONDARY_ARM", rating=3),
        Equipment(name="Ring of Luck", type="ACCESSORY", rating=7)
    ]
    db.session.add_all(equipments)
    db.session.commit()


    firion = characters[0]
    char_equipments = [
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[0].id, slot="head"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[1].id, slot="chest"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[2].id, slot="right_hand"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[3].id, slot="left_hand"),
        CharacterEquipment(character_id=firion.id, equipment_id=equipments[4].id, slot="accessory"),
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
