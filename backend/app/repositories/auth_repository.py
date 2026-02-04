from app.extensions import db
from app.models.user import User


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def create_user(username, email, password_hash):
    user = User(username=username, email=email, password=password_hash)
    db.session.add(user)
    db.session.commit()
    return user
