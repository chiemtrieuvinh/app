import pytest
from unittest.mock import patch, MagicMock

def test_get_companies_success(client):
    mock_user = MagicMock()
    mock_user.is_admin = True
    
    with patch('routers.company.token_interceptor', return_value=mock_user), \
         patch('routers.company.company') as mock_company_schema:
        
        mock_companies = [MagicMock(), MagicMock()]
        mock_company_schema.Company = MagicMock()
        
        def mock_get_db():
            mock_db_session = MagicMock()
            mock_db_session.query.return_value.all.return_value = mock_companies
            yield mock_db_session
        
        with patch('routers.company.get_db_context', mock_get_db):
            response = client.get("/companies", headers={"Authorization": "Bearer test_token"})
            assert response.status_code == 200

def test_create_company_success(client):
    mock_user = MagicMock()
    mock_user.is_admin = True
    
    company_data = {
        "name": "Test Company",
        "description": "Test Description",
        "mode": "Test Mode",
        "rating": "5"
    }
    
    with patch('routers.company.token_interceptor', return_value=mock_user), \
         patch('routers.company.company') as mock_company_schema:
        
        mock_company_schema.Company = MagicMock()
        
        def mock_get_db():
            mock_db_session = MagicMock()
            yield mock_db_session
        
        with patch('routers.company.get_db_context', mock_get_db):
            response = client.post("/companies", 
                                 json=company_data,
                                 headers={"Authorization": "Bearer test_token"})
            assert response.status_code == 201
            assert response.json() == {"message": "New company created"}