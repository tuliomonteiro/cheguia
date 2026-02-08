import uuid
from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, Column, JSON

class ChatSessionBase(SQLModel):
    title: Optional[str] = None
    platform: str = "web"

class ChatSession(ChatSessionBase, table=True):
    __tablename__ = "chat_sessions"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships would require back_populates on User model too
    # For now keeping it simple without explicit relationship fields unless needed

class MessageBase(SQLModel):
    role: str
    content: str
    sources: List[str] = Field(default_factory=list, sa_column=Column(JSON))

class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    session_id: uuid.UUID = Field(foreign_key="chat_sessions.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
