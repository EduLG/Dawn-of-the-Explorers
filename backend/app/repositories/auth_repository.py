from app.extensions import db
from app.models.user import User
from app.models.party import Party


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def create_user(username, email, password_hash):
    user = User(username=username, email=email, password=password_hash)
    db.session.add(user)
    db.session.flush()  # get user.id before creating Party
    party = Party(name="Explorers party", user_id=user.id)
    db.session.add(party)
    db.session.commit()
    return user
