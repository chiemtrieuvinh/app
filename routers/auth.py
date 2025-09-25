from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db_context
from services.auth import authenticate_user, create_access_token
from jose import jwt


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_context)                            
      ) -> None:
    #user
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create claim JWT token
    token = create_access_token(user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }