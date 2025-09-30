import pytest
from uuid import uuid4
from models.user import UserModel, UserViewModel
from models.company import CompanyModel, CompanyViewModel
from models.task import TaskModel, TaskViewModel

def test_user_model():
    user = UserModel(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        password="password123",
        is_admin=True
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.is_admin == True

def test_user_view_model():
    user_id = uuid4()
    user = UserViewModel(
        id=user_id,
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password="hashed_password",
        is_active=True,
        is_admin=True
    )
    assert user.id == user_id
    assert user.email == "test@example.com"

def test_company_model():
    company = CompanyModel(
        name="Test Company",
        description="Test Description",
        mode="Test Mode",
        rating="5"
    )
    assert company.name == "Test Company"
    assert company.description == "Test Description"

def test_company_view_model():
    company_id = uuid4()
    company = CompanyViewModel(
        id=company_id,
        name="Test Company",
        description="Test Description",
        mode="Test Mode",
        rating="5"
    )
    assert company.id == company_id
    assert company.name == "Test Company"

def test_task_model():
    task = TaskModel(
        summary="Test Task",
        description="Test Description",
        status="Open",
        priority="High"
    )
    assert task.summary == "Test Task"
    assert task.status == "Open"

def test_task_view_model():
    task_id = uuid4()
    task = TaskViewModel(
        id=task_id,
        summary="Test Task",
        description="Test Description",
        status="Open",
        priority="High"
    )
    assert task.id == task_id
    assert task.summary == "Test Task"