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
        # HEAD - T1 (rating 2)
        Equipment(name="Apprentice Goggles",    type="head", rating=2,  job_id=jobs[0].id),
        Equipment(name="Rawhide Cap",           type="head", rating=2,  job_id=jobs[1].id),
        Equipment(name="Cloth Cap",             type="head", rating=2,  job_id=jobs[2].id),
        Equipment(name="Apprentice's Cap",      type="head", rating=2,  job_id=jobs[3].id),
        Equipment(name="Iron Coif",             type="head", rating=2,  job_id=jobs[4].id),
        Equipment(name="Sentry Cap",            type="head", rating=2,  job_id=jobs[5].id),
        Equipment(name="Apprentice Hood",       type="head", rating=2,  job_id=jobs[6].id),
        Equipment(name="Rogue's Wrap",          type="head", rating=2,  job_id=jobs[7].id),
        Equipment(name="Student's Cap",         type="head", rating=2,  job_id=jobs[8].id),
        Equipment(name="Pelt Cap",              type="head", rating=2,  job_id=jobs[9].id),

        # HEAD - T2 (rating 5)
        Equipment(name="Workshop Goggles",      type="head", rating=5,  job_id=jobs[0].id),
        Equipment(name="Leather Cap",           type="head", rating=5,  job_id=jobs[1].id),
        Equipment(name="Straw Hat",             type="head", rating=5,  job_id=jobs[2].id),
        Equipment(name="Alchemist's Cap",       type="head", rating=5,  job_id=jobs[3].id),
        Equipment(name="Iron Helmet",           type="head", rating=5,  job_id=jobs[4].id),
        Equipment(name="Guard's Helm",          type="head", rating=5,  job_id=jobs[5].id),
        Equipment(name="Sage's Hood",           type="head", rating=5,  job_id=jobs[6].id),
        Equipment(name="Thief's Hood",          type="head", rating=5,  job_id=jobs[7].id),
        Equipment(name="Researcher's Cap",      type="head", rating=5,  job_id=jobs[8].id),
        Equipment(name="Hunter's Cap",          type="head", rating=5,  job_id=jobs[9].id),

        # HEAD - T3 (rating 9)
        Equipment(name="Tinkerer's Helm",       type="head", rating=9,  job_id=jobs[0].id),
        Equipment(name="Frontier Hat",          type="head", rating=9,  job_id=jobs[1].id),
        Equipment(name="Adventurer's Hat",      type="head", rating=9,  job_id=jobs[2].id),
        Equipment(name="Alchemist Hood",        type="head", rating=9,  job_id=jobs[3].id),
        Equipment(name="Steel Helmet",          type="head", rating=9,  job_id=jobs[4].id),
        Equipment(name="Sentinel's Helm",       type="head", rating=9,  job_id=jobs[5].id),
        Equipment(name="Mage's Cap",            type="head", rating=9,  job_id=jobs[6].id),
        Equipment(name="Shadow Hood",           type="head", rating=9,  job_id=jobs[7].id),
        Equipment(name="Academic Hood",         type="head", rating=9,  job_id=jobs[8].id),
        Equipment(name="Feral Mask",            type="head", rating=9,  job_id=jobs[9].id),

        # HEAD - T4 (rating 14)
        Equipment(name="Gear Cap",              type="head", rating=14, job_id=jobs[0].id),
        Equipment(name="Drifter's Brim",        type="head", rating=14, job_id=jobs[1].id),
        Equipment(name="Traveler's Hood",       type="head", rating=14, job_id=jobs[2].id),
        Equipment(name="Brew Master's Hat",     type="head", rating=14, job_id=jobs[3].id),
        Equipment(name="Knight's Visor",        type="head", rating=14, job_id=jobs[4].id),
        Equipment(name="Vanguard's Helm",       type="head", rating=14, job_id=jobs[5].id),
        Equipment(name="Arcanist's Hood",       type="head", rating=14, job_id=jobs[6].id),
        Equipment(name="Infiltrator's Mask",    type="head", rating=14, job_id=jobs[7].id),
        Equipment(name="Scholar's Hat",         type="head", rating=14, job_id=jobs[8].id),
        Equipment(name="Wild Crown",            type="head", rating=14, job_id=jobs[9].id),

        # HEAD - T5 (rating 20)
        Equipment(name="Engineer Goggles",      type="head", rating=20, job_id=jobs[0].id),
        Equipment(name="Sharpshooter's Cap",    type="head", rating=20, job_id=jobs[1].id),
        Equipment(name="Scout's Helm",          type="head", rating=20, job_id=jobs[2].id),
        Equipment(name="Mystic Hood",           type="head", rating=20, job_id=jobs[3].id),
        Equipment(name="Battle Helm",           type="head", rating=20, job_id=jobs[4].id),
        Equipment(name="Defender's Plate",      type="head", rating=20, job_id=jobs[5].id),
        Equipment(name="Mystic Turban",         type="head", rating=20, job_id=jobs[6].id),
        Equipment(name="Shadow Mask",           type="head", rating=20, job_id=jobs[7].id),
        Equipment(name="Analyst's Visor",       type="head", rating=20, job_id=jobs[8].id),
        Equipment(name="Beast Mask",            type="head", rating=20, job_id=jobs[9].id),

        # HEAD - T6 (rating 28)
        Equipment(name="Precision Visor",       type="head", rating=28, job_id=jobs[0].id),
        Equipment(name="Bounty Hunter's Hat",   type="head", rating=28, job_id=jobs[1].id),
        Equipment(name="Pathfinder's Cap",      type="head", rating=28, job_id=jobs[2].id),
        Equipment(name="Sage Veil",             type="head", rating=28, job_id=jobs[3].id),
        Equipment(name="Champion's Helm",       type="head", rating=28, job_id=jobs[4].id),
        Equipment(name="Bulwark Helm",          type="head", rating=28, job_id=jobs[5].id),
        Equipment(name="Elder's Hat",           type="head", rating=28, job_id=jobs[6].id),
        Equipment(name="Phantom Veil",          type="head", rating=28, job_id=jobs[7].id),
        Equipment(name="Professor's Cap",       type="head", rating=28, job_id=jobs[8].id),
        Equipment(name="Alpha's Mark",          type="head", rating=28, job_id=jobs[9].id),

        # HEAD - T7 (rating 38)
        Equipment(name="Iron Goggle Mk.II",     type="head", rating=38, job_id=jobs[0].id),
        Equipment(name="Outlaw's Brim",         type="head", rating=38, job_id=jobs[1].id),
        Equipment(name="Explorer's Visor",      type="head", rating=38, job_id=jobs[2].id),
        Equipment(name="Arcane Hood",           type="head", rating=38, job_id=jobs[3].id),
        Equipment(name="Templar Helmet",        type="head", rating=38, job_id=jobs[4].id),
        Equipment(name="Fortress Helm",         type="head", rating=38, job_id=jobs[5].id),
        Equipment(name="Ethereal Hood",         type="head", rating=38, job_id=jobs[6].id),
        Equipment(name="Nightwalker's Hood",    type="head", rating=38, job_id=jobs[7].id),
        Equipment(name="Mastermind's Hood",     type="head", rating=38, job_id=jobs[8].id),
        Equipment(name="Beast Crown",           type="head", rating=38, job_id=jobs[9].id),

        # HEAD - T8 (rating 50)
        Equipment(name="Mech Helm",             type="head", rating=50, job_id=jobs[0].id),
        Equipment(name="Marshal's Hat",         type="head", rating=50, job_id=jobs[1].id),
        Equipment(name="Trailblazer's Helm",    type="head", rating=50, job_id=jobs[2].id),
        Equipment(name="Arcane Circlet",        type="head", rating=50, job_id=jobs[3].id),
        Equipment(name="Warlord's Helm",        type="head", rating=50, job_id=jobs[4].id),
        Equipment(name="Citadel Helm",          type="head", rating=50, job_id=jobs[5].id),
        Equipment(name="Archmage's Cap",        type="head", rating=50, job_id=jobs[6].id),
        Equipment(name="Specter's Mask",        type="head", rating=50, job_id=jobs[7].id),
        Equipment(name="Grand Scholar's Hat",   type="head", rating=50, job_id=jobs[8].id),
        Equipment(name="Warchief's Helm",       type="head", rating=50, job_id=jobs[9].id),

        # HEAD - T9 (rating 65)
        Equipment(name="Servo Cranium",         type="head", rating=65, job_id=jobs[0].id),
        Equipment(name="Desperado's Crown",     type="head", rating=65, job_id=jobs[1].id),
        Equipment(name="Wayfarer's Crown",      type="head", rating=65, job_id=jobs[2].id),
        Equipment(name="Philosopher's Hat",     type="head", rating=65, job_id=jobs[3].id),
        Equipment(name="Dragon Helm",           type="head", rating=65, job_id=jobs[4].id),
        Equipment(name="Bastion Crown",         type="head", rating=65, job_id=jobs[5].id),
        Equipment(name="Celestial Hood",        type="head", rating=65, job_id=jobs[6].id),
        Equipment(name="Void Mask",             type="head", rating=65, job_id=jobs[7].id),
        Equipment(name="Sage's Laurel",         type="head", rating=65, job_id=jobs[8].id),
        Equipment(name="Elder Beast Crown",     type="head", rating=65, job_id=jobs[9].id),

        # HEAD - T10 (rating 82)
        Equipment(name="Neural Interface",      type="head", rating=82, job_id=jobs[0].id),
        Equipment(name="Legend's Hat",          type="head", rating=82, job_id=jobs[1].id),
        Equipment(name="Explorer's Crown",      type="head", rating=82, job_id=jobs[2].id),
        Equipment(name="Grand Alchemist's Crown", type="head", rating=82, job_id=jobs[3].id),
        Equipment(name="Legendary Helm",        type="head", rating=82, job_id=jobs[4].id),
        Equipment(name="Aegis Helm",            type="head", rating=82, job_id=jobs[5].id),
        Equipment(name="Divine Circlet",        type="head", rating=82, job_id=jobs[6].id),
        Equipment(name="Dark Assassin's Crown", type="head", rating=82, job_id=jobs[7].id),
        Equipment(name="Omniscient's Crown",    type="head", rating=82, job_id=jobs[8].id),
        Equipment(name="Apex Predator's Crown", type="head", rating=82, job_id=jobs[9].id),

        # CHEST - T1 (rating 2)
        Equipment(name="Work Vest",             type="chest", rating=2,  job_id=jobs[0].id),
        Equipment(name="Canvas Shirt",          type="chest", rating=2,  job_id=jobs[1].id),
        Equipment(name="Cloth Tunic",           type="chest", rating=2,  job_id=jobs[2].id),
        Equipment(name="Apprentice's Robe",     type="chest", rating=2,  job_id=jobs[3].id),
        Equipment(name="Padded Armor",          type="chest", rating=2,  job_id=jobs[4].id),
        Equipment(name="Guard's Tunic",         type="chest", rating=2,  job_id=jobs[5].id),
        Equipment(name="Simple Robe",           type="chest", rating=2,  job_id=jobs[6].id),
        Equipment(name="Rogue's Shirt",         type="chest", rating=2,  job_id=jobs[7].id),
        Equipment(name="Student's Coat",        type="chest", rating=2,  job_id=jobs[8].id),
        Equipment(name="Pelt Shirt",            type="chest", rating=2,  job_id=jobs[9].id),

        # CHEST - T2 (rating 5)
        Equipment(name="Utility Vest",          type="chest", rating=5,  job_id=jobs[0].id),
        Equipment(name="Leather Vest",          type="chest", rating=5,  job_id=jobs[1].id),
        Equipment(name="Work Tunic",            type="chest", rating=5,  job_id=jobs[2].id),
        Equipment(name="Scholar's Coat",        type="chest", rating=5,  job_id=jobs[3].id),
        Equipment(name="Chain Mail",            type="chest", rating=5,  job_id=jobs[4].id),
        Equipment(name="Scale Armor",           type="chest", rating=5,  job_id=jobs[5].id),
        Equipment(name="Sage's Robe",           type="chest", rating=5,  job_id=jobs[6].id),
        Equipment(name="Shadow Garb",           type="chest", rating=5,  job_id=jobs[7].id),
        Equipment(name="Lab Coat",              type="chest", rating=5,  job_id=jobs[8].id),
        Equipment(name="Hide Vest",             type="chest", rating=5,  job_id=jobs[9].id),

        # CHEST - T3 (rating 9)
        Equipment(name="Tinkerer's Coat",       type="chest", rating=9,  job_id=jobs[0].id),
        Equipment(name="Drifter's Shirt",       type="chest", rating=9,  job_id=jobs[1].id),
        Equipment(name="Traveler's Shirt",      type="chest", rating=9,  job_id=jobs[2].id),
        Equipment(name="Mystic Robe",           type="chest", rating=9,  job_id=jobs[3].id),
        Equipment(name="Scale Mail",            type="chest", rating=9,  job_id=jobs[4].id),
        Equipment(name="Mail Coat",             type="chest", rating=9,  job_id=jobs[5].id),
        Equipment(name="Mage's Coat",           type="chest", rating=9,  job_id=jobs[6].id),
        Equipment(name="Thief's Coat",          type="chest", rating=9,  job_id=jobs[7].id),
        Equipment(name="Researcher's Coat",     type="chest", rating=9,  job_id=jobs[8].id),
        Equipment(name="Hunter's Coat",         type="chest", rating=9,  job_id=jobs[9].id),

        # CHEST - T4 (rating 14)
        Equipment(name="Steam Vest",            type="chest", rating=14, job_id=jobs[0].id),
        Equipment(name="Frontier Coat",         type="chest", rating=14, job_id=jobs[1].id),
        Equipment(name="Explorer's Tunic",      type="chest", rating=14, job_id=jobs[2].id),
        Equipment(name="Alchemist's Coat",      type="chest", rating=14, job_id=jobs[3].id),
        Equipment(name="Plate Vest",            type="chest", rating=14, job_id=jobs[4].id),
        Equipment(name="Sentinel's Plate",      type="chest", rating=14, job_id=jobs[5].id),
        Equipment(name="Arcanist's Robe",       type="chest", rating=14, job_id=jobs[6].id),
        Equipment(name="Infiltrator's Vest",    type="chest", rating=14, job_id=jobs[7].id),
        Equipment(name="Academic Robe",         type="chest", rating=14, job_id=jobs[8].id),
        Equipment(name="Feral Vest",            type="chest", rating=14, job_id=jobs[9].id),

        # CHEST - T5 (rating 20)
        Equipment(name="Engineer's Coat",       type="chest", rating=20, job_id=jobs[0].id),
        Equipment(name="Duster Coat",           type="chest", rating=20, job_id=jobs[1].id),
        Equipment(name="Scout's Vest",          type="chest", rating=20, job_id=jobs[2].id),
        Equipment(name="Brew Master's Robe",    type="chest", rating=20, job_id=jobs[3].id),
        Equipment(name="Battle Plate",          type="chest", rating=20, job_id=jobs[4].id),
        Equipment(name="Vanguard's Armor",      type="chest", rating=20, job_id=jobs[5].id),
        Equipment(name="Ethereal Robe",         type="chest", rating=20, job_id=jobs[6].id),
        Equipment(name="Nightweave Shirt",      type="chest", rating=20, job_id=jobs[7].id),
        Equipment(name="Analyst's Coat",        type="chest", rating=20, job_id=jobs[8].id),
        Equipment(name="Beastkin Coat",         type="chest", rating=20, job_id=jobs[9].id),

        # CHEST - T6 (rating 28)
        Equipment(name="Gear Plate",            type="chest", rating=28, job_id=jobs[0].id),
        Equipment(name="Bounty Coat",           type="chest", rating=28, job_id=jobs[1].id),
        Equipment(name="Pathfinder's Coat",     type="chest", rating=28, job_id=jobs[2].id),
        Equipment(name="Alchemist's Mantle",    type="chest", rating=28, job_id=jobs[3].id),
        Equipment(name="Knight's Plate",        type="chest", rating=28, job_id=jobs[4].id),
        Equipment(name="Bulwark Coat",          type="chest", rating=28, job_id=jobs[5].id),
        Equipment(name="Elder's Mantle",        type="chest", rating=28, job_id=jobs[6].id),
        Equipment(name="Shadow Suit",           type="chest", rating=28, job_id=jobs[7].id),
        Equipment(name="Professor's Coat",      type="chest", rating=28, job_id=jobs[8].id),
        Equipment(name="Pack Leader's Vest",    type="chest", rating=28, job_id=jobs[9].id),

        # CHEST - T7 (rating 38)
        Equipment(name="Steam Coat",            type="chest", rating=38, job_id=jobs[0].id),
        Equipment(name="Outlaw's Coat",         type="chest", rating=38, job_id=jobs[1].id),
        Equipment(name="Traveler's Coat",       type="chest", rating=38, job_id=jobs[2].id),
        Equipment(name="Arcane Robe",           type="chest", rating=38, job_id=jobs[3].id),
        Equipment(name="Dragon Scale Mail",     type="chest", rating=38, job_id=jobs[4].id),
        Equipment(name="Fortress Plate",        type="chest", rating=38, job_id=jobs[5].id),
        Equipment(name="Arcane Mantle",         type="chest", rating=38, job_id=jobs[6].id),
        Equipment(name="Phantom Garb",          type="chest", rating=38, job_id=jobs[7].id),
        Equipment(name="Scholar's Mantle",      type="chest", rating=38, job_id=jobs[8].id),
        Equipment(name="Alpha's Hide",          type="chest", rating=38, job_id=jobs[9].id),

        # CHEST - T8 (rating 50)
        Equipment(name="Mech Suit",             type="chest", rating=50, job_id=jobs[0].id),
        Equipment(name="Marshal's Coat",        type="chest", rating=50, job_id=jobs[1].id),
        Equipment(name="Trailblazer's Vest",    type="chest", rating=50, job_id=jobs[2].id),
        Equipment(name="Philosopher's Robe",    type="chest", rating=50, job_id=jobs[3].id),
        Equipment(name="Templar Plate",         type="chest", rating=50, job_id=jobs[4].id),
        Equipment(name="Citadel Armor",         type="chest", rating=50, job_id=jobs[5].id),
        Equipment(name="Archmage's Robe",       type="chest", rating=50, job_id=jobs[6].id),
        Equipment(name="Nightweave Suit",       type="chest", rating=50, job_id=jobs[7].id),
        Equipment(name="Grand Scholar's Coat",  type="chest", rating=50, job_id=jobs[8].id),
        Equipment(name="Warchief's Coat",       type="chest", rating=50, job_id=jobs[9].id),

        # CHEST - T9 (rating 65)
        Equipment(name="Power Armor",           type="chest", rating=65, job_id=jobs[0].id),
        Equipment(name="Desperado's Vest",      type="chest", rating=65, job_id=jobs[1].id),
        Equipment(name="Wayfarer's Coat",       type="chest", rating=65, job_id=jobs[2].id),
        Equipment(name="Grand Alchemist's Robe", type="chest", rating=65, job_id=jobs[3].id),
        Equipment(name="Warlord's Plate",       type="chest", rating=65, job_id=jobs[4].id),
        Equipment(name="Bastion Armor",         type="chest", rating=65, job_id=jobs[5].id),
        Equipment(name="Celestial Mantle",      type="chest", rating=65, job_id=jobs[6].id),
        Equipment(name="Void Garb",             type="chest", rating=65, job_id=jobs[7].id),
        Equipment(name="Master's Mantle",       type="chest", rating=65, job_id=jobs[8].id),
        Equipment(name="Elder Beast Hide",      type="chest", rating=65, job_id=jobs[9].id),

        # CHEST - T10 (rating 82)
        Equipment(name="Power Suit",            type="chest", rating=82, job_id=jobs[0].id),
        Equipment(name="Legend's Coat",         type="chest", rating=82, job_id=jobs[1].id),
        Equipment(name="Explorer's Plate",      type="chest", rating=82, job_id=jobs[2].id),
        Equipment(name="Celestial Robe",        type="chest", rating=82, job_id=jobs[3].id),
        Equipment(name="Void Plate",            type="chest", rating=82, job_id=jobs[4].id),
        Equipment(name="Aegis Plate",           type="chest", rating=82, job_id=jobs[5].id),
        Equipment(name="Divine Robe",           type="chest", rating=82, job_id=jobs[6].id),
        Equipment(name="Dark Assassin's Suit",  type="chest", rating=82, job_id=jobs[7].id),
        Equipment(name="Omniscient's Robe",     type="chest", rating=82, job_id=jobs[8].id),
        Equipment(name="Apex Predator's Coat",  type="chest", rating=82, job_id=jobs[9].id),

        # PRIMARY HAND - T1 (rating 2)
        Equipment(name="Rusty Wrench",          type="primary_hand", rating=2,  job_id=jobs[0].id),
        Equipment(name="Broken Pistol",         type="primary_hand", rating=2,  job_id=jobs[1].id),
        Equipment(name="Wooden Stick",          type="primary_hand", rating=2,  job_id=jobs[2].id),
        Equipment(name="Apprentice's Wand",     type="primary_hand", rating=2,  job_id=jobs[3].id),
        Equipment(name="Training Sword",        type="primary_hand", rating=2,  job_id=jobs[4].id),
        Equipment(name="Wooden Club",           type="primary_hand", rating=2,  job_id=jobs[5].id),
        Equipment(name="Crooked Staff",         type="primary_hand", rating=2,  job_id=jobs[6].id),
        Equipment(name="Rusty Knife",           type="primary_hand", rating=2,  job_id=jobs[7].id),
        Equipment(name="Field Notes",           type="primary_hand", rating=2,  job_id=jobs[8].id),
        Equipment(name="Rope Whip",             type="primary_hand", rating=2,  job_id=jobs[9].id),

        # PRIMARY HAND - T2 (rating 5)
        Equipment(name="Iron Wrench",           type="primary_hand", rating=5,  job_id=jobs[0].id),
        Equipment(name="Flintlock",             type="primary_hand", rating=5,  job_id=jobs[1].id),
        Equipment(name="Short Sword",           type="primary_hand", rating=5,  job_id=jobs[2].id),
        Equipment(name="Crystal Wand",          type="primary_hand", rating=5,  job_id=jobs[3].id),
        Equipment(name="Iron Sword",            type="primary_hand", rating=5,  job_id=jobs[4].id),
        Equipment(name="Iron Club",             type="primary_hand", rating=5,  job_id=jobs[5].id),
        Equipment(name="Wooden Staff",          type="primary_hand", rating=5,  job_id=jobs[6].id),
        Equipment(name="Boot Knife",            type="primary_hand", rating=5,  job_id=jobs[7].id),
        Equipment(name="Research Tome",         type="primary_hand", rating=5,  job_id=jobs[8].id),
        Equipment(name="Taming Whip",           type="primary_hand", rating=5,  job_id=jobs[9].id),

        # PRIMARY HAND - T3 (rating 9)
        Equipment(name="Titan Wrench",          type="primary_hand", rating=9,  job_id=jobs[0].id),
        Equipment(name="Revolver",              type="primary_hand", rating=9,  job_id=jobs[1].id),
        Equipment(name="Scout's Blade",         type="primary_hand", rating=9,  job_id=jobs[2].id),
        Equipment(name="Crystal Staff",         type="primary_hand", rating=9,  job_id=jobs[3].id),
        Equipment(name="Steel Sword",           type="primary_hand", rating=9,  job_id=jobs[4].id),
        Equipment(name="War Club",              type="primary_hand", rating=9,  job_id=jobs[5].id),
        Equipment(name="Sage's Wand",           type="primary_hand", rating=9,  job_id=jobs[6].id),
        Equipment(name="Shadow Blade",          type="primary_hand", rating=9,  job_id=jobs[7].id),
        Equipment(name="Analytical Lens",       type="primary_hand", rating=9,  job_id=jobs[8].id),
        Equipment(name="Beast Prod",            type="primary_hand", rating=9,  job_id=jobs[9].id),

        # PRIMARY HAND - T4 (rating 14)
        Equipment(name="Gear Hammer",           type="primary_hand", rating=14, job_id=jobs[0].id),
        Equipment(name="Double Barrel",         type="primary_hand", rating=14, job_id=jobs[1].id),
        Equipment(name="Traveler's Blade",      type="primary_hand", rating=14, job_id=jobs[2].id),
        Equipment(name="Runic Rod",             type="primary_hand", rating=14, job_id=jobs[3].id),
        Equipment(name="Broad Sword",           type="primary_hand", rating=14, job_id=jobs[4].id),
        Equipment(name="Iron Mace",             type="primary_hand", rating=14, job_id=jobs[5].id),
        Equipment(name="Sage's Staff",          type="primary_hand", rating=14, job_id=jobs[6].id),
        Equipment(name="Twin Blades",           type="primary_hand", rating=14, job_id=jobs[7].id),
        Equipment(name="Scholar's Tome",        type="primary_hand", rating=14, job_id=jobs[8].id),
        Equipment(name="Alpha Whip",            type="primary_hand", rating=14, job_id=jobs[9].id),

        # PRIMARY HAND - T5 (rating 20)
        Equipment(name="Wrench Mk.II",          type="primary_hand", rating=20, job_id=jobs[0].id),
        Equipment(name="Revolver Mk.II",        type="primary_hand", rating=20, job_id=jobs[1].id),
        Equipment(name="Adventurer's Blade",    type="primary_hand", rating=20, job_id=jobs[2].id),
        Equipment(name="Golden Staff",          type="primary_hand", rating=20, job_id=jobs[3].id),
        Equipment(name="War Sword",             type="primary_hand", rating=20, job_id=jobs[4].id),
        Equipment(name="War Axe",               type="primary_hand", rating=20, job_id=jobs[5].id),
        Equipment(name="Elder Staff",           type="primary_hand", rating=20, job_id=jobs[6].id),
        Equipment(name="Shadow Daggers",        type="primary_hand", rating=20, job_id=jobs[7].id),
        Equipment(name="Professor's Lens",      type="primary_hand", rating=20, job_id=jobs[8].id),
        Equipment(name="Feral Staff",           type="primary_hand", rating=20, job_id=jobs[9].id),

        # PRIMARY HAND - T6 (rating 28)
        Equipment(name="Power Wrench",          type="primary_hand", rating=28, job_id=jobs[0].id),
        Equipment(name="Marksman's Rifle",      type="primary_hand", rating=28, job_id=jobs[1].id),
        Equipment(name="Pathfinder's Blade",    type="primary_hand", rating=28, job_id=jobs[2].id),
        Equipment(name="Arcane Rod",            type="primary_hand", rating=28, job_id=jobs[3].id),
        Equipment(name="Knight's Blade",        type="primary_hand", rating=28, job_id=jobs[4].id),
        Equipment(name="Battle Axe",            type="primary_hand", rating=28, job_id=jobs[5].id),
        Equipment(name="Arcane Staff",          type="primary_hand", rating=28, job_id=jobs[6].id),
        Equipment(name="Twin Daggers",          type="primary_hand", rating=28, job_id=jobs[7].id),
        Equipment(name="Grand Tome",            type="primary_hand", rating=28, job_id=jobs[8].id),
        Equipment(name="Taming Staff",          type="primary_hand", rating=28, job_id=jobs[9].id),

        # PRIMARY HAND - T7 (rating 38)
        Equipment(name="Plasma Wrench",         type="primary_hand", rating=38, job_id=jobs[0].id),
        Equipment(name="Repeating Rifle",       type="primary_hand", rating=38, job_id=jobs[1].id),
        Equipment(name="Explorer's Blade",      type="primary_hand", rating=38, job_id=jobs[2].id),
        Equipment(name="Staff of Mysteries",    type="primary_hand", rating=38, job_id=jobs[3].id),
        Equipment(name="Holy Sword",            type="primary_hand", rating=38, job_id=jobs[4].id),
        Equipment(name="Great Axe",             type="primary_hand", rating=38, job_id=jobs[5].id),
        Equipment(name="Ethereal Staff",        type="primary_hand", rating=38, job_id=jobs[6].id),
        Equipment(name="Phantom Blades",        type="primary_hand", rating=38, job_id=jobs[7].id),
        Equipment(name="Mastermind's Lens",     type="primary_hand", rating=38, job_id=jobs[8].id),
        Equipment(name="Beast Caller Staff",    type="primary_hand", rating=38, job_id=jobs[9].id),

        # PRIMARY HAND - T8 (rating 50)
        Equipment(name="Gear Cannon",           type="primary_hand", rating=50, job_id=jobs[0].id),
        Equipment(name="Thunder Gun",           type="primary_hand", rating=50, job_id=jobs[1].id),
        Equipment(name="Trailblazer's Blade",   type="primary_hand", rating=50, job_id=jobs[2].id),
        Equipment(name="Staff of Elements",     type="primary_hand", rating=50, job_id=jobs[3].id),
        Equipment(name="Champion's Blade",      type="primary_hand", rating=50, job_id=jobs[4].id),
        Equipment(name="Warlord's Axe",         type="primary_hand", rating=50, job_id=jobs[5].id),
        Equipment(name="Archmage's Staff",      type="primary_hand", rating=50, job_id=jobs[6].id),
        Equipment(name="Void Daggers",          type="primary_hand", rating=50, job_id=jobs[7].id),
        Equipment(name="Grand Scholar's Lens",  type="primary_hand", rating=50, job_id=jobs[8].id),
        Equipment(name="Alpha Staff",           type="primary_hand", rating=50, job_id=jobs[9].id),

        # PRIMARY HAND - T9 (rating 65)
        Equipment(name="Plasma Cutter",         type="primary_hand", rating=65, job_id=jobs[0].id),
        Equipment(name="Devastator",            type="primary_hand", rating=65, job_id=jobs[1].id),
        Equipment(name="Wayfarer's Blade",      type="primary_hand", rating=65, job_id=jobs[2].id),
        Equipment(name="Grand Staff",           type="primary_hand", rating=65, job_id=jobs[3].id),
        Equipment(name="Dragon Sword",          type="primary_hand", rating=65, job_id=jobs[4].id),
        Equipment(name="Fortress Axe",          type="primary_hand", rating=65, job_id=jobs[5].id),
        Equipment(name="Celestial Staff",       type="primary_hand", rating=65, job_id=jobs[6].id),
        Equipment(name="Specter's Blades",      type="primary_hand", rating=65, job_id=jobs[7].id),
        Equipment(name="Omniscient Lens",       type="primary_hand", rating=65, job_id=jobs[8].id),
        Equipment(name="Elder Taming Staff",    type="primary_hand", rating=65, job_id=jobs[9].id),

        # PRIMARY HAND - T10 (rating 82)
        Equipment(name="Neural Cannon",         type="primary_hand", rating=82, job_id=jobs[0].id),
        Equipment(name="Legend's Rifle",        type="primary_hand", rating=82, job_id=jobs[1].id),
        Equipment(name="Vorpal Blade",          type="primary_hand", rating=82, job_id=jobs[2].id),
        Equipment(name="Staff of Creation",     type="primary_hand", rating=82, job_id=jobs[3].id),
        Equipment(name="Excalibur",             type="primary_hand", rating=82, job_id=jobs[4].id),
        Equipment(name="Aegis Axe",             type="primary_hand", rating=82, job_id=jobs[5].id),
        Equipment(name="Divine Staff",          type="primary_hand", rating=82, job_id=jobs[6].id),
        Equipment(name="Dark Assassin's Blades", type="primary_hand", rating=82, job_id=jobs[7].id),
        Equipment(name="Oracle's Lens",         type="primary_hand", rating=82, job_id=jobs[8].id),
        Equipment(name="Apex Predator's Staff", type="primary_hand", rating=82, job_id=jobs[9].id),

        # SECONDARY HAND - T1 (rating 2)
        Equipment(name="Worn Bracer",           type="secondary_hand", rating=2,  job_id=jobs[0].id),
        Equipment(name="Powder Horn",           type="secondary_hand", rating=2,  job_id=jobs[1].id),
        Equipment(name="Wooden Buckler",        type="secondary_hand", rating=2,  job_id=jobs[2].id),
        Equipment(name="Focus Shard",           type="secondary_hand", rating=2,  job_id=jobs[3].id),
        Equipment(name="Wooden Shield",         type="secondary_hand", rating=2,  job_id=jobs[4].id),
        Equipment(name="Cracked Shield",        type="secondary_hand", rating=2,  job_id=jobs[5].id),
        Equipment(name="Dim Orb",               type="secondary_hand", rating=2,  job_id=jobs[6].id),
        Equipment(name="Smoke Pellet",          type="secondary_hand", rating=2,  job_id=jobs[7].id),
        Equipment(name="Field Journal",         type="secondary_hand", rating=2,  job_id=jobs[8].id),
        Equipment(name="Beast Token",           type="secondary_hand", rating=2,  job_id=jobs[9].id),

        # SECONDARY HAND - T2 (rating 5)
        Equipment(name="Reinforced Bracer",     type="secondary_hand", rating=5,  job_id=jobs[0].id),
        Equipment(name="Ammo Pouch",            type="secondary_hand", rating=5,  job_id=jobs[1].id),
        Equipment(name="Wooden Targe",          type="secondary_hand", rating=5,  job_id=jobs[2].id),
        Equipment(name="Focus Orb",             type="secondary_hand", rating=5,  job_id=jobs[3].id),
        Equipment(name="Iron Shield",           type="secondary_hand", rating=5,  job_id=jobs[4].id),
        Equipment(name="Recruit's Shield",      type="secondary_hand", rating=5,  job_id=jobs[5].id),
        Equipment(name="Spell Tome",            type="secondary_hand", rating=5,  job_id=jobs[6].id),
        Equipment(name="Throwing Knife",        type="secondary_hand", rating=5,  job_id=jobs[7].id),
        Equipment(name="Research Journal",      type="secondary_hand", rating=5,  job_id=jobs[8].id),
        Equipment(name="Feather Totem",         type="secondary_hand", rating=5,  job_id=jobs[9].id),

        # SECONDARY HAND - T3 (rating 9)
        Equipment(name="Tool Bracer",           type="secondary_hand", rating=9,  job_id=jobs[0].id),
        Equipment(name="Quick Draw Holster",    type="secondary_hand", rating=9,  job_id=jobs[1].id),
        Equipment(name="Travel Shield",         type="secondary_hand", rating=9,  job_id=jobs[2].id),
        Equipment(name="Mana Crystal",          type="secondary_hand", rating=9,  job_id=jobs[3].id),
        Equipment(name="Kite Shield",           type="secondary_hand", rating=9,  job_id=jobs[4].id),
        Equipment(name="Sentinel Shield",       type="secondary_hand", rating=9,  job_id=jobs[5].id),
        Equipment(name="Arcane Tome",           type="secondary_hand", rating=9,  job_id=jobs[6].id),
        Equipment(name="Smoke Bomb",            type="secondary_hand", rating=9,  job_id=jobs[7].id),
        Equipment(name="Data Tablet",           type="secondary_hand", rating=9,  job_id=jobs[8].id),
        Equipment(name="Bone Totem",            type="secondary_hand", rating=9,  job_id=jobs[9].id),

        # SECONDARY HAND - T4 (rating 14)
        Equipment(name="Gear Bracer",           type="secondary_hand", rating=14, job_id=jobs[0].id),
        Equipment(name="Off-hand Pistol",       type="secondary_hand", rating=14, job_id=jobs[1].id),
        Equipment(name="Scout's Buckler",       type="secondary_hand", rating=14, job_id=jobs[2].id),
        Equipment(name="Runic Crystal",         type="secondary_hand", rating=14, job_id=jobs[3].id),
        Equipment(name="Battle Shield",         type="secondary_hand", rating=14, job_id=jobs[4].id),
        Equipment(name="Tower Shield",          type="secondary_hand", rating=14, job_id=jobs[5].id),
        Equipment(name="Elder's Tome",          type="secondary_hand", rating=14, job_id=jobs[6].id),
        Equipment(name="Flash Bomb",            type="secondary_hand", rating=14, job_id=jobs[7].id),
        Equipment(name="Annotated Tome",        type="secondary_hand", rating=14, job_id=jobs[8].id),
        Equipment(name="Pack Totem",            type="secondary_hand", rating=14, job_id=jobs[9].id),

        # SECONDARY HAND - T5 (rating 20)
        Equipment(name="Steam Bracer",          type="secondary_hand", rating=20, job_id=jobs[0].id),
        Equipment(name="Bandolier",             type="secondary_hand", rating=20, job_id=jobs[1].id),
        Equipment(name="Pathfinder's Shield",   type="secondary_hand", rating=20, job_id=jobs[2].id),
        Equipment(name="Grand Crystal",         type="secondary_hand", rating=20, job_id=jobs[3].id),
        Equipment(name="Knight's Shield",       type="secondary_hand", rating=20, job_id=jobs[4].id),
        Equipment(name="Bulwark Shield",        type="secondary_hand", rating=20, job_id=jobs[5].id),
        Equipment(name="Mystic Orb",            type="secondary_hand", rating=20, job_id=jobs[6].id),
        Equipment(name="Poison Vial",           type="secondary_hand", rating=20, job_id=jobs[7].id),
        Equipment(name="Professor's Journal",   type="secondary_hand", rating=20, job_id=jobs[8].id),
        Equipment(name="Alpha Totem",           type="secondary_hand", rating=20, job_id=jobs[9].id),

        # SECONDARY HAND - T6 (rating 28)
        Equipment(name="Hydraulic Bracer",      type="secondary_hand", rating=28, job_id=jobs[0].id),
        Equipment(name="Marksman's Scope",      type="secondary_hand", rating=28, job_id=jobs[1].id),
        Equipment(name="Explorer's Buckler",    type="secondary_hand", rating=28, job_id=jobs[2].id),
        Equipment(name="Arcane Crystal",        type="secondary_hand", rating=28, job_id=jobs[3].id),
        Equipment(name="Champion's Shield",     type="secondary_hand", rating=28, job_id=jobs[4].id),
        Equipment(name="Fortress Shield",       type="secondary_hand", rating=28, job_id=jobs[5].id),
        Equipment(name="Arcane Orb",            type="secondary_hand", rating=28, job_id=jobs[6].id),
        Equipment(name="Shadow Bomb",           type="secondary_hand", rating=28, job_id=jobs[7].id),
        Equipment(name="Grand Journal",         type="secondary_hand", rating=28, job_id=jobs[8].id),
        Equipment(name="Elder Totem",           type="secondary_hand", rating=28, job_id=jobs[9].id),

        # SECONDARY HAND - T7 (rating 38)
        Equipment(name="Plasma Bracer",         type="secondary_hand", rating=38, job_id=jobs[0].id),
        Equipment(name="Eagle Eye Scope",       type="secondary_hand", rating=38, job_id=jobs[1].id),
        Equipment(name="Trailblazer's Shield",  type="secondary_hand", rating=38, job_id=jobs[2].id),
        Equipment(name="Ether Crystal",         type="secondary_hand", rating=38, job_id=jobs[3].id),
        Equipment(name="Templar Shield",        type="secondary_hand", rating=38, job_id=jobs[4].id),
        Equipment(name="Citadel Shield",        type="secondary_hand", rating=38, job_id=jobs[5].id),
        Equipment(name="Ethereal Orb",          type="secondary_hand", rating=38, job_id=jobs[6].id),
        Equipment(name="Void Bomb",             type="secondary_hand", rating=38, job_id=jobs[7].id),
        Equipment(name="Mastermind's Journal",  type="secondary_hand", rating=38, job_id=jobs[8].id),
        Equipment(name="Spirit Totem",          type="secondary_hand", rating=38, job_id=jobs[9].id),

        # SECONDARY HAND - T8 (rating 50)
        Equipment(name="Mech Bracer",           type="secondary_hand", rating=50, job_id=jobs[0].id),
        Equipment(name="Rapid Fire Module",     type="secondary_hand", rating=50, job_id=jobs[1].id),
        Equipment(name="Wayfarer's Shield",     type="secondary_hand", rating=50, job_id=jobs[2].id),
        Equipment(name="Philosopher's Orb",     type="secondary_hand", rating=50, job_id=jobs[3].id),
        Equipment(name="Warlord's Shield",      type="secondary_hand", rating=50, job_id=jobs[4].id),
        Equipment(name="Aegis Shield",          type="secondary_hand", rating=50, job_id=jobs[5].id),
        Equipment(name="Archmage's Orb",        type="secondary_hand", rating=50, job_id=jobs[6].id),
        Equipment(name="Specter's Bomb",        type="secondary_hand", rating=50, job_id=jobs[7].id),
        Equipment(name="Grand Scholar's Journal", type="secondary_hand", rating=50, job_id=jobs[8].id),
        Equipment(name="Apex Totem",            type="secondary_hand", rating=50, job_id=jobs[9].id),

        # SECONDARY HAND - T9 (rating 65)
        Equipment(name="Neural Bracer",         type="secondary_hand", rating=65, job_id=jobs[0].id),
        Equipment(name="Targeting System",      type="secondary_hand", rating=65, job_id=jobs[1].id),
        Equipment(name="Explorer's Shield",     type="secondary_hand", rating=65, job_id=jobs[2].id),
        Equipment(name="Grand Orb",             type="secondary_hand", rating=65, job_id=jobs[3].id),
        Equipment(name="Dragon Shield",         type="secondary_hand", rating=65, job_id=jobs[4].id),
        Equipment(name="Bastion Shield",        type="secondary_hand", rating=65, job_id=jobs[5].id),
        Equipment(name="Celestial Orb",         type="secondary_hand", rating=65, job_id=jobs[6].id),
        Equipment(name="Dark Bomb",             type="secondary_hand", rating=65, job_id=jobs[7].id),
        Equipment(name="Omniscient Journal",    type="secondary_hand", rating=65, job_id=jobs[8].id),
        Equipment(name="Elder Spirit Totem",    type="secondary_hand", rating=65, job_id=jobs[9].id),

        # SECONDARY HAND - T10 (rating 82)
        Equipment(name="Exo Bracer",            type="secondary_hand", rating=82, job_id=jobs[0].id),
        Equipment(name="Legend's Scope",        type="secondary_hand", rating=82, job_id=jobs[1].id),
        Equipment(name="Legendary Buckler",     type="secondary_hand", rating=82, job_id=jobs[2].id),
        Equipment(name="Cosmic Orb",            type="secondary_hand", rating=82, job_id=jobs[3].id),
        Equipment(name="Eternal Shield",        type="secondary_hand", rating=82, job_id=jobs[4].id),
        Equipment(name="Divine Shield",         type="secondary_hand", rating=82, job_id=jobs[5].id),
        Equipment(name="Divine Orb",            type="secondary_hand", rating=82, job_id=jobs[6].id),
        Equipment(name="Phantom Bomb",          type="secondary_hand", rating=82, job_id=jobs[7].id),
        Equipment(name="Oracle's Journal",      type="secondary_hand", rating=82, job_id=jobs[8].id),
        Equipment(name="Apex Spirit Totem",     type="secondary_hand", rating=82, job_id=jobs[9].id),

        # ACCESORY - T1 (rating 2)
        Equipment(name="Bent Cog",              type="accesory", rating=2,  job_id=jobs[0].id),
        Equipment(name="Copper Badge",          type="accesory", rating=2,  job_id=jobs[1].id),
        Equipment(name="Lucky Pebble",          type="accesory", rating=2,  job_id=jobs[2].id),
        Equipment(name="Empty Vial",            type="accesory", rating=2,  job_id=jobs[3].id),
        Equipment(name="Tin Ring",              type="accesory", rating=2,  job_id=jobs[4].id),
        Equipment(name="Recruit's Insignia",    type="accesory", rating=2,  job_id=jobs[5].id),
        Equipment(name="Dim Crystal",           type="accesory", rating=2,  job_id=jobs[6].id),
        Equipment(name="Shadow Token",          type="accesory", rating=2,  job_id=jobs[7].id),
        Equipment(name="Student's Pin",         type="accesory", rating=2,  job_id=jobs[8].id),
        Equipment(name="Animal Claw",           type="accesory", rating=2,  job_id=jobs[9].id),

        # ACCESORY - T2 (rating 5)
        Equipment(name="Pocket Compass",        type="accesory", rating=5,  job_id=jobs[0].id),
        Equipment(name="Sheriff's Badge",       type="accesory", rating=5,  job_id=jobs[1].id),
        Equipment(name="Lucky Clover",          type="accesory", rating=5,  job_id=jobs[2].id),
        Equipment(name="Elixir Vial",           type="accesory", rating=5,  job_id=jobs[3].id),
        Equipment(name="Iron Ring",             type="accesory", rating=5,  job_id=jobs[4].id),
        Equipment(name="Guard's Insignia",      type="accesory", rating=5,  job_id=jobs[5].id),
        Equipment(name="Spirit Pendant",        type="accesory", rating=5,  job_id=jobs[6].id),
        Equipment(name="Assassin's Mark",       type="accesory", rating=5,  job_id=jobs[7].id),
        Equipment(name="Scholar's Pin",         type="accesory", rating=5,  job_id=jobs[8].id),
        Equipment(name="Beast Fang",            type="accesory", rating=5,  job_id=jobs[9].id),

        # ACCESORY - T3 (rating 9)
        Equipment(name="Gear Token",            type="accesory", rating=9,  job_id=jobs[0].id),
        Equipment(name="Marksman's Badge",      type="accesory", rating=9,  job_id=jobs[1].id),
        Equipment(name="Journey Stone",         type="accesory", rating=9,  job_id=jobs[2].id),
        Equipment(name="Alchemist's Seal",      type="accesory", rating=9,  job_id=jobs[3].id),
        Equipment(name="Warrior's Band",        type="accesory", rating=9,  job_id=jobs[4].id),
        Equipment(name="Sentinel's Medal",      type="accesory", rating=9,  job_id=jobs[5].id),
        Equipment(name="Rune Pendant",          type="accesory", rating=9,  job_id=jobs[6].id),
        Equipment(name="Shadow Seal",           type="accesory", rating=9,  job_id=jobs[7].id),
        Equipment(name="Research Medal",        type="accesory", rating=9,  job_id=jobs[8].id),
        Equipment(name="Pack Fang",             type="accesory", rating=9,  job_id=jobs[9].id),

        # ACCESORY - T4 (rating 14)
        Equipment(name="Clockwork Charm",       type="accesory", rating=14, job_id=jobs[0].id),
        Equipment(name="Bounty Medal",          type="accesory", rating=14, job_id=jobs[1].id),
        Equipment(name="Explorer's Charm",      type="accesory", rating=14, job_id=jobs[2].id),
        Equipment(name="Mystic Vial",           type="accesory", rating=14, job_id=jobs[3].id),
        Equipment(name="Steel Ring",            type="accesory", rating=14, job_id=jobs[4].id),
        Equipment(name="Vanguard's Medal",      type="accesory", rating=14, job_id=jobs[5].id),
        Equipment(name="Mystic Pendant",        type="accesory", rating=14, job_id=jobs[6].id),
        Equipment(name="Phantom Seal",          type="accesory", rating=14, job_id=jobs[7].id),
        Equipment(name="Academic Medal",        type="accesory", rating=14, job_id=jobs[8].id),
        Equipment(name="Alpha Fang",            type="accesory", rating=14, job_id=jobs[9].id),

        # ACCESORY - T5 (rating 20)
        Equipment(name="Steam Cog",             type="accesory", rating=20, job_id=jobs[0].id),
        Equipment(name="Outlaw's Star",         type="accesory", rating=20, job_id=jobs[1].id),
        Equipment(name="Pathfinder's Stone",    type="accesory", rating=20, job_id=jobs[2].id),
        Equipment(name="Grand Vial",            type="accesory", rating=20, job_id=jobs[3].id),
        Equipment(name="Knight's Ring",         type="accesory", rating=20, job_id=jobs[4].id),
        Equipment(name="Defender's Emblem",     type="accesory", rating=20, job_id=jobs[5].id),
        Equipment(name="Arcane Pendant",        type="accesory", rating=20, job_id=jobs[6].id),
        Equipment(name="Night Seal",            type="accesory", rating=20, job_id=jobs[7].id),
        Equipment(name="Professor's Medal",     type="accesory", rating=20, job_id=jobs[8].id),
        Equipment(name="Elder Fang",            type="accesory", rating=20, job_id=jobs[9].id),

        # ACCESORY - T6 (rating 28)
        Equipment(name="Precision Cog",         type="accesory", rating=28, job_id=jobs[0].id),
        Equipment(name="Marshal's Star",        type="accesory", rating=28, job_id=jobs[1].id),
        Equipment(name="Wayfarer's Charm",      type="accesory", rating=28, job_id=jobs[2].id),
        Equipment(name="Arcane Vial",           type="accesory", rating=28, job_id=jobs[3].id),
        Equipment(name="Champion's Ring",       type="accesory", rating=28, job_id=jobs[4].id),
        Equipment(name="Fortress Emblem",       type="accesory", rating=28, job_id=jobs[5].id),
        Equipment(name="Elder Rune",            type="accesory", rating=28, job_id=jobs[6].id),
        Equipment(name="Void Seal",             type="accesory", rating=28, job_id=jobs[7].id),
        Equipment(name="Grand Medal",           type="accesory", rating=28, job_id=jobs[8].id),
        Equipment(name="Alpha Claw",            type="accesory", rating=28, job_id=jobs[9].id),

        # ACCESORY - T7 (rating 38)
        Equipment(name="Gear Core",             type="accesory", rating=38, job_id=jobs[0].id),
        Equipment(name="Desperado's Star",      type="accesory", rating=38, job_id=jobs[1].id),
        Equipment(name="Trailblazer's Stone",   type="accesory", rating=38, job_id=jobs[2].id),
        Equipment(name="Philosopher's Vial",    type="accesory", rating=38, job_id=jobs[3].id),
        Equipment(name="Templar's Ring",        type="accesory", rating=38, job_id=jobs[4].id),
        Equipment(name="Citadel Emblem",        type="accesory", rating=38, job_id=jobs[5].id),
        Equipment(name="Ethereal Rune",         type="accesory", rating=38, job_id=jobs[6].id),
        Equipment(name="Specter's Mark",        type="accesory", rating=38, job_id=jobs[7].id),
        Equipment(name="Mastermind's Medal",    type="accesory", rating=38, job_id=jobs[8].id),
        Equipment(name="Spirit Claw",           type="accesory", rating=38, job_id=jobs[9].id),

        # ACCESORY - T8 (rating 50)
        Equipment(name="Gravity Core",          type="accesory", rating=50, job_id=jobs[0].id),
        Equipment(name="Legend's Badge",        type="accesory", rating=50, job_id=jobs[1].id),
        Equipment(name="Legendary Stone",       type="accesory", rating=50, job_id=jobs[2].id),
        Equipment(name="Grand Alchemist's Vial", type="accesory", rating=50, job_id=jobs[3].id),
        Equipment(name="Warlord's Ring",        type="accesory", rating=50, job_id=jobs[4].id),
        Equipment(name="Bastion Emblem",        type="accesory", rating=50, job_id=jobs[5].id),
        Equipment(name="Celestial Rune",        type="accesory", rating=50, job_id=jobs[6].id),
        Equipment(name="Dark Seal",             type="accesory", rating=50, job_id=jobs[7].id),
        Equipment(name="Grand Scholar's Medal", type="accesory", rating=50, job_id=jobs[8].id),
        Equipment(name="Apex Claw",             type="accesory", rating=50, job_id=jobs[9].id),

        # ACCESORY - T9 (rating 65)
        Equipment(name="Neural Core",           type="accesory", rating=65, job_id=jobs[0].id),
        Equipment(name="Myth Badge",            type="accesory", rating=65, job_id=jobs[1].id),
        Equipment(name="Ancient Stone",         type="accesory", rating=65, job_id=jobs[2].id),
        Equipment(name="Cosmic Vial",           type="accesory", rating=65, job_id=jobs[3].id),
        Equipment(name="Dragon Ring",           type="accesory", rating=65, job_id=jobs[4].id),
        Equipment(name="Citadel Crest",         type="accesory", rating=65, job_id=jobs[5].id),
        Equipment(name="Divine Rune",           type="accesory", rating=65, job_id=jobs[6].id),
        Equipment(name="Phantom Mark",          type="accesory", rating=65, job_id=jobs[7].id),
        Equipment(name="Omniscient Medal",      type="accesory", rating=65, job_id=jobs[8].id),
        Equipment(name="Elder Spirit Claw",     type="accesory", rating=65, job_id=jobs[9].id),

        # ACCESORY - T10 (rating 82)
        Equipment(name="Omega Core",            type="accesory", rating=82, job_id=jobs[0].id),
        Equipment(name="Legend's Medallion",    type="accesory", rating=82, job_id=jobs[1].id),
        Equipment(name="Explorer's Relic",      type="accesory", rating=82, job_id=jobs[2].id),
        Equipment(name="Philosopher's Stone",   type="accesory", rating=82, job_id=jobs[3].id),
        Equipment(name="Legendary Ring",        type="accesory", rating=82, job_id=jobs[4].id),
        Equipment(name="Aegis Crest",           type="accesory", rating=82, job_id=jobs[5].id),
        Equipment(name="Cosmic Pendant",        type="accesory", rating=82, job_id=jobs[6].id),
        Equipment(name="Dark Assassin's Seal",  type="accesory", rating=82, job_id=jobs[7].id),
        Equipment(name="Oracle's Medal",        type="accesory", rating=82, job_id=jobs[8].id),
        Equipment(name="Apex Predator's Fang",  type="accesory", rating=82, job_id=jobs[9].id),
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

    def loot(*specs):
        return [equipments[base + (tier - 1) * 10 + job].id for base, tier, job in specs]

    dungeons = [
        Dungeon(
            name="Primeval Dense Forest",
            description="Vast woodland of ancient trees, narrow rivers and mist-covered clearings.",
            image_path="/localizations/forest_1.png",
            min_rating=0, visibility_rating=0, duration=60,
            loot=loot((H,1,2), (C,1,4), (P,1,3), (S,1,0), (A,1,1)),
        ),
        Dungeon(
            name="The Infinite Observation Tower",
            description="Colossal vertical structure that pierces the clouds and vanishes into the sky.",
            image_path="/localizations/tower_2.png",
            min_rating=50, visibility_rating=0, duration=120,
            loot=loot((H,2,4), (C,2,3), (P,2,1), (S,2,2), (A,2,6)),
        ),
        Dungeon(
            name="Canyon of Eternal Storms",
            description="Deep rocky rift with sheer walls and violent air currents.",
            image_path="/localizations/canyon_3.png",
            min_rating=80, visibility_rating=40, duration=180,
            loot=loot((H,3,1), (C,3,0), (P,3,4), (S,2,9), (A,3,7), (C,2,5)),
        ),
        Dungeon(
            name="Archipelago of Wandering Clouds",
            description="Collection of floating islands suspended above a sea of clouds.",
            image_path="/localizations/archipelago_4.png",
            min_rating=120, visibility_rating=60, duration=300,
            loot=loot((H,3,6), (C,3,8), (P,3,1), (S,3,4), (A,3,9), (P,3,3)),
        ),
        Dungeon(
            name="Abyssal Steam Pit",
            description="Enormous geothermal rift descending into the earth's crust.",
            image_path="/localizations/pit_5.png",
            min_rating=150, visibility_rating=75, duration=420,
            loot=loot((H,4,0), (C,4,4), (P,3,9), (S,4,5), (A,4,8), (H,3,7)),
        ),
        Dungeon(
            name="Sunken Bronze City",
            description="Ruins of an ancient technological metropolis beneath dense, dark waters.",
            image_path="/localizations/sunken_6.png",
            min_rating=180, visibility_rating=90, duration=600,
            loot=loot((H,4,8), (C,4,7), (P,4,1), (S,4,2), (A,4,4), (C,4,6)),
        ),
        Dungeon(
            name="Isle of the Fallen Engineers",
            description="Rocky island overrun by abandoned factories and ruined laboratories.",
            image_path="/localizations/engineers_7.png",
            min_rating=220, visibility_rating=110, duration=900,
            loot=loot((H,5,0), (C,5,4), (P,5,1), (S,4,3), (A,5,7), (H,4,9)),
        ),
        Dungeon(
            name="Resonant Crystal Desert",
            description="Vast expanse of dunes formed by fragments of translucent crystal.",
            image_path="/localizations/desert_8.png",
            min_rating=260, visibility_rating=130, duration=1200,
            loot=loot((H,5,8), (C,5,3), (P,5,4), (S,5,9), (A,5,5), (P,5,6)),
        ),
        Dungeon(
            name="Airship Graveyard",
            description="Plains covered by the wreckage of crashed zeppelins and airships.",
            image_path="/localizations/graveyard_9.png",
            min_rating=300, visibility_rating=150, duration=1800,
            loot=loot((H,6,1), (C,6,0), (P,6,4), (S,5,2), (A,6,3), (P,5,7)),
        ),
        Dungeon(
            name="Etherized Caldera Volcano",
            description="Active volcano with a wide caldera surrounded by lava flows.",
            image_path="/localizations/volcano_10.png",
            min_rating=400, visibility_rating=200, duration=3600,
            loot=loot((H,7,4), (C,7,5), (P,7,3), (S,6,6), (A,7,9), (H,6,7)),
        ),
        Dungeon(
            name="Ether Core",
            description="Colossal cavity at the planet's core where the world's energy converges.",
            image_path="/localizations/core_11.png",
            min_rating=600, visibility_rating=300, duration=7200,
            loot=loot((H,9,4), (C,9,0), (P,8,3), (S,9,5), (A,9,8), (H,10,6)),
        ),
    ]
    db.session.add_all(dungeons)
    db.session.commit()

    print("Seeding data inserted successfully")
