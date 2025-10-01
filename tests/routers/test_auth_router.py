import pytest
from unittest.mock import patch, MagicMock
from database import get_db_context
from main import app

def test_login_success(client):
    mock_db = MagicMock()
    
    app.dependency_overrides[get_db_context] = lambda: mock_db
    
    with patch('routers.auth.authenticate_user') as mock_auth, \
         patch('routers.auth.create_access_token') as mock_token:
        
        mock_user = MagicMock()
        mock_auth.return_value = mock_user
        mock_token.return_value = "test_token"
        
        response = client.post("/auth/token", data={
            "username": "testuser",
            "password": "password"
        })
        
        assert response.status_code == 200
        assert response.json() == {
            "access_token": "test_token",
            "token_type": "bearer"
        }
    
    app.dependency_overrides.clear()

def test_login_invalid_credentials(client):
    mock_db = MagicMock()
    
    app.dependency_overrides[get_db_context] = lambda: mock_db
    
    with patch('routers.auth.authenticate_user') as mock_auth:
        mock_auth.return_value = False
        
        response = client.post("/auth/token", data={
            "username": "testuser",
            "password": "wrong_password"
        })
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    app.dependency_overrides.clear()