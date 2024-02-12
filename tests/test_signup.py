import pytest
from web.model import db, User
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_register(client):
    response = client.post('/register', data=dict(
        username='test_user',
        password='test_password'
    ), follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Account created successfully!' in response.data

    # Ensure that the user is added to the database
    user = User.query.filter_by(username='test_user').first()
    assert user is not None

