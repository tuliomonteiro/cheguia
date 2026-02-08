import uuid
from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, JSON

class DocumentBase(SQLModel):
    title: str
    content: str
    source_url: Optional[str] = None
    document_type: str
    language: str = "es"
    embedding_vector: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))

class Document(DocumentBase, table=True):
    __tablename__ = "documents"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DocumentTemplateBase(SQLModel):
    name: str
    template_type: str
    template_content: str
    fields: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    is_premium: bool = False

class DocumentTemplate(DocumentTemplateBase, table=True):
    __tablename__ = "document_templates"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
