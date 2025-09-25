from fastapi import APIRouter, Depends, Query, HTTPException
from starlette import status
from models.task import TaskModel, TaskViewModel
from database import get_db_context
from schemas import task
from sqlalchemy.orm import Session
from datetime import datetime
from schemas.user import User
from services.auth import token_interceptor

router = APIRouter(prefix="/tasks", tags=["Task"])


@router.get("", response_model=list[TaskViewModel])
async def get_tasks(
    title: str = Query(default=None),
    task_id: str = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    # query = db.query(task.Task).options(joinedload(task.Task.user, innerjoin=True), joinedload(task.Task.company, innerjoin=True))
    return db.query(task.Task).all()

# tuong tu cho post authenticate this function roi dung 
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskModel, db: Session = Depends(get_db_context)) -> None:
    task = task.Task(**request.model_dump())
    task.created_at = datetime.now()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
