from app import create_app
from app.extensions import db
from flask_migrate import upgrade

app = create_app()

with app.app_context():
    db.create_all()
    upgrade()

if __name__ == "__main__":
    app.run(debug=True)