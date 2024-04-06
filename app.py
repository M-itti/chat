from web import create_app, socketio
from web.model import db

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    socketio.run(app, debug=True, port=5005)

