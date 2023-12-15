from flask import Flask
from flask import render_template
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def hello_world():    
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
        print('received message: ' + data)

if __name__ == '__main__':
        socketio.run(app)

