from web import create_app, socketio
from web.model import db

if __name__ == '__main__':
    app = create_app()

    # Create the database tables before running the application
    with app.app_context():
        db.create_all()

    # Run the application using SocketIO for WebSocket support
    socketio.run(app, debug=True, port=5000)

