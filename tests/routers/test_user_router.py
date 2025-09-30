import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

def test_get_users(client):
    with patch('routers.user.user') as mock_user_schema:
        mock_users = [MagicMock(), MagicMock()]
        mock_user_schema.User = MagicMock()
        
        with patch('database.get_db_context') as mock_db:
            mock_db_session = MagicMock()
            mock_db_session.query.return_value.all.return_value = mock_users
            mock_db.return_value = mock_db_session
            
            response = client.get("/users")
            assert response.status_code == 200

def test_create_user(client):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "password123",
        "is_admin": True
    }
    
    with patch('routers.user.user') as mock_user_schema, \
         patch('routers.user.datetime') as mock_datetime:
        
        mock_user_schema.get_password_hash.return_value = "hashed_password"
        mock_user_schema.User = MagicMock()
        mock_datetime.now.return_value = "2023-01-01"
        
        response = client.post("/users", json=user_data)
        assert response.status_code == 201
        assert response.json() == {"message": "New user created"}
