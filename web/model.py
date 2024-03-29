from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=False)
    message = db.Column(db.String(500))
    password = db.Column(db.String(500))
    timestamp = db.Column(db.String(500))

