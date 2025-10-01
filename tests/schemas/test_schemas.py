import pytest
from schemas.user import User
from schemas.company import Company
from schemas.task import Task
from uuid import uuid4

def test_user_schema():
    user = User()
    user.id = uuid4()
    user.email = "test@example.com"
    user.username = "testuser"
    user.first_name = "Test"
    user.last_name = "User"
    user.is_active = True
    user.is_admin = False
    
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.is_active == True

def test_company_schema():
    company = Company()
    company.id = uuid4()
    company.name = "Test Company"
    company.description = "Test Description"
    company.mode = "Test Mode"
    company.rating = "5"
    
    assert company.name == "Test Company"
    assert company.description == "Test Description"

def test_task_schema():
    task = Task()
    task.id = uuid4()
    task.summary = "Test Task"
    task.description = "Test Description"
    task.status = "Open"
    task.priority = "High"
    
    assert task.summary == "Test Task"
    assert task.status == "Open"