import os
import pytest

# Set TESTING to True BEFORE importing the app so config.py uses SQLite
os.environ["TESTING"] = "True"

from app import app, db

@pytest.fixture
def client():
    # Setup: Configure the app for testing
    app.config["TESTING"] = True
    
    # Create a test client
    with app.test_client() as client:
        with app.app_context():
            # Ensure tables are created in the in-memory SQLite DB
            db.create_all()
        yield client

def test_home(client):
    """Test the home page (/)"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.get_json()
    assert "Flask + MySQL + SQLAlchemy is working!" in data["message"]

def test_create_user_missing_data(client):
    """Test creating a user with missing data"""
    response = client.post("/users", json={"name": "Rajiv"})
    assert response.status_code == 400
    assert "Name and email are required" in response.get_json()["error"]
