from sqlmodel import Session, select, create_engine
from app.models.document import Document
from app.core.config import settings

engine = create_engine(settings.DATABASE_URI)

def check_docs():
    with Session(engine) as db:
        docs = db.exec(select(Document)).all()
        print(f"Total documents: {len(docs)}")
        for doc in docs:
            has_emb = "YES" if doc.embedding_vector and len(doc.embedding_vector) > 0 else "NO"
            print(f"ID: {doc.id} | Title: {doc.title} | Type: {doc.document_type} | Vector: {has_emb} | Content Len: {len(doc.content)}")

if __name__ == "__main__":
    check_docs()
