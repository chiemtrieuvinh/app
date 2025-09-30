import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

def test_login_success(client):
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

def test_login_invalid_credentials(client):
    with patch('routers.auth.authenticate_user') as mock_auth:
        mock_auth.return_value = False
        
        response = client.post("/auth/token", data={
            "username": "testuser",
            "password": "wrong_password"
        })
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]