from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    id: str
    email: str = Field(min_length=3)

class TaskViewModel(BaseModel):
    id: str
    summary: str
    description: str
    status: str
    priority: str
    class Config:
        orm_mode = True