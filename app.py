from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from model import User
from model import db, User
from auth import auth_bp
from flask import jsonify, session

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins='*', engineio_logger=True,logger=False)

db.init_app(app)
app.register_blueprint(auth_bp, url_prefix='/')

@app.route('/get_name')
def get_name():
    username = session.get('username')  
    return jsonify({'username': username})  

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/chat')
def chat():
    messages = User.query.all()
    message_text = [message.message for message in messages]
    return render_template('index.html', messages=messages)

# retrieve the session username
@socketio.on('new_message')
def handle_new_message(data):
    username = data.get('username')
    message_content = data.get('message')
    ses_username = session['username']
    
    # Create a new Message instance
    new_message = User(username=username, message=message_content)
    
    # Add the message to the database
    db.session.add(new_message)
    db.session.commit()
    
    messages = User.query.all()

    # Emit the updated messages to all clients
    emit('update_messages', [{'username': msg.username, 'message': msg.message} for msg in messages], broadcast=True)

@socketio.on('connect')
def handle_connect():
    # Retrieve all messages from the database and emit them to the client
    messages = User.query.all()
    emit('update_messages', [{'username': msg.username, 'message': msg.message} for msg in messages])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)

