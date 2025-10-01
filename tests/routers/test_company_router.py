import pytest
from unittest.mock import MagicMock
from services.auth import token_interceptor
from database import get_db_context
from main import app

def test_get_companies_authenticated(client):
    mock_user = MagicMock()
    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = []
    
    app.dependency_overrides[token_interceptor] = lambda: mock_user
    app.dependency_overrides[get_db_context] = lambda: mock_db
    
    response = client.get("/companies")
    assert response.status_code == 200
    
    app.dependency_overrides.clear()

def test_create_company_authenticated(client):
    mock_user = MagicMock()
    mock_db = MagicMock()
    
    company_data = {
        "name": "Test Company",
        "description": "Test Description",
        "mode": "active",
        "rating": "5"
    }
    
    app.dependency_overrides[token_interceptor] = lambda: mock_user
    app.dependency_overrides[get_db_context] = lambda: mock_db
    
    response = client.post("/companies", json=company_data)
    assert response.status_code == 201
    assert response.json() == {"message": "New company created"}
    
    app.dependency_overrides.clear()

def test_get_companies_unauthenticated(client):
    response = client.get("/companies")
    assert response.status_code == 401

def test_create_company_unauthenticated(client):
    company_data = {
        "name": "Test Company",
        "description": "Test Description",
        "mode": "active",
        "rating": "5"
    }
    
    response = client.post("/companies", json=company_data)
    assert response.status_code == 401