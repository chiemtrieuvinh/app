from fastapi import APIRouter, Depends
from starlette import status
from database import LocalSession
from models.company import CompanyModel, CompanyViewModel
from sqlalchemy.orm import Session
from schemas import company
from database import get_db_context
from datetime import datetime


router = APIRouter(prefix="/companies", tags=["Company"])



@router.get("", response_model=list[CompanyViewModel])
async def get_companies(db: Session = Depends(get_db_context)):
    return db.query(company.Company).all()  # Example query to ensure DB session is used


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_company(request: CompanyModel, db: Session = Depends(get_db_context)) -> None:
    company = company.Company(**request.model_dump())
    company.created_at = datetime.now()
    db.add(company)
    db.commit()
    return {"message": "Company created"}
