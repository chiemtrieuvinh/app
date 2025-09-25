from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import User, verify_password
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from settings import JWT_SECRET, JWT_ALGORITHM
from fastapi.security import OAuth2PasswordBearer


oa2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(username: str, password: str, db: Session) -> bool:
    # Implement your user authentication logic here
    # For demonstration purposes, we'll just check if the username and password are the same
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(user: User, exipres:Optional[timedelta] = None) -> str:
    claims = {
        "sub": user.username,
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_admin": user.is_admin
    }
    expires_in = datetime.now() + (exipres if exipres else timedelta(minutes=5))
    claims.update({"exp": expires_in})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


def token_interceptor(token: str = Depends(oa2_bearer)) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = User()
        user.username = payload.get("sub")
        user.id = payload.get("id")
        user.first_name = payload.get("first_name")
        user.last_name = payload.get("last_name")
        user.email = payload.get("email")
        user.is_admin = payload.get("is_admin") 

        if(user.username is None or user.id is None):
            raise token_exception()
        return user
    except jwt.JWTError:
            raise token_exception()

def token_exception():
    raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )