import pytest
from unittest.mock import patch, MagicMock

def test_get_tasks_success_admin(client):
    mock_user = MagicMock()
    mock_user.is_admin = True
    
    with patch('routers.task.token_interceptor', return_value=mock_user), \
         patch('routers.task.task') as mock_task_schema:
        
        mock_tasks = [MagicMock(), MagicMock()]
        mock_task_schema.Task = MagicMock()
        
        with patch('database.get_db_context') as mock_db:
            mock_db_session = MagicMock()
            mock_db_session.query.return_value.all.return_value = mock_tasks
            mock_db.return_value = mock_db_session
            
            response = client.get("/tasks", headers={"Authorization": "Bearer test_token"})
            assert response.status_code == 200

def test_get_tasks_forbidden_non_admin(client):
    mock_user = MagicMock()
    mock_user.is_admin = False
    
    with patch('routers.task.token_interceptor', return_value=mock_user):
        response = client.get("/tasks", headers={"Authorization": "Bearer test_token"})
        assert response.status_code == 403
        assert "Not authorized to access this resource" in response.json()["detail"]

def test_get_tasks_with_query_params(client):
    mock_user = MagicMock()
    mock_user.is_admin = True
    
    with patch('routers.task.token_interceptor', return_value=mock_user), \
         patch('routers.task.task') as mock_task_schema:
        
        mock_tasks = [MagicMock()]
        mock_task_schema.Task = MagicMock()
        
        with patch('database.get_db_context') as mock_db:
            mock_db_session = MagicMock()
            mock_db_session.query.return_value.all.return_value = mock_tasks
            mock_db.return_value = mock_db_session
            
            response = client.get("/tasks?title=test&task_id=123&page=1&size=10", 
                                headers={"Authorization": "Bearer test_token"})
            assert response.status_code == 200

def test_create_task_success(client):
    mock_user = MagicMock()
    mock_user.is_admin = True
    
    task_data = {
        "summary": "Test Task",
        "description": "Test Description",
        "status": "Open",
        "priority": "High"
    }
    
    with patch('routers.task.token_interceptor', return_value=mock_user), \
         patch('routers.task.task') as mock_task_schema:
        
        mock_task_schema.Task = MagicMock()
        
        response = client.post("/tasks", 
                             json=task_data,
                             headers={"Authorization": "Bearer test_token"})
        assert response.status_code == 201
        assert response.json() == {"message": "New task created"}