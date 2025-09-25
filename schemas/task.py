import uuid
from .base import Base  # Import your models here to ensure they are registered
from sqlalchemy import Column, String, ForeignKey, UUID, Integer
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summary = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")