from app import create_app
from app.extensions import db
from werkzeug.security import generate_password_hash

from app.models.job import Job
from app.models.user import User
from app.models.party import Party
from app.models.character import Character
from app.models.equipment import Equipment
from app.models.dungeon import Dungeon

app = create_app()

with app.app_context():

    db.drop_all()
    db.create_all()

    # -------------------------------
    # Create user + party
    # -------------------------------
    user = User(
        username="eduladron",
        email="edu@example.com",
        password=generate_password_hash("12345678"),
    )
    db.session.add(user)
    db.session.flush()  # get user.id before creating Party

    party = Party(name="Heroes Party", level=1, experience=0, user_id=user.id)
    db.session.add(party)
    db.session.commit()

    # -------------------------------
    # Create second user without characters (for onboarding testing)
    # -------------------------------
    user2 = User(
        username="eduladron2",
        email="edu2@gmail.com",
        password=generate_password_hash("12345678"),
    )
    db.session.add(user2)
    db.session.flush()
    party2 = Party(name="Explorers party", level=1, experience=0, user_id=user2.id)
    db.session.add(party2)
    db.session.commit()

    # -------------------------------
    # Create jobs
    # -------------------------------
    job_names = [
        "engineer", "gunslinger", "adventurer", "alchemist",
        "warrior", "fender", "sage", "thief", "scholar", "beastmaster"
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
        # HEAD - T1 (rating 2)
        Equipment(name="Apprentice Goggles",    slot="head", rating=2,  equipment_type="cloth"),
        Equipment(name="Rawhide Cap",           slot="head", rating=2,  equipment_type="leather"),
        Equipment(name="Cloth Cap",             slot="head", rating=2,  equipment_type="leather"),
        Equipment(name="Apprentice's Cap",      slot="head", rating=2,  equipment_type="cloth"),
        Equipment(name="Iron Coif",             slot="head", rating=2,  equipment_type="plate"),
        Equipment(name="Sentry Cap",            slot="head", rating=2,  equipment_type="plate"),
        Equipment(name="Apprentice Hood",       slot="head", rating=2,  equipment_type="cloth"),
        Equipment(name="Rogue's Wrap",          slot="head", rating=2,  equipment_type="leather"),
        Equipment(name="Student's Cap",         slot="head", rating=2,  equipment_type="cloth"),
        Equipment(name="Pelt Cap",              slot="head", rating=2,  equipment_type="leather"),

        # HEAD - T2 (rating 5)
        Equipment(name="Workshop Goggles",      slot="head", rating=5,  equipment_type="cloth"),
        Equipment(name="Leather Cap",           slot="head", rating=5,  equipment_type="leather"),
        Equipment(name="Straw Hat",             slot="head", rating=5,  equipment_type="leather"),
        Equipment(name="Alchemist's Cap",       slot="head", rating=5,  equipment_type="cloth"),
        Equipment(name="Iron Helmet",           slot="head", rating=5,  equipment_type="plate"),
        Equipment(name="Guard's Helm",          slot="head", rating=5,  equipment_type="plate"),
        Equipment(name="Sage's Hood",           slot="head", rating=5,  equipment_type="cloth"),
        Equipment(name="Thief's Hood",          slot="head", rating=5,  equipment_type="leather"),
        Equipment(name="Researcher's Cap",      slot="head", rating=5,  equipment_type="cloth"),
        Equipment(name="Hunter's Cap",          slot="head", rating=5,  equipment_type="leather"),

        # HEAD - T3 (rating 9)
        Equipment(name="Tinkerer's Helm",       slot="head", rating=9,  equipment_type="cloth"),
        Equipment(name="Frontier Hat",          slot="head", rating=9,  equipment_type="leather"),
        Equipment(name="Adventurer's Hat",      slot="head", rating=9,  equipment_type="leather"),
        Equipment(name="Alchemist Hood",        slot="head", rating=9,  equipment_type="cloth"),
        Equipment(name="Steel Helmet",          slot="head", rating=9,  equipment_type="plate"),
        Equipment(name="Sentinel's Helm",       slot="head", rating=9,  equipment_type="plate"),
        Equipment(name="Mage's Cap",            slot="head", rating=9,  equipment_type="cloth"),
        Equipment(name="Shadow Hood",           slot="head", rating=9,  equipment_type="leather"),
        Equipment(name="Academic Hood",         slot="head", rating=9,  equipment_type="cloth"),
        Equipment(name="Feral Mask",            slot="head", rating=9,  equipment_type="leather"),

        # HEAD - T4 (rating 14)
        Equipment(name="Gear Cap",              slot="head", rating=14, equipment_type="cloth"),
        Equipment(name="Drifter's Brim",        slot="head", rating=14, equipment_type="leather"),
        Equipment(name="Traveler's Hood",       slot="head", rating=14, equipment_type="leather"),
        Equipment(name="Brew Master's Hat",     slot="head", rating=14, equipment_type="cloth"),
        Equipment(name="Knight's Visor",        slot="head", rating=14, equipment_type="plate"),
        Equipment(name="Vanguard's Helm",       slot="head", rating=14, equipment_type="plate"),
        Equipment(name="Arcanist's Hood",       slot="head", rating=14, equipment_type="cloth"),
        Equipment(name="Infiltrator's Mask",    slot="head", rating=14, equipment_type="leather"),
        Equipment(name="Scholar's Hat",         slot="head", rating=14, equipment_type="cloth"),
        Equipment(name="Wild Crown",            slot="head", rating=14, equipment_type="leather"),

        # HEAD - T5 (rating 20)
        Equipment(name="Engineer Goggles",      slot="head", rating=20, equipment_type="cloth"),
        Equipment(name="Sharpshooter's Cap",    slot="head", rating=20, equipment_type="leather"),
        Equipment(name="Scout's Helm",          slot="head", rating=20, equipment_type="leather"),
        Equipment(name="Mystic Hood",           slot="head", rating=20, equipment_type="cloth"),
        Equipment(name="Battle Helm",           slot="head", rating=20, equipment_type="plate"),
        Equipment(name="Defender's Plate",      slot="head", rating=20, equipment_type="plate"),
        Equipment(name="Mystic Turban",         slot="head", rating=20, equipment_type="cloth"),
        Equipment(name="Shadow Mask",           slot="head", rating=20, equipment_type="leather"),
        Equipment(name="Analyst's Visor",       slot="head", rating=20, equipment_type="cloth"),
        Equipment(name="Beast Mask",            slot="head", rating=20, equipment_type="leather"),

        # HEAD - T6 (rating 28)
        Equipment(name="Precision Visor",       slot="head", rating=28, equipment_type="cloth"),
        Equipment(name="Bounty Hunter's Hat",   slot="head", rating=28, equipment_type="leather"),
        Equipment(name="Pathfinder's Cap",      slot="head", rating=28, equipment_type="leather"),
        Equipment(name="Sage Veil",             slot="head", rating=28, equipment_type="cloth"),
        Equipment(name="Champion's Helm",       slot="head", rating=28, equipment_type="plate"),
        Equipment(name="Bulwark Helm",          slot="head", rating=28, equipment_type="plate"),
        Equipment(name="Elder's Hat",           slot="head", rating=28, equipment_type="cloth"),
        Equipment(name="Phantom Veil",          slot="head", rating=28, equipment_type="leather"),
        Equipment(name="Professor's Cap",       slot="head", rating=28, equipment_type="cloth"),
        Equipment(name="Alpha's Mark",          slot="head", rating=28, equipment_type="leather"),

        # HEAD - T7 (rating 38)
        Equipment(name="Iron Goggle Mk.II",     slot="head", rating=38, equipment_type="cloth"),
        Equipment(name="Outlaw's Brim",         slot="head", rating=38, equipment_type="leather"),
        Equipment(name="Explorer's Visor",      slot="head", rating=38, equipment_type="leather"),
        Equipment(name="Arcane Hood",           slot="head", rating=38, equipment_type="cloth"),
        Equipment(name="Templar Helmet",        slot="head", rating=38, equipment_type="plate"),
        Equipment(name="Fortress Helm",         slot="head", rating=38, equipment_type="plate"),
        Equipment(name="Ethereal Hood",         slot="head", rating=38, equipment_type="cloth"),
        Equipment(name="Nightwalker's Hood",    slot="head", rating=38, equipment_type="leather"),
        Equipment(name="Mastermind's Hood",     slot="head", rating=38, equipment_type="cloth"),
        Equipment(name="Beast Crown",           slot="head", rating=38, equipment_type="leather"),

        # HEAD - T8 (rating 50)
        Equipment(name="Mech Helm",             slot="head", rating=50, equipment_type="cloth"),
        Equipment(name="Marshal's Hat",         slot="head", rating=50, equipment_type="leather"),
        Equipment(name="Trailblazer's Helm",    slot="head", rating=50, equipment_type="leather"),
        Equipment(name="Arcane Circlet",        slot="head", rating=50, equipment_type="cloth"),
        Equipment(name="Warlord's Helm",        slot="head", rating=50, equipment_type="plate"),
        Equipment(name="Citadel Helm",          slot="head", rating=50, equipment_type="plate"),
        Equipment(name="Archmage's Cap",        slot="head", rating=50, equipment_type="cloth"),
        Equipment(name="Specter's Mask",        slot="head", rating=50, equipment_type="leather"),
        Equipment(name="Grand Scholar's Hat",   slot="head", rating=50, equipment_type="cloth"),
        Equipment(name="Warchief's Helm",       slot="head", rating=50, equipment_type="leather"),

        # HEAD - T9 (rating 65)
        Equipment(name="Servo Cranium",         slot="head", rating=65, equipment_type="cloth"),
        Equipment(name="Desperado's Crown",     slot="head", rating=65, equipment_type="leather"),
        Equipment(name="Wayfarer's Crown",      slot="head", rating=65, equipment_type="leather"),
        Equipment(name="Philosopher's Hat",     slot="head", rating=65, equipment_type="cloth"),
        Equipment(name="Dragon Helm",           slot="head", rating=65, equipment_type="plate"),
        Equipment(name="Bastion Crown",         slot="head", rating=65, equipment_type="plate"),
        Equipment(name="Celestial Hood",        slot="head", rating=65, equipment_type="cloth"),
        Equipment(name="Void Mask",             slot="head", rating=65, equipment_type="leather"),
        Equipment(name="Sage's Laurel",         slot="head", rating=65, equipment_type="cloth"),
        Equipment(name="Elder Beast Crown",     slot="head", rating=65, equipment_type="leather"),

        # HEAD - T10 (rating 82)
        Equipment(name="Neural Interface",      slot="head", rating=82, equipment_type="cloth"),
        Equipment(name="Legend's Hat",          slot="head", rating=82, equipment_type="leather"),
        Equipment(name="Explorer's Crown",      slot="head", rating=82, equipment_type="leather"),
        Equipment(name="Grand Alchemist's Crown", slot="head", rating=82, equipment_type="cloth"),
        Equipment(name="Legendary Helm",        slot="head", rating=82, equipment_type="plate"),
        Equipment(name="Aegis Helm",            slot="head", rating=82, equipment_type="plate"),
        Equipment(name="Divine Circlet",        slot="head", rating=82, equipment_type="cloth"),
        Equipment(name="Dark Assassin's Crown", slot="head", rating=82, equipment_type="leather"),
        Equipment(name="Omniscient's Crown",    slot="head", rating=82, equipment_type="cloth"),
        Equipment(name="Apex Predator's Crown", slot="head", rating=82, equipment_type="leather"),

        # CHEST - T1 (rating 2)
        Equipment(name="Work Vest",             slot="chest", rating=2,  equipment_type="cloth"),
        Equipment(name="Canvas Shirt",          slot="chest", rating=2,  equipment_type="leather"),
        Equipment(name="Cloth Tunic",           slot="chest", rating=2,  equipment_type="leather"),
        Equipment(name="Apprentice's Robe",     slot="chest", rating=2,  equipment_type="cloth"),
        Equipment(name="Padded Armor",          slot="chest", rating=2,  equipment_type="plate"),
        Equipment(name="Guard's Tunic",         slot="chest", rating=2,  equipment_type="plate"),
        Equipment(name="Simple Robe",           slot="chest", rating=2,  equipment_type="cloth"),
        Equipment(name="Rogue's Shirt",         slot="chest", rating=2,  equipment_type="leather"),
        Equipment(name="Student's Coat",        slot="chest", rating=2,  equipment_type="cloth"),
        Equipment(name="Pelt Shirt",            slot="chest", rating=2,  equipment_type="leather"),

        # CHEST - T2 (rating 5)
        Equipment(name="Utility Vest",          slot="chest", rating=5,  equipment_type="cloth"),
        Equipment(name="Leather Vest",          slot="chest", rating=5,  equipment_type="leather"),
        Equipment(name="Work Tunic",            slot="chest", rating=5,  equipment_type="leather"),
        Equipment(name="Scholar's Coat",        slot="chest", rating=5,  equipment_type="cloth"),
        Equipment(name="Chain Mail",            slot="chest", rating=5,  equipment_type="plate"),
        Equipment(name="Scale Armor",           slot="chest", rating=5,  equipment_type="plate"),
        Equipment(name="Sage's Robe",           slot="chest", rating=5,  equipment_type="cloth"),
        Equipment(name="Shadow Garb",           slot="chest", rating=5,  equipment_type="leather"),
        Equipment(name="Lab Coat",              slot="chest", rating=5,  equipment_type="cloth"),
        Equipment(name="Hide Vest",             slot="chest", rating=5,  equipment_type="leather"),

        # CHEST - T3 (rating 9)
        Equipment(name="Tinkerer's Coat",       slot="chest", rating=9,  equipment_type="cloth"),
        Equipment(name="Drifter's Shirt",       slot="chest", rating=9,  equipment_type="leather"),
        Equipment(name="Traveler's Shirt",      slot="chest", rating=9,  equipment_type="leather"),
        Equipment(name="Mystic Robe",           slot="chest", rating=9,  equipment_type="cloth"),
        Equipment(name="Scale Mail",            slot="chest", rating=9,  equipment_type="plate"),
        Equipment(name="Mail Coat",             slot="chest", rating=9,  equipment_type="plate"),
        Equipment(name="Mage's Coat",           slot="chest", rating=9,  equipment_type="cloth"),
        Equipment(name="Thief's Coat",          slot="chest", rating=9,  equipment_type="leather"),
        Equipment(name="Researcher's Coat",     slot="chest", rating=9,  equipment_type="cloth"),
        Equipment(name="Hunter's Coat",         slot="chest", rating=9,  equipment_type="leather"),

        # CHEST - T4 (rating 14)
        Equipment(name="Steam Vest",            slot="chest", rating=14, equipment_type="cloth"),
        Equipment(name="Frontier Coat",         slot="chest", rating=14, equipment_type="leather"),
        Equipment(name="Explorer's Tunic",      slot="chest", rating=14, equipment_type="leather"),
        Equipment(name="Alchemist's Coat",      slot="chest", rating=14, equipment_type="cloth"),
        Equipment(name="Plate Vest",            slot="chest", rating=14, equipment_type="plate"),
        Equipment(name="Sentinel's Plate",      slot="chest", rating=14, equipment_type="plate"),
        Equipment(name="Arcanist's Robe",       slot="chest", rating=14, equipment_type="cloth"),
        Equipment(name="Infiltrator's Vest",    slot="chest", rating=14, equipment_type="leather"),
        Equipment(name="Academic Robe",         slot="chest", rating=14, equipment_type="cloth"),
        Equipment(name="Feral Vest",            slot="chest", rating=14, equipment_type="leather"),

        # CHEST - T5 (rating 20)
        Equipment(name="Engineer's Coat",       slot="chest", rating=20, equipment_type="cloth"),
        Equipment(name="Duster Coat",           slot="chest", rating=20, equipment_type="leather"),
        Equipment(name="Scout's Vest",          slot="chest", rating=20, equipment_type="leather"),
        Equipment(name="Brew Master's Robe",    slot="chest", rating=20, equipment_type="cloth"),
        Equipment(name="Battle Plate",          slot="chest", rating=20, equipment_type="plate"),
        Equipment(name="Vanguard's Armor",      slot="chest", rating=20, equipment_type="plate"),
        Equipment(name="Ethereal Robe",         slot="chest", rating=20, equipment_type="cloth"),
        Equipment(name="Nightweave Shirt",      slot="chest", rating=20, equipment_type="leather"),
        Equipment(name="Analyst's Coat",        slot="chest", rating=20, equipment_type="cloth"),
        Equipment(name="Beastkin Coat",         slot="chest", rating=20, equipment_type="leather"),

        # CHEST - T6 (rating 28)
        Equipment(name="Gear Plate",            slot="chest", rating=28, equipment_type="cloth"),
        Equipment(name="Bounty Coat",           slot="chest", rating=28, equipment_type="leather"),
        Equipment(name="Pathfinder's Coat",     slot="chest", rating=28, equipment_type="leather"),
        Equipment(name="Alchemist's Mantle",    slot="chest", rating=28, equipment_type="cloth"),
        Equipment(name="Knight's Plate",        slot="chest", rating=28, equipment_type="plate"),
        Equipment(name="Bulwark Coat",          slot="chest", rating=28, equipment_type="plate"),
        Equipment(name="Elder's Mantle",        slot="chest", rating=28, equipment_type="cloth"),
        Equipment(name="Shadow Suit",           slot="chest", rating=28, equipment_type="leather"),
        Equipment(name="Professor's Coat",      slot="chest", rating=28, equipment_type="cloth"),
        Equipment(name="Pack Leader's Vest",    slot="chest", rating=28, equipment_type="leather"),

        # CHEST - T7 (rating 38)
        Equipment(name="Steam Coat",            slot="chest", rating=38, equipment_type="cloth"),
        Equipment(name="Outlaw's Coat",         slot="chest", rating=38, equipment_type="leather"),
        Equipment(name="Traveler's Coat",       slot="chest", rating=38, equipment_type="leather"),
        Equipment(name="Arcane Robe",           slot="chest", rating=38, equipment_type="cloth"),
        Equipment(name="Dragon Scale Mail",     slot="chest", rating=38, equipment_type="plate"),
        Equipment(name="Fortress Plate",        slot="chest", rating=38, equipment_type="plate"),
        Equipment(name="Arcane Mantle",         slot="chest", rating=38, equipment_type="cloth"),
        Equipment(name="Phantom Garb",          slot="chest", rating=38, equipment_type="leather"),
        Equipment(name="Scholar's Mantle",      slot="chest", rating=38, equipment_type="cloth"),
        Equipment(name="Alpha's Hide",          slot="chest", rating=38, equipment_type="leather"),

        # CHEST - T8 (rating 50)
        Equipment(name="Mech Suit",             slot="chest", rating=50, equipment_type="cloth"),
        Equipment(name="Marshal's Coat",        slot="chest", rating=50, equipment_type="leather"),
        Equipment(name="Trailblazer's Vest",    slot="chest", rating=50, equipment_type="leather"),
        Equipment(name="Philosopher's Robe",    slot="chest", rating=50, equipment_type="cloth"),
        Equipment(name="Templar Plate",         slot="chest", rating=50, equipment_type="plate"),
        Equipment(name="Citadel Armor",         slot="chest", rating=50, equipment_type="plate"),
        Equipment(name="Archmage's Robe",       slot="chest", rating=50, equipment_type="cloth"),
        Equipment(name="Nightweave Suit",       slot="chest", rating=50, equipment_type="leather"),
        Equipment(name="Grand Scholar's Coat",  slot="chest", rating=50, equipment_type="cloth"),
        Equipment(name="Warchief's Coat",       slot="chest", rating=50, equipment_type="leather"),

        # CHEST - T9 (rating 65)
        Equipment(name="Power Armor",           slot="chest", rating=65, equipment_type="cloth"),
        Equipment(name="Desperado's Vest",      slot="chest", rating=65, equipment_type="leather"),
        Equipment(name="Wayfarer's Coat",       slot="chest", rating=65, equipment_type="leather"),
        Equipment(name="Grand Alchemist's Robe", slot="chest", rating=65, equipment_type="cloth"),
        Equipment(name="Warlord's Plate",       slot="chest", rating=65, equipment_type="plate"),
        Equipment(name="Bastion Armor",         slot="chest", rating=65, equipment_type="plate"),
        Equipment(name="Celestial Mantle",      slot="chest", rating=65, equipment_type="cloth"),
        Equipment(name="Void Garb",             slot="chest", rating=65, equipment_type="leather"),
        Equipment(name="Master's Mantle",       slot="chest", rating=65, equipment_type="cloth"),
        Equipment(name="Elder Beast Hide",      slot="chest", rating=65, equipment_type="leather"),

        # CHEST - T10 (rating 82)
        Equipment(name="Power Suit",            slot="chest", rating=82, equipment_type="cloth"),
        Equipment(name="Legend's Coat",         slot="chest", rating=82, equipment_type="leather"),
        Equipment(name="Explorer's Plate",      slot="chest", rating=82, equipment_type="leather"),
        Equipment(name="Celestial Robe",        slot="chest", rating=82, equipment_type="cloth"),
        Equipment(name="Void Plate",            slot="chest", rating=82, equipment_type="plate"),
        Equipment(name="Aegis Plate",           slot="chest", rating=82, equipment_type="plate"),
        Equipment(name="Divine Robe",           slot="chest", rating=82, equipment_type="cloth"),
        Equipment(name="Dark Assassin's Suit",  slot="chest", rating=82, equipment_type="leather"),
        Equipment(name="Omniscient's Robe",     slot="chest", rating=82, equipment_type="cloth"),
        Equipment(name="Apex Predator's Coat",  slot="chest", rating=82, equipment_type="leather"),

        # PRIMARY HAND - T1 (rating 2)
        Equipment(name="Rusty Wrench",          slot="primary_hand", rating=2,  equipment_type="cloth"),
        Equipment(name="Broken Pistol",         slot="primary_hand", rating=2,  equipment_type="leather"),
        Equipment(name="Wooden Stick",          slot="primary_hand", rating=2,  equipment_type="leather"),
        Equipment(name="Apprentice's Wand",     slot="primary_hand", rating=2,  equipment_type="cloth"),
        Equipment(name="Training Sword",        slot="primary_hand", rating=2,  equipment_type="plate"),
        Equipment(name="Wooden Club",           slot="primary_hand", rating=2,  equipment_type="plate"),
        Equipment(name="Crooked Staff",         slot="primary_hand", rating=2,  equipment_type="cloth"),
        Equipment(name="Rusty Knife",           slot="primary_hand", rating=2,  equipment_type="leather"),
        Equipment(name="Field Notes",           slot="primary_hand", rating=2,  equipment_type="cloth"),
        Equipment(name="Rope Whip",             slot="primary_hand", rating=2,  equipment_type="leather"),

        # PRIMARY HAND - T2 (rating 5)
        Equipment(name="Iron Wrench",           slot="primary_hand", rating=5,  equipment_type="cloth"),
        Equipment(name="Flintlock",             slot="primary_hand", rating=5,  equipment_type="leather"),
        Equipment(name="Short Sword",           slot="primary_hand", rating=5,  equipment_type="leather"),
        Equipment(name="Crystal Wand",          slot="primary_hand", rating=5,  equipment_type="cloth"),
        Equipment(name="Iron Sword",            slot="primary_hand", rating=5,  equipment_type="plate"),
        Equipment(name="Iron Club",             slot="primary_hand", rating=5,  equipment_type="plate"),
        Equipment(name="Wooden Staff",          slot="primary_hand", rating=5,  equipment_type="cloth"),
        Equipment(name="Boot Knife",            slot="primary_hand", rating=5,  equipment_type="leather"),
        Equipment(name="Research Tome",         slot="primary_hand", rating=5,  equipment_type="cloth"),
        Equipment(name="Taming Whip",           slot="primary_hand", rating=5,  equipment_type="leather"),

        # PRIMARY HAND - T3 (rating 9)
        Equipment(name="Titan Wrench",          slot="primary_hand", rating=9,  equipment_type="cloth"),
        Equipment(name="Revolver",              slot="primary_hand", rating=9,  equipment_type="leather"),
        Equipment(name="Scout's Blade",         slot="primary_hand", rating=9,  equipment_type="leather"),
        Equipment(name="Crystal Staff",         slot="primary_hand", rating=9,  equipment_type="cloth"),
        Equipment(name="Steel Sword",           slot="primary_hand", rating=9,  equipment_type="plate"),
        Equipment(name="War Club",              slot="primary_hand", rating=9,  equipment_type="plate"),
        Equipment(name="Sage's Wand",           slot="primary_hand", rating=9,  equipment_type="cloth"),
        Equipment(name="Shadow Blade",          slot="primary_hand", rating=9,  equipment_type="leather"),
        Equipment(name="Analytical Lens",       slot="primary_hand", rating=9,  equipment_type="cloth"),
        Equipment(name="Beast Prod",            slot="primary_hand", rating=9,  equipment_type="leather"),

        # PRIMARY HAND - T4 (rating 14)
        Equipment(name="Gear Hammer",           slot="primary_hand", rating=14, equipment_type="cloth"),
        Equipment(name="Double Barrel",         slot="primary_hand", rating=14, equipment_type="leather"),
        Equipment(name="Traveler's Blade",      slot="primary_hand", rating=14, equipment_type="leather"),
        Equipment(name="Runic Rod",             slot="primary_hand", rating=14, equipment_type="cloth"),
        Equipment(name="Broad Sword",           slot="primary_hand", rating=14, equipment_type="plate"),
        Equipment(name="Iron Mace",             slot="primary_hand", rating=14, equipment_type="plate"),
        Equipment(name="Sage's Staff",          slot="primary_hand", rating=14, equipment_type="cloth"),
        Equipment(name="Twin Blades",           slot="primary_hand", rating=14, equipment_type="leather"),
        Equipment(name="Scholar's Tome",        slot="primary_hand", rating=14, equipment_type="cloth"),
        Equipment(name="Alpha Whip",            slot="primary_hand", rating=14, equipment_type="leather"),

        # PRIMARY HAND - T5 (rating 20)
        Equipment(name="Wrench Mk.II",          slot="primary_hand", rating=20, equipment_type="cloth"),
        Equipment(name="Revolver Mk.II",        slot="primary_hand", rating=20, equipment_type="leather"),
        Equipment(name="Adventurer's Blade",    slot="primary_hand", rating=20, equipment_type="leather"),
        Equipment(name="Golden Staff",          slot="primary_hand", rating=20, equipment_type="cloth"),
        Equipment(name="War Sword",             slot="primary_hand", rating=20, equipment_type="plate"),
        Equipment(name="War Axe",               slot="primary_hand", rating=20, equipment_type="plate"),
        Equipment(name="Elder Staff",           slot="primary_hand", rating=20, equipment_type="cloth"),
        Equipment(name="Shadow Daggers",        slot="primary_hand", rating=20, equipment_type="leather"),
        Equipment(name="Professor's Lens",      slot="primary_hand", rating=20, equipment_type="cloth"),
        Equipment(name="Feral Staff",           slot="primary_hand", rating=20, equipment_type="leather"),

        # PRIMARY HAND - T6 (rating 28)
        Equipment(name="Power Wrench",          slot="primary_hand", rating=28, equipment_type="cloth"),
        Equipment(name="Marksman's Rifle",      slot="primary_hand", rating=28, equipment_type="leather"),
        Equipment(name="Pathfinder's Blade",    slot="primary_hand", rating=28, equipment_type="leather"),
        Equipment(name="Arcane Rod",            slot="primary_hand", rating=28, equipment_type="cloth"),
        Equipment(name="Knight's Blade",        slot="primary_hand", rating=28, equipment_type="plate"),
        Equipment(name="Battle Axe",            slot="primary_hand", rating=28, equipment_type="plate"),
        Equipment(name="Arcane Staff",          slot="primary_hand", rating=28, equipment_type="cloth"),
        Equipment(name="Twin Daggers",          slot="primary_hand", rating=28, equipment_type="leather"),
        Equipment(name="Grand Tome",            slot="primary_hand", rating=28, equipment_type="cloth"),
        Equipment(name="Taming Staff",          slot="primary_hand", rating=28, equipment_type="leather"),

        # PRIMARY HAND - T7 (rating 38)
        Equipment(name="Plasma Wrench",         slot="primary_hand", rating=38, equipment_type="cloth"),
        Equipment(name="Repeating Rifle",       slot="primary_hand", rating=38, equipment_type="leather"),
        Equipment(name="Explorer's Blade",      slot="primary_hand", rating=38, equipment_type="leather"),
        Equipment(name="Staff of Mysteries",    slot="primary_hand", rating=38, equipment_type="cloth"),
        Equipment(name="Holy Sword",            slot="primary_hand", rating=38, equipment_type="plate"),
        Equipment(name="Great Axe",             slot="primary_hand", rating=38, equipment_type="plate"),
        Equipment(name="Ethereal Staff",        slot="primary_hand", rating=38, equipment_type="cloth"),
        Equipment(name="Phantom Blades",        slot="primary_hand", rating=38, equipment_type="leather"),
        Equipment(name="Mastermind's Lens",     slot="primary_hand", rating=38, equipment_type="cloth"),
        Equipment(name="Beast Caller Staff",    slot="primary_hand", rating=38, equipment_type="leather"),

        # PRIMARY HAND - T8 (rating 50)
        Equipment(name="Gear Cannon",           slot="primary_hand", rating=50, equipment_type="cloth"),
        Equipment(name="Thunder Gun",           slot="primary_hand", rating=50, equipment_type="leather"),
        Equipment(name="Trailblazer's Blade",   slot="primary_hand", rating=50, equipment_type="leather"),
        Equipment(name="Staff of Elements",     slot="primary_hand", rating=50, equipment_type="cloth"),
        Equipment(name="Champion's Blade",      slot="primary_hand", rating=50, equipment_type="plate"),
        Equipment(name="Warlord's Axe",         slot="primary_hand", rating=50, equipment_type="plate"),
        Equipment(name="Archmage's Staff",      slot="primary_hand", rating=50, equipment_type="cloth"),
        Equipment(name="Void Daggers",          slot="primary_hand", rating=50, equipment_type="leather"),
        Equipment(name="Grand Scholar's Lens",  slot="primary_hand", rating=50, equipment_type="cloth"),
        Equipment(name="Alpha Staff",           slot="primary_hand", rating=50, equipment_type="leather"),

        # PRIMARY HAND - T9 (rating 65)
        Equipment(name="Plasma Cutter",         slot="primary_hand", rating=65, equipment_type="cloth"),
        Equipment(name="Devastator",            slot="primary_hand", rating=65, equipment_type="leather"),
        Equipment(name="Wayfarer's Blade",      slot="primary_hand", rating=65, equipment_type="leather"),
        Equipment(name="Grand Staff",           slot="primary_hand", rating=65, equipment_type="cloth"),
        Equipment(name="Dragon Sword",          slot="primary_hand", rating=65, equipment_type="plate"),
        Equipment(name="Fortress Axe",          slot="primary_hand", rating=65, equipment_type="plate"),
        Equipment(name="Celestial Staff",       slot="primary_hand", rating=65, equipment_type="cloth"),
        Equipment(name="Specter's Blades",      slot="primary_hand", rating=65, equipment_type="leather"),
        Equipment(name="Omniscient Lens",       slot="primary_hand", rating=65, equipment_type="cloth"),
        Equipment(name="Elder Taming Staff",    slot="primary_hand", rating=65, equipment_type="leather"),

        # PRIMARY HAND - T10 (rating 82)
        Equipment(name="Neural Cannon",         slot="primary_hand", rating=82, equipment_type="cloth"),
        Equipment(name="Legend's Rifle",        slot="primary_hand", rating=82, equipment_type="leather"),
        Equipment(name="Vorpal Blade",          slot="primary_hand", rating=82, equipment_type="leather"),
        Equipment(name="Staff of Creation",     slot="primary_hand", rating=82, equipment_type="cloth"),
        Equipment(name="Excalibur",             slot="primary_hand", rating=82, equipment_type="plate"),
        Equipment(name="Aegis Axe",             slot="primary_hand", rating=82, equipment_type="plate"),
        Equipment(name="Divine Staff",          slot="primary_hand", rating=82, equipment_type="cloth"),
        Equipment(name="Dark Assassin's Blades", slot="primary_hand", rating=82, equipment_type="leather"),
        Equipment(name="Oracle's Lens",         slot="primary_hand", rating=82, equipment_type="cloth"),
        Equipment(name="Apex Predator's Staff", slot="primary_hand", rating=82, equipment_type="leather"),

        # SECONDARY HAND - T1 (rating 2)
        Equipment(name="Worn Bracer",           slot="secondary_hand", rating=2,  equipment_type="cloth"),
        Equipment(name="Powder Horn",           slot="secondary_hand", rating=2,  equipment_type="leather"),
        Equipment(name="Wooden Buckler",        slot="secondary_hand", rating=2,  equipment_type="leather"),
        Equipment(name="Focus Shard",           slot="secondary_hand", rating=2,  equipment_type="cloth"),
        Equipment(name="Wooden Shield",         slot="secondary_hand", rating=2,  equipment_type="plate"),
        Equipment(name="Cracked Shield",        slot="secondary_hand", rating=2,  equipment_type="plate"),
        Equipment(name="Dim Orb",               slot="secondary_hand", rating=2,  equipment_type="cloth"),
        Equipment(name="Smoke Pellet",          slot="secondary_hand", rating=2,  equipment_type="leather"),
        Equipment(name="Field Journal",         slot="secondary_hand", rating=2,  equipment_type="cloth"),
        Equipment(name="Beast Token",           slot="secondary_hand", rating=2,  equipment_type="leather"),

        # SECONDARY HAND - T2 (rating 5)
        Equipment(name="Reinforced Bracer",     slot="secondary_hand", rating=5,  equipment_type="cloth"),
        Equipment(name="Ammo Pouch",            slot="secondary_hand", rating=5,  equipment_type="leather"),
        Equipment(name="Wooden Targe",          slot="secondary_hand", rating=5,  equipment_type="leather"),
        Equipment(name="Focus Orb",             slot="secondary_hand", rating=5,  equipment_type="cloth"),
        Equipment(name="Iron Shield",           slot="secondary_hand", rating=5,  equipment_type="plate"),
        Equipment(name="Recruit's Shield",      slot="secondary_hand", rating=5,  equipment_type="plate"),
        Equipment(name="Spell Tome",            slot="secondary_hand", rating=5,  equipment_type="cloth"),
        Equipment(name="Throwing Knife",        slot="secondary_hand", rating=5,  equipment_type="leather"),
        Equipment(name="Research Journal",      slot="secondary_hand", rating=5,  equipment_type="cloth"),
        Equipment(name="Feather Totem",         slot="secondary_hand", rating=5,  equipment_type="leather"),

        # SECONDARY HAND - T3 (rating 9)
        Equipment(name="Tool Bracer",           slot="secondary_hand", rating=9,  equipment_type="cloth"),
        Equipment(name="Quick Draw Holster",    slot="secondary_hand", rating=9,  equipment_type="leather"),
        Equipment(name="Travel Shield",         slot="secondary_hand", rating=9,  equipment_type="leather"),
        Equipment(name="Mana Crystal",          slot="secondary_hand", rating=9,  equipment_type="cloth"),
        Equipment(name="Kite Shield",           slot="secondary_hand", rating=9,  equipment_type="plate"),
        Equipment(name="Sentinel Shield",       slot="secondary_hand", rating=9,  equipment_type="plate"),
        Equipment(name="Arcane Tome",           slot="secondary_hand", rating=9,  equipment_type="cloth"),
        Equipment(name="Smoke Bomb",            slot="secondary_hand", rating=9,  equipment_type="leather"),
        Equipment(name="Data Tablet",           slot="secondary_hand", rating=9,  equipment_type="cloth"),
        Equipment(name="Bone Totem",            slot="secondary_hand", rating=9,  equipment_type="leather"),

        # SECONDARY HAND - T4 (rating 14)
        Equipment(name="Gear Bracer",           slot="secondary_hand", rating=14, equipment_type="cloth"),
        Equipment(name="Off-hand Pistol",       slot="secondary_hand", rating=14, equipment_type="leather"),
        Equipment(name="Scout's Buckler",       slot="secondary_hand", rating=14, equipment_type="leather"),
        Equipment(name="Runic Crystal",         slot="secondary_hand", rating=14, equipment_type="cloth"),
        Equipment(name="Battle Shield",         slot="secondary_hand", rating=14, equipment_type="plate"),
        Equipment(name="Tower Shield",          slot="secondary_hand", rating=14, equipment_type="plate"),
        Equipment(name="Elder's Tome",          slot="secondary_hand", rating=14, equipment_type="cloth"),
        Equipment(name="Flash Bomb",            slot="secondary_hand", rating=14, equipment_type="leather"),
        Equipment(name="Annotated Tome",        slot="secondary_hand", rating=14, equipment_type="cloth"),
        Equipment(name="Pack Totem",            slot="secondary_hand", rating=14, equipment_type="leather"),

        # SECONDARY HAND - T5 (rating 20)
        Equipment(name="Steam Bracer",          slot="secondary_hand", rating=20, equipment_type="cloth"),
        Equipment(name="Bandolier",             slot="secondary_hand", rating=20, equipment_type="leather"),
        Equipment(name="Pathfinder's Shield",   slot="secondary_hand", rating=20, equipment_type="leather"),
        Equipment(name="Grand Crystal",         slot="secondary_hand", rating=20, equipment_type="cloth"),
        Equipment(name="Knight's Shield",       slot="secondary_hand", rating=20, equipment_type="plate"),
        Equipment(name="Bulwark Shield",        slot="secondary_hand", rating=20, equipment_type="plate"),
        Equipment(name="Mystic Orb",            slot="secondary_hand", rating=20, equipment_type="cloth"),
        Equipment(name="Poison Vial",           slot="secondary_hand", rating=20, equipment_type="leather"),
        Equipment(name="Professor's Journal",   slot="secondary_hand", rating=20, equipment_type="cloth"),
        Equipment(name="Alpha Totem",           slot="secondary_hand", rating=20, equipment_type="leather"),

        # SECONDARY HAND - T6 (rating 28)
        Equipment(name="Hydraulic Bracer",      slot="secondary_hand", rating=28, equipment_type="cloth"),
        Equipment(name="Marksman's Scope",      slot="secondary_hand", rating=28, equipment_type="leather"),
        Equipment(name="Explorer's Buckler",    slot="secondary_hand", rating=28, equipment_type="leather"),
        Equipment(name="Arcane Crystal",        slot="secondary_hand", rating=28, equipment_type="cloth"),
        Equipment(name="Champion's Shield",     slot="secondary_hand", rating=28, equipment_type="plate"),
        Equipment(name="Fortress Shield",       slot="secondary_hand", rating=28, equipment_type="plate"),
        Equipment(name="Arcane Orb",            slot="secondary_hand", rating=28, equipment_type="cloth"),
        Equipment(name="Shadow Bomb",           slot="secondary_hand", rating=28, equipment_type="leather"),
        Equipment(name="Grand Journal",         slot="secondary_hand", rating=28, equipment_type="cloth"),
        Equipment(name="Elder Totem",           slot="secondary_hand", rating=28, equipment_type="leather"),

        # SECONDARY HAND - T7 (rating 38)
        Equipment(name="Plasma Bracer",         slot="secondary_hand", rating=38, equipment_type="cloth"),
        Equipment(name="Eagle Eye Scope",       slot="secondary_hand", rating=38, equipment_type="leather"),
        Equipment(name="Trailblazer's Shield",  slot="secondary_hand", rating=38, equipment_type="leather"),
        Equipment(name="Ether Crystal",         slot="secondary_hand", rating=38, equipment_type="cloth"),
        Equipment(name="Templar Shield",        slot="secondary_hand", rating=38, equipment_type="plate"),
        Equipment(name="Citadel Shield",        slot="secondary_hand", rating=38, equipment_type="plate"),
        Equipment(name="Ethereal Orb",          slot="secondary_hand", rating=38, equipment_type="cloth"),
        Equipment(name="Void Bomb",             slot="secondary_hand", rating=38, equipment_type="leather"),
        Equipment(name="Mastermind's Journal",  slot="secondary_hand", rating=38, equipment_type="cloth"),
        Equipment(name="Spirit Totem",          slot="secondary_hand", rating=38, equipment_type="leather"),

        # SECONDARY HAND - T8 (rating 50)
        Equipment(name="Mech Bracer",           slot="secondary_hand", rating=50, equipment_type="cloth"),
        Equipment(name="Rapid Fire Module",     slot="secondary_hand", rating=50, equipment_type="leather"),
        Equipment(name="Wayfarer's Shield",     slot="secondary_hand", rating=50, equipment_type="leather"),
        Equipment(name="Philosopher's Orb",     slot="secondary_hand", rating=50, equipment_type="cloth"),
        Equipment(name="Warlord's Shield",      slot="secondary_hand", rating=50, equipment_type="plate"),
        Equipment(name="Aegis Shield",          slot="secondary_hand", rating=50, equipment_type="plate"),
        Equipment(name="Archmage's Orb",        slot="secondary_hand", rating=50, equipment_type="cloth"),
        Equipment(name="Specter's Bomb",        slot="secondary_hand", rating=50, equipment_type="leather"),
        Equipment(name="Grand Scholar's Journal", slot="secondary_hand", rating=50, equipment_type="cloth"),
        Equipment(name="Apex Totem",            slot="secondary_hand", rating=50, equipment_type="leather"),

        # SECONDARY HAND - T9 (rating 65)
        Equipment(name="Neural Bracer",         slot="secondary_hand", rating=65, equipment_type="cloth"),
        Equipment(name="Targeting System",      slot="secondary_hand", rating=65, equipment_type="leather"),
        Equipment(name="Explorer's Shield",     slot="secondary_hand", rating=65, equipment_type="leather"),
        Equipment(name="Grand Orb",             slot="secondary_hand", rating=65, equipment_type="cloth"),
        Equipment(name="Dragon Shield",         slot="secondary_hand", rating=65, equipment_type="plate"),
        Equipment(name="Bastion Shield",        slot="secondary_hand", rating=65, equipment_type="plate"),
        Equipment(name="Celestial Orb",         slot="secondary_hand", rating=65, equipment_type="cloth"),
        Equipment(name="Dark Bomb",             slot="secondary_hand", rating=65, equipment_type="leather"),
        Equipment(name="Omniscient Journal",    slot="secondary_hand", rating=65, equipment_type="cloth"),
        Equipment(name="Elder Spirit Totem",    slot="secondary_hand", rating=65, equipment_type="leather"),

        # SECONDARY HAND - T10 (rating 82)
        Equipment(name="Exo Bracer",            slot="secondary_hand", rating=82, equipment_type="cloth"),
        Equipment(name="Legend's Scope",        slot="secondary_hand", rating=82, equipment_type="leather"),
        Equipment(name="Legendary Buckler",     slot="secondary_hand", rating=82, equipment_type="leather"),
        Equipment(name="Cosmic Orb",            slot="secondary_hand", rating=82, equipment_type="cloth"),
        Equipment(name="Eternal Shield",        slot="secondary_hand", rating=82, equipment_type="plate"),
        Equipment(name="Divine Shield",         slot="secondary_hand", rating=82, equipment_type="plate"),
        Equipment(name="Divine Orb",            slot="secondary_hand", rating=82, equipment_type="cloth"),
        Equipment(name="Phantom Bomb",          slot="secondary_hand", rating=82, equipment_type="leather"),
        Equipment(name="Oracle's Journal",      slot="secondary_hand", rating=82, equipment_type="cloth"),
        Equipment(name="Apex Spirit Totem",     slot="secondary_hand", rating=82, equipment_type="leather"),

        # ACCESORY - T1 (rating 2)
        Equipment(name="Bent Cog",              slot="accesory", rating=2,  equipment_type="cloth"),
        Equipment(name="Copper Badge",          slot="accesory", rating=2,  equipment_type="leather"),
        Equipment(name="Lucky Pebble",          slot="accesory", rating=2,  equipment_type="leather"),
        Equipment(name="Empty Vial",            slot="accesory", rating=2,  equipment_type="cloth"),
        Equipment(name="Tin Ring",              slot="accesory", rating=2,  equipment_type="plate"),
        Equipment(name="Recruit's Insignia",    slot="accesory", rating=2,  equipment_type="plate"),
        Equipment(name="Dim Crystal",           slot="accesory", rating=2,  equipment_type="cloth"),
        Equipment(name="Shadow Token",          slot="accesory", rating=2,  equipment_type="leather"),
        Equipment(name="Student's Pin",         slot="accesory", rating=2,  equipment_type="cloth"),
        Equipment(name="Animal Claw",           slot="accesory", rating=2,  equipment_type="leather"),

        # ACCESORY - T2 (rating 5)
        Equipment(name="Pocket Compass",        slot="accesory", rating=5,  equipment_type="cloth"),
        Equipment(name="Sheriff's Badge",       slot="accesory", rating=5,  equipment_type="leather"),
        Equipment(name="Lucky Clover",          slot="accesory", rating=5,  equipment_type="leather"),
        Equipment(name="Elixir Vial",           slot="accesory", rating=5,  equipment_type="cloth"),
        Equipment(name="Iron Ring",             slot="accesory", rating=5,  equipment_type="plate"),
        Equipment(name="Guard's Insignia",      slot="accesory", rating=5,  equipment_type="plate"),
        Equipment(name="Spirit Pendant",        slot="accesory", rating=5,  equipment_type="cloth"),
        Equipment(name="Assassin's Mark",       slot="accesory", rating=5,  equipment_type="leather"),
        Equipment(name="Scholar's Pin",         slot="accesory", rating=5,  equipment_type="cloth"),
        Equipment(name="Beast Fang",            slot="accesory", rating=5,  equipment_type="leather"),

        # ACCESORY - T3 (rating 9)
        Equipment(name="Gear Token",            slot="accesory", rating=9,  equipment_type="cloth"),
        Equipment(name="Marksman's Badge",      slot="accesory", rating=9,  equipment_type="leather"),
        Equipment(name="Journey Stone",         slot="accesory", rating=9,  equipment_type="leather"),
        Equipment(name="Alchemist's Seal",      slot="accesory", rating=9,  equipment_type="cloth"),
        Equipment(name="Warrior's Band",        slot="accesory", rating=9,  equipment_type="plate"),
        Equipment(name="Sentinel's Medal",      slot="accesory", rating=9,  equipment_type="plate"),
        Equipment(name="Rune Pendant",          slot="accesory", rating=9,  equipment_type="cloth"),
        Equipment(name="Shadow Seal",           slot="accesory", rating=9,  equipment_type="leather"),
        Equipment(name="Research Medal",        slot="accesory", rating=9,  equipment_type="cloth"),
        Equipment(name="Pack Fang",             slot="accesory", rating=9,  equipment_type="leather"),

        # ACCESORY - T4 (rating 14)
        Equipment(name="Clockwork Charm",       slot="accesory", rating=14, equipment_type="cloth"),
        Equipment(name="Bounty Medal",          slot="accesory", rating=14, equipment_type="leather"),
        Equipment(name="Explorer's Charm",      slot="accesory", rating=14, equipment_type="leather"),
        Equipment(name="Mystic Vial",           slot="accesory", rating=14, equipment_type="cloth"),
        Equipment(name="Steel Ring",            slot="accesory", rating=14, equipment_type="plate"),
        Equipment(name="Vanguard's Medal",      slot="accesory", rating=14, equipment_type="plate"),
        Equipment(name="Mystic Pendant",        slot="accesory", rating=14, equipment_type="cloth"),
        Equipment(name="Phantom Seal",          slot="accesory", rating=14, equipment_type="leather"),
        Equipment(name="Academic Medal",        slot="accesory", rating=14, equipment_type="cloth"),
        Equipment(name="Alpha Fang",            slot="accesory", rating=14, equipment_type="leather"),

        # ACCESORY - T5 (rating 20)
        Equipment(name="Steam Cog",             slot="accesory", rating=20, equipment_type="cloth"),
        Equipment(name="Outlaw's Star",         slot="accesory", rating=20, equipment_type="leather"),
        Equipment(name="Pathfinder's Stone",    slot="accesory", rating=20, equipment_type="leather"),
        Equipment(name="Grand Vial",            slot="accesory", rating=20, equipment_type="cloth"),
        Equipment(name="Knight's Ring",         slot="accesory", rating=20, equipment_type="plate"),
        Equipment(name="Defender's Emblem",     slot="accesory", rating=20, equipment_type="plate"),
        Equipment(name="Arcane Pendant",        slot="accesory", rating=20, equipment_type="cloth"),
        Equipment(name="Night Seal",            slot="accesory", rating=20, equipment_type="leather"),
        Equipment(name="Professor's Medal",     slot="accesory", rating=20, equipment_type="cloth"),
        Equipment(name="Elder Fang",            slot="accesory", rating=20, equipment_type="leather"),

        # ACCESORY - T6 (rating 28)
        Equipment(name="Precision Cog",         slot="accesory", rating=28, equipment_type="cloth"),
        Equipment(name="Marshal's Star",        slot="accesory", rating=28, equipment_type="leather"),
        Equipment(name="Wayfarer's Charm",      slot="accesory", rating=28, equipment_type="leather"),
        Equipment(name="Arcane Vial",           slot="accesory", rating=28, equipment_type="cloth"),
        Equipment(name="Champion's Ring",       slot="accesory", rating=28, equipment_type="plate"),
        Equipment(name="Fortress Emblem",       slot="accesory", rating=28, equipment_type="plate"),
        Equipment(name="Elder Rune",            slot="accesory", rating=28, equipment_type="cloth"),
        Equipment(name="Void Seal",             slot="accesory", rating=28, equipment_type="leather"),
        Equipment(name="Grand Medal",           slot="accesory", rating=28, equipment_type="cloth"),
        Equipment(name="Alpha Claw",            slot="accesory", rating=28, equipment_type="leather"),

        # ACCESORY - T7 (rating 38)
        Equipment(name="Gear Core",             slot="accesory", rating=38, equipment_type="cloth"),
        Equipment(name="Desperado's Star",      slot="accesory", rating=38, equipment_type="leather"),
        Equipment(name="Trailblazer's Stone",   slot="accesory", rating=38, equipment_type="leather"),
        Equipment(name="Philosopher's Vial",    slot="accesory", rating=38, equipment_type="cloth"),
        Equipment(name="Templar's Ring",        slot="accesory", rating=38, equipment_type="plate"),
        Equipment(name="Citadel Emblem",        slot="accesory", rating=38, equipment_type="plate"),
        Equipment(name="Ethereal Rune",         slot="accesory", rating=38, equipment_type="cloth"),
        Equipment(name="Specter's Mark",        slot="accesory", rating=38, equipment_type="leather"),
        Equipment(name="Mastermind's Medal",    slot="accesory", rating=38, equipment_type="cloth"),
        Equipment(name="Spirit Claw",           slot="accesory", rating=38, equipment_type="leather"),

        # ACCESORY - T8 (rating 50)
        Equipment(name="Gravity Core",          slot="accesory", rating=50, equipment_type="cloth"),
        Equipment(name="Legend's Badge",        slot="accesory", rating=50, equipment_type="leather"),
        Equipment(name="Legendary Stone",       slot="accesory", rating=50, equipment_type="leather"),
        Equipment(name="Grand Alchemist's Vial", slot="accesory", rating=50, equipment_type="cloth"),
        Equipment(name="Warlord's Ring",        slot="accesory", rating=50, equipment_type="plate"),
        Equipment(name="Bastion Emblem",        slot="accesory", rating=50, equipment_type="plate"),
        Equipment(name="Celestial Rune",        slot="accesory", rating=50, equipment_type="cloth"),
        Equipment(name="Dark Seal",             slot="accesory", rating=50, equipment_type="leather"),
        Equipment(name="Grand Scholar's Medal", slot="accesory", rating=50, equipment_type="cloth"),
        Equipment(name="Apex Claw",             slot="accesory", rating=50, equipment_type="leather"),

        # ACCESORY - T9 (rating 65)
        Equipment(name="Neural Core",           slot="accesory", rating=65, equipment_type="cloth"),
        Equipment(name="Myth Badge",            slot="accesory", rating=65, equipment_type="leather"),
        Equipment(name="Ancient Stone",         slot="accesory", rating=65, equipment_type="leather"),
        Equipment(name="Cosmic Vial",           slot="accesory", rating=65, equipment_type="cloth"),
        Equipment(name="Dragon Ring",           slot="accesory", rating=65, equipment_type="plate"),
        Equipment(name="Citadel Crest",         slot="accesory", rating=65, equipment_type="plate"),
        Equipment(name="Divine Rune",           slot="accesory", rating=65, equipment_type="cloth"),
        Equipment(name="Phantom Mark",          slot="accesory", rating=65, equipment_type="leather"),
        Equipment(name="Omniscient Medal",      slot="accesory", rating=65, equipment_type="cloth"),
        Equipment(name="Elder Spirit Claw",     slot="accesory", rating=65, equipment_type="leather"),

        # ACCESORY - T10 (rating 82)
        Equipment(name="Omega Core",            slot="accesory", rating=82, equipment_type="cloth"),
        Equipment(name="Legend's Medallion",    slot="accesory", rating=82, equipment_type="leather"),
        Equipment(name="Explorer's Relic",      slot="accesory", rating=82, equipment_type="leather"),
        Equipment(name="Philosopher's Stone",   slot="accesory", rating=82, equipment_type="cloth"),
        Equipment(name="Legendary Ring",        slot="accesory", rating=82, equipment_type="plate"),
        Equipment(name="Aegis Crest",           slot="accesory", rating=82, equipment_type="plate"),
        Equipment(name="Cosmic Pendant",        slot="accesory", rating=82, equipment_type="cloth"),
        Equipment(name="Dark Assassin's Seal",  slot="accesory", rating=82, equipment_type="leather"),
        Equipment(name="Oracle's Medal",        slot="accesory", rating=82, equipment_type="cloth"),
        Equipment(name="Apex Predator's Fang",  slot="accesory", rating=82, equipment_type="leather"),
    ]
    db.session.add_all(equipments)
    db.session.commit()

    # -------------------------------
    # Seed dungeons
    # -------------------------------
    # Loot index formula: type_base + (tier-1)*10 + job_index
    # type_base → H=0  C=100  P=200  S=300  A=400
    # job_index → eng=0 gun=1 adv=2 alc=3 war=4 fen=5 sag=6 ass=7 sch=8 bst=9
    H, C, P, S, A = 0, 100, 200, 300, 400

    def tier_loot(t):
        """Returns all 50 item IDs (5 slots × 10 jobs) for the given tier."""
        return [
            equipments[base + (t - 1) * 10 + job].id
            for base in [H, C, P, S, A]
            for job in range(10)
        ]

    dungeons = [
        Dungeon(
            name="Primeval Dense Forest",
            description="Vast woodland of ancient trees, narrow rivers and mist-covered clearings.",
            image_path="/localizations/forest_1.png",
            rating=40,   min_rating=0,   visibility_rating=0,   duration=20,
            loot=tier_loot(1),
        ),
        Dungeon(
            name="The Infinite Observation Tower",
            description="Colossal vertical structure that pierces the clouds and vanishes into the sky.",
            image_path="/localizations/tower_2.png",
            rating=100,  min_rating=24,  visibility_rating=0,   duration=300,
            loot=tier_loot(2),
        ),
        Dungeon(
            name="Canyon of Eternal Storms",
            description="Deep rocky rift with sheer walls and violent air currents.",
            image_path="/localizations/canyon_3.png",
            rating=180,  min_rating=60,  visibility_rating=24,  duration=1200,
            loot=tier_loot(3),
        ),
        Dungeon(
            name="Archipelago of Wandering Clouds",
            description="Collection of floating islands suspended above a sea of clouds.",
            image_path="/localizations/archipelago_4.png",
            rating=280,  min_rating=108, visibility_rating=60,  duration=2700,
            loot=tier_loot(4),
        ),
        Dungeon(
            name="Abyssal Steam Pit",
            description="Enormous geothermal rift descending into the earth's crust.",
            image_path="/localizations/pit_5.png",
            rating=400,  min_rating=168, visibility_rating=108, duration=3600,
            loot=tier_loot(5),
        ),
        Dungeon(
            name="Sunken Bronze City",
            description="Ruins of an ancient technological metropolis beneath dense, dark waters.",
            image_path="/localizations/sunken_6.png",
            rating=560,  min_rating=240, visibility_rating=168, duration=6300,
            loot=tier_loot(6),
        ),
        Dungeon(
            name="Isle of the Fallen Engineers",
            description="Rocky island overrun by abandoned factories and ruined laboratories.",
            image_path="/localizations/engineers_7.png",
            rating=760,  min_rating=336, visibility_rating=240, duration=10800,
            loot=tier_loot(7),
        ),
        Dungeon(
            name="Resonant Crystal Desert",
            description="Vast expanse of dunes formed by fragments of translucent crystal.",
            image_path="/localizations/desert_8.png",
            rating=1000, min_rating=456, visibility_rating=336, duration=18000,
            loot=tier_loot(8),
        ),
        Dungeon(
            name="Airship Graveyard",
            description="Plains covered by the wreckage of crashed zeppelins and airships.",
            image_path="/localizations/graveyard_9.png",
            rating=1300, min_rating=600, visibility_rating=456, duration=28800,
            loot=tier_loot(9),
        ),
        Dungeon(
            name="Etherized Caldera Volcano",
            description="Active volcano with a wide caldera surrounded by lava flows.",
            image_path="/localizations/volcano_10.png",
            rating=1640, min_rating=780, visibility_rating=600, duration=43200,
            loot=tier_loot(10),
        ),
        Dungeon(
            name="Ether Core",
            description="Colossal cavity at the planet's core where the world's energy converges.",
            image_path="/localizations/core_11.png",
            rating=1640, min_rating=984, visibility_rating=780, duration=86400,
            loot=[],
        ),
    ]
    db.session.add_all(dungeons)
    db.session.commit()

    print("Seeding data inserted successfully")
