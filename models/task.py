from pydantic import BaseModel, Field
from uuid import UUID


class TaskModel(BaseModel):
    summary: str = Field(min_length=1)
    description: str = Field(min_length=1)
    status: str = Field(min_length=1)
    priority: str = Field(min_length=1)


class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: str
    priority: str
    class Config:
        orm_mode = True