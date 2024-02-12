import pytest
from web.model import db, User
from app import create_app
from flask_bcrypt import generate_password_hash, check_password_hash

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login(client):
    test_username = 'test_user'
    test_password = 'test_password'
    hashed_password = generate_password_hash(test_password)
    new_user = User(username=test_username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    response = client.post('/login', data=dict(
        username=test_username,
        password=test_password
    ), follow_redirects=True)

    assert response.status_code == 200

def test_login_invalid_credentials(client):
    response = client.post('/login', data=dict(
        username='invalid_user',
        password='invalid_password'
    ), follow_redirects=True)

    assert response.status_code == 200

