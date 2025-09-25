from fastapi import APIRouter, Depends
from starlette import status
from database import LocalSession
from models.company import CompanyModel, CompanyViewModel
from sqlalchemy.orm import Session
from schemas import company
from database import get_db_context
from schemas.user import User
from services.auth import token_interceptor

router = APIRouter(prefix="/companies", tags=["Company"])



@router.get("", response_model=list[CompanyViewModel])
async def get_companies(
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)):
    return db.query(company.Company).all()  # Example query to ensure DB session is used


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_company(
    request: CompanyModel, 
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)) -> None:
    new_company = company.Company(**request.model_dump())
    db.add(new_company)
    db.commit()
    return {"message": "New company created"}
