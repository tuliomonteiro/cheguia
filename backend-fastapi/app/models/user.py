import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, String
from pydantic import EmailStr

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)
    language_preference: str = Field(default="es")
    is_premium: bool = False

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    hashed_password: str = Field(sa_column=Column("password", String))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
