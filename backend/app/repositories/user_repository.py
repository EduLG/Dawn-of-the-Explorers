from app.models.user import User

def get_user_by_id(user_id):
	return User.query.filter_by(id=user_id).first()
