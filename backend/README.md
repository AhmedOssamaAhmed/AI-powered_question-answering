# AI Chatbot System - Backend

A FastAPI-based backend for an AI-powered question-answering system using LangChain, OpenAI, and PostgreSQL.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- OpenAI API key

### Local Development

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL:**
   ```bash
   # Install PostgreSQL if you haven't already
   # Create a database named 'ai_qa_db'
   # Update the DATABASE_URL in .env
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run the backend:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── document_processor.py # Document processing logic
│   ├── llm_service.py       # LLM integration
│   ├── vector_store.py      # Vector database operations
│   └── routers/             # API route handlers
│       ├── auth.py          # Authentication routes
│       ├── documents.py     # Document management routes
│       └── qa.py            # Question-answering routes
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_qa_db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key-here

# Vector Database
CHROMA_PERSIST_DIRECTORY=./chroma_db

# App Settings
DEBUG=True
ALLOWED_HOSTS=["*"]
```

### Database Connection

- **Local**: Requires PostgreSQL server running on localhost:5432
- **Production**: Update DATABASE_URL to point to your production database

## 🛠️ API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token

### Documents
- `POST /documents/upload` - Upload document
- `GET /documents/` - List documents
- `GET /documents/{id}` - Get document details
- `DELETE /documents/{id}` - Delete document

### Question Answering
- `POST /qa/ask` - Ask a question
- `GET /qa/history` - Get question history

### Health Check
- `GET /health` - Service health status
- `GET /` - API information

## 📊 Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `hashed_password`
- `created_at`
- `updated_at`

### Documents Table
- `id` (Primary Key)
- `filename`
- `file_path`
- `file_size`
- `file_type`
- `user_id` (Foreign Key)
- `created_at`
- `updated_at`

### Questions Table
- `id` (Primary Key)
- `question`
- `answer`
- `user_id` (Foreign Key)
- `document_id` (Foreign Key)
- `created_at`

## 🧪 Testing

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app
```

## 🔍 Troubleshooting

### Common Issues

1. **PostgreSQL Connection Error**
   - Ensure PostgreSQL server is running
   - Check if port 5432 is available
   - Verify database credentials in `.env`
   - Make sure the database 'ai_qa_db' exists

2. **Python-magic Error (Windows)**
   - The requirements.txt includes `python-magic-bin` for Windows compatibility
   - If issues persist, try: `pip uninstall python-magic python-magic-bin && pip install python-magic-bin`

3. **ChromaDB Issues**
   - Ensure the `chroma_db` directory exists and is writable
   - Check disk space for vector storage

4. **OpenAI API Issues**
   - Verify your OpenAI API key is set in `.env`
   - Check API key permissions and quota

### Logs and Debugging

```bash
# View backend logs (when running with uvicorn)
# Logs will appear in the terminal where you started the server

# Access PostgreSQL directly
psql -U your_username -d ai_qa_db -h localhost
```

## 📈 Performance Optimization

- **Database**: Use connection pooling for high concurrency
- **Vector Search**: ChromaDB is optimized for similarity search
- **Caching**: Consider Redis for session and query caching
- **File Processing**: Large files are processed asynchronously

## 🔒 Security Considerations

- Change default SECRET_KEY in production
- Use HTTPS in production
- Implement rate limiting
- Validate file uploads
- Use environment variables for sensitive data

## 📝 License

This project is part of the AI Chatbot System. 