# Paraguay Guide - FastAPI Backend

Modern, async-first backend for the Paraguay Guide application. Built with FastAPI, SQLModel, Alembic, and Ollama.

## Features
- **FastAPI**: High performance, easy to learn, fast to code, ready for production.
- **SQLModel**: Modern ORM combining SQLAlchemy and Pydantic.
- **Alembic**: Database migrations (configured for async).
- **JWT Authentication**: Secure stateless authentication.
- **RAG & AI**: 
    - Integration with local LLM via **Ollama**.
    - **RAG (Retrieval-Augmented Generation)**: Answers questions using your own documents.
    - **PDF Ingestion**: Upload PDFs to expand the knowledge base (uses PyMuPDF).

## Prerequisites
- Python 3.9+
- PostgreSQL
- [Ollama](https://ollama.ai/) running locally on port `11434`.

## Setup

1. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # Or using poetry if preferred, but requirements.txt is standard for now
   # We also need pymupdf, psycopg2-binary, etc. 
   # Check pyproject.toml for full list.
   ```

3. **Environment Variables**
   Create a `.env` file in `backend-fastapi/`:
   ```env
   PROJECT_NAME="Paraguay Guide API"
   POSTGRES_SERVER=localhost
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=paraguay_guide
   SECRET_KEY=your_secret_key
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=llama3.2:latest
   OLLAMA_EMBEDDING_MODEL=nomic-embed-text
   ```

4. **Initialize Database**
   ```bash
   alembic upgrade head
   ```

5. **Pull AI Models**
   ```bash
   ollama pull llama3.2:latest
   ollama pull nomic-embed-text
   ```

## Running the Server

```bash
cd backend-fastapi
./venv/bin/uvicorn app.main:app --reload --port 8000
```
- API Docs (Swagger UI): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key Endpoints

### Chat & AI
- `POST /api/v1/chat/`: Chat with the AI. Includes RAG context if relevant documents are found.
- `GET /api/v1/chat/status`: Check Ollama availability.

### Documents (RAG)
- `POST /api/v1/documents/`: Upload raw text/facts.
- `POST /api/v1/documents/upload-pdf`: Upload PDF file (auto-indexed).

### Auth
- `POST /api/v1/login/access-token`: Get JWT token.
- `POST /api/v1/users/`: Register new user.

## Project Structure
```
backend-fastapi/
├── app/
│   ├── api/            # API Endpoints (v1)
│   ├── core/           # Config & Security
│   ├── db/             # Database session
│   ├── models/         # SQLModel Database Models
│   └── services/       # Business Logic (Ollama, Documents)
├── alembic/            # Migration scripts
├── tests/              # Pytest suite
└── main.py             # Entry point
```
