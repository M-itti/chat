from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from model import User
from auth import auth
from model import db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins='*')

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('new_message')
def handle_new_message(data):
    username = data.get('username')
    message_content = data.get('message')
    
    # Create a new Message instance
    new_message = User(username=username, message=message_content)
    
    # Add the message to the database
    db.session.add(new_message)
    db.session.commit()
    
    # Emit the updated messages to all clients
    messages = User.query.all()
    emit('update_messages', [{'username': msg.username, 'message': msg.message} for msg in messages], broadcast=True)

@socketio.on('connect')
def handle_connect():
    # Retrieve all messages from the database and emit them to the client
    messages = User.query.all()
    emit('update_messages', [{'username': msg.username, 'message': msg.message} for msg in messages])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app)

