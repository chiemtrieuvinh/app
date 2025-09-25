import uuid
from .base import Base 
from sqlalchemy import Column, String,  UUID, Integer
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    mode = Column(String, nullable=True)
    rating = Column(String, nullable=True)

    users = relationship("User", back_populates="company")
