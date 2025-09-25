import uuid
from .base import Base  # Import your models here to ensure they are registered
from sqlalchemy import Column, String, ForeignKey, UUID, Boolean
from passlib.context import CryptContext
from sqlalchemy.orm import relationship


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# create update or delete user later
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True)
    is_admin = Column(Boolean, nullable=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))

    company = relationship("Company", back_populates="users")
    tasks = relationship("Task", back_populates="user")



def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Implement your password verification logic here
    # For demonstration purposes, we'll just check if the passwords are the same
    return bcrypt_context.verify(plain_password, hashed_password)