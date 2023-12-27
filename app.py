from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

messages = []  # To store messages

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('new_message')
def handle_new_message(data):
    messages.append(data)
    emit('update_messages', messages, broadcast=True)

@socketio.on('connect')
def handle_connect():
    emit('update_messages', messages)

if __name__ == '__main__':
    socketio.run(app)

