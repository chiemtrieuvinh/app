import pytest
from unittest.mock import MagicMock
from services.auth import token_interceptor
from database import get_db_context
from main import app

def test_get_tasks_success_admin(client):
    mock_user = MagicMock()
    mock_user.is_admin = True
    
    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = []
    
    app.dependency_overrides[token_interceptor] = lambda: mock_user
    app.dependency_overrides[get_db_context] = lambda: mock_db
    
    response = client.get("/tasks")
    assert response.status_code == 200
    
    app.dependency_overrides.clear()

def test_get_tasks_forbidden_non_admin(client):
    mock_user = MagicMock()
    mock_user.is_admin = False
    
    app.dependency_overrides[token_interceptor] = lambda: mock_user
    
    response = client.get("/tasks")
    assert response.status_code == 403
    assert "Not authorized to access this resource" in response.json()["detail"]
    
    app.dependency_overrides.clear()

def test_get_tasks_with_query_params(client):
    mock_user = MagicMock()
    mock_user.is_admin = True
    
    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = []
    
    app.dependency_overrides[token_interceptor] = lambda: mock_user
    app.dependency_overrides[get_db_context] = lambda: mock_db
    
    response = client.get("/tasks?title=test&task_id=123&page=1&size=10")
    assert response.status_code == 200
    
    app.dependency_overrides.clear()

def test_create_task_success(client):
    mock_user = MagicMock()
    mock_user.is_admin = True
    
    task_data = {
        "summary": "Test Task",
        "description": "Test Description",
        "status": "Open",
        "priority": "High"
    }
    
    mock_db = MagicMock()
    
    app.dependency_overrides[token_interceptor] = lambda: mock_user
    app.dependency_overrides[get_db_context] = lambda: mock_db
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    assert response.json() == {"message": "New task created"}
    
    app.dependency_overrides.clear()