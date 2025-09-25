from pydantic import BaseModel, Field
from uuid import UUID

class UserModel(BaseModel):
    email: str = Field(min_length=1)
    username: str = Field(min_length=1)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    password: str = Field(min_length=1)
    is_admin: bool = True

class UserViewModel(BaseModel):
    id: UUID
    email: str 
    username: str 
    username: str 
    first_name: str 
    last_name: str 
    hashed_password: str
    is_active: bool
    is_admin: bool
    class Config:
        orm_mode = True