from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import redis

socketio = SocketIO(cors_allowed_origins='*', engineio_logger=False, logger=True)

def create_app():
    app = Flask(__name__, static_folder='assets')
    app.config['SECRET_KEY'] = 'secret!'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_KEY_PREFIX'] = 'session:'
    app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379, db=0)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from .model import User, db
    from .auth import auth_bp
    from .main import main

    db.init_app(app)
    Session(app)
    socketio.init_app(app) 

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')

    return app

