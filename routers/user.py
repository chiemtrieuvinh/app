from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from models.user import UserModel, UserViewModel
from database import get_db_context
from sqlalchemy.orm import Session
from schemas import user
from datetime import datetime

router = APIRouter(prefix="/users", tags=["User"])


@router.get("", response_model=list[UserViewModel])
async def get_users(db: Session = Depends(get_db_context)):
    return db.query(user.User).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserModel, db: Session = Depends(get_db_context)) -> None:
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


# Todo need to create update methods in user schema
@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user_id: str, request: UserModel, db: Session = Depends(get_db_context)) -> None:
    update_user = db.query(user.User).filter(user.User.id == user_id).first()
    if update_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.update(request.model_dump())
    db.commit()
    return {"message": "User updated"}

# Todo need to create delete methods in user schema
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: Session = Depends(get_db_context)) -> None:
    user = db.query(user.User).filter(user.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}