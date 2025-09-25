from pydantic import BaseModel, Field


class CompanyModel(BaseModel):
    id: str
    email: str = Field(min_length=3)

class CompanyViewModel(BaseModel):
    id: str
    name: str
    description: str
    mode: str
    rating: str 
    class Config:
        orm_mode = True