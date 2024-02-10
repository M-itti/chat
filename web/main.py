from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, session
import redis
from flask_session import Session
from flask import Blueprint

from .model import db, User
from .auth import auth_bp
from . import socketio

main = Blueprint('main', __name__)

@main.route('/get_name')
def get_name():
    username = session.get('username')  
    return jsonify({'username': username})  

@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home.html')

@main.route('/chat')
def chat():
    username = request.args.get('username')
    messages = User.query.all()
    message_text = [message.message for message in messages]
    return render_template('index.html', messages=messages, username=username)

# retrieve the session username
@socketio.on('new_message')
def handle_new_message(data):
    username = data.get('username')
    message_content = data.get('message')
    timestamp = data.get('timestamp')
    ses_username = session['username']
    
    # Create a new Message instance
    new_message = User(username=username, message=message_content, timestamp=timestamp)
    
    # Add the message to the database
    db.session.add(new_message)
    db.session.commit()
    
    messages = User.query.all()

    # Emit the updated messages to all clients
    emit('update_messages', [{'username': msg.username, 'message': msg.message, 'timestamp': msg.timestamp} for msg in messages], broadcast=True)

@socketio.on('connect')
def handle_connect():
    # Retrieve all messages from the database and emit them to the client
    messages = User.query.all()

    for msg in messages:
        emit('update_messages', [{'username': msg.username, 'message': msg.message, 'timestamp': msg.timestamp} for msg in messages])

