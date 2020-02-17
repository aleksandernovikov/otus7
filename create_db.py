from app import app, db

db.init_app(app)
db.create_all()
