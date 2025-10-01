import pytest
from unittest.mock import MagicMock
from database import get_db_context
from main import app

def test_get_users(client):
    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = []
    
    app.dependency_overrides[get_db_context] = lambda: mock_db
    
    response = client.get("/users")
    assert response.status_code == 200
    
    app.dependency_overrides.clear()

def test_create_user(client):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "password123",
        "is_admin": True
    }
    
    mock_db = MagicMock()
    
    app.dependency_overrides[get_db_context] = lambda: mock_db
    
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json() == {"message": "New user created"}
    
    app.dependency_overrides.clear()
