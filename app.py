from flask import Flask, render_template
from flask_socketio import SocketIO
from auth import auth_bp  
#from flask_migrate import Migrate

from models import db
from models import Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking, as it is unnecessary

socketio = SocketIO(app)

#migrate = Migrate(app, db)
db.init_app(app)

# Register the authentication blueprint with the app
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/chat")
def index():
    messages = Message.query.all()
    message_texts = [message.text for message in messages]  
    print(message_texts)
    return render_template('index.html', messages=messages)

# Save it to the database
@socketio.on('my event')
def handle_message(data):
    from models import Message
    print(data)
    # Assuming 'user_id' is available in the 'data' dictionary
    #new_message = Message(text=data['message'], user_id=data['user_id'])
    new_message = Message(text=data['message'], user_id="tmp user")
    db.session.add(new_message)
    db.session.commit()
    print('received message: ', data)

if __name__ == "__main__":
    # Create the database tables (if they don't exist) before running the app
    with app.app_context():
        db.create_all()
    socketio.run(app)

