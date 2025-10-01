import os
# Set JWT environment variables
os.environ['JWT_SECRET_KEY'] = 'test-secret-key-for-testing-only'
os.environ['JWT_ALGORITHM'] = 'HS256'

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas.base import Base
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from models.company import CompanyModel, CompanyViewModel
from models.user import UserModel, UserViewModel
from schemas.user import User
from services.auth import authenticate_user, create_access_token, token_interceptor
from schemas import company, user
from datetime import datetime
from schemas import company, user, task


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Create test routers with test database
auth_router = APIRouter(prefix="/auth", tags=["Auth"])
user_router = APIRouter(prefix="/users", tags=["User"])
company_router = APIRouter(prefix="/companies", tags=["Company"])

@auth_router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_test_db)
):
    user_obj = authenticate_user(form_data.username, form_data.password, db)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user_obj)
    return {"access_token": token, "token_type": "bearer"}

@user_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserModel, db = Depends(get_test_db)):
    user_data = request.model_dump()
    password = user_data.pop("password")
    hashed_password = user.get_password_hash(password)
    user_data["hashed_password"] = hashed_password
    user_data["is_active"] = True
    new_user = user.User(**user_data)
    new_user.created_at = datetime.now()
    db.add(new_user)
    db.commit()
    return {"message": "New user created"}

@company_router.get("", response_model=list[CompanyViewModel])
async def get_companies(
    user_obj: User = Depends(token_interceptor),
    db = Depends(get_test_db)
):
    return db.query(company.Company).all()

@company_router.post("", status_code=status.HTTP_201_CREATED)
async def create_company(
    request: CompanyModel,
    user_obj: User = Depends(token_interceptor),
    db = Depends(get_test_db)
):
    new_company = company.Company(**request.model_dump())
    db.add(new_company)
    db.commit()
    return {"message": "New company created"}

# Create test app
test_app = FastAPI()
test_app.include_router(auth_router)
test_app.include_router(user_router)
test_app.include_router(company_router)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(test_app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def admin_user():
    return {
        "email": "admin@example.com",
        "username": "admin", 
        "first_name": "Admin",
        "last_name": "User",
        "password": "adminpass123",
        "is_admin": True
    }

def get_auth_token(client: TestClient, user_data):
    client.post("/users", json=user_data)
    response = client.post("/auth/token", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    return response.json()["access_token"]

def test_get_companies_authenticated(client, admin_user):
    token = get_auth_token(client, admin_user)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/companies", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_company_authenticated(client, admin_user):
    token = get_auth_token(client, admin_user)
    headers = {"Authorization": f"Bearer {token}"}
    
    company_data = {
        "name": "Test Company",
        "description": "Test Description",
        "mode": "active",
        "rating": "5"
    }
    
    response = client.post("/companies", json=company_data, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "New company created"}

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