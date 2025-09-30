import pytest
from unittest.mock import patch, MagicMock

def test_auth_login_success(client):
    with patch('routers.auth.authenticate_user') as mock_auth, \
         patch('routers.auth.create_access_token') as mock_token:
        
        mock_user = MagicMock()
        mock_auth.return_value = mock_user
        mock_token.return_value = "test_token"
        
        def mock_get_db():
            yield MagicMock()
        
        with patch('routers.auth.get_db_context', mock_get_db):
            response = client.post("/auth/token", data={
                "username": "testuser",
                "password": "password"
            })
            
            assert response.status_code == 200
            assert response.json() == {
                "access_token": "test_token",
                "token_type": "bearer"
            }

def test_users_get_all(client):
    with patch('routers.user.user') as mock_user_schema:
        mock_users = [MagicMock(), MagicMock()]
        mock_user_schema.User = MagicMock()
        
        def mock_get_db():
            mock_db_session = MagicMock()
            mock_db_session.query.return_value.all.return_value = mock_users
            yield mock_db_session
        
        with patch('routers.user.get_db_context', mock_get_db):
            response = client.get("/users")
            assert response.status_code == 200

def test_tasks_get_admin(client):
    mock_user = MagicMock()
    mock_user.is_admin = True
    
    with patch('routers.task.token_interceptor', return_value=mock_user), \
         patch('routers.task.task') as mock_task_schema:
        
        mock_tasks = [MagicMock()]
        mock_task_schema.Task = MagicMock()
        
        def mock_get_db():
            mock_db_session = MagicMock()
            mock_db_session.query.return_value.all.return_value = mock_tasks
            yield mock_db_session
        
        with patch('routers.task.get_db_context', mock_get_db):
            response = client.get("/tasks", headers={"Authorization": "Bearer test_token"})
            assert response.status_code == 200