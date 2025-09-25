from pydantic import BaseModel, Field
from uuid import UUID


class CompanyModel(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    mode: str = Field(min_length=1)
    rating: str = Field(min_length=1)

class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str
    mode: str
    rating: str 
    class Config:
        orm_mode = True