import pytest
from backend.app import create_app
from backend.app.extensions import db
from backend.app.models import Accommodation, Room, Review, Booking, User

@pytest.fixture
def app():
    app = create_app("testing") # Assuming testing config uses memory DB
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_average_rating(app):
    """Test Task 1: Rating Logic"""
    host = User(full_name="Test Host", email="host@test.com", phone="123", role="host")
    db.session.add(host)
    db.session.commit()
    
    acc = Accommodation(host_id=host.id, name="Test Homestay")
    db.session.add(acc)
    db.session.commit()
    
    room1 = Room(accommodation_id=acc.id, name="Room 1")
    room2 = Room(accommodation_id=acc.id, name="Room 2")
    db.session.add_all([room1, room2])
    db.session.commit()
    
    # Add reviews
    r1 = Review(room_id=room1.id, guest_name="Guest 1", rating=5)
    r2 = Review(room_id=room1.id, guest_name="Guest 2", rating=4)
    r3 = Review(room_id=room2.id, guest_name="Guest 3", rating=3)
    db.session.add_all([r1, r2, r3])
    db.session.commit()
    
    # Average should be (5+4+3)/3 = 4.0
    assert acc.average_rating == 4.0

def test_pet_policy_boolean(app):
    """Test Task 10: Pet Policy Boolean"""
    host = User(full_name="Test Host", email="host@test.com", phone="123", role="host")
    db.session.add(host)
    db.session.commit()
    
    acc = Accommodation(host_id=host.id, name="Pet Friendly Homestay", allows_pets=True)
    db.session.add(acc)
    db.session.commit()
    
    assert acc.allows_pets is True
