# AI Question Answering System

A comprehensive AI-powered question-answering system built with FastAPI backend and React frontend. This application allows users to upload documents, generate embeddings, and ask questions using an LLM with vector similarity search.

## 🌐 Live Demo

**Test Version**: [http://16.16.129.60:3000/](http://16.16.129.60:3000/)

## 🚀 Features

- **User Authentication**: Secure JWT-based authentication system
- **Document Upload**: Support for PDF and TXT files with automatic text extraction
- **Vector Embeddings**: Document chunking and embedding generation using ChromaDB
- **AI Question Answering**: LLM-powered responses using OpenAI GPT-3.5-turbo
- **Query Logging**: Complete history of questions and responses
- **Multi-user Support**: Isolated document spaces for each user
- **Modern React Frontend**: Beautiful, responsive UI built with Tailwind CSS

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database for user data and query logs
- **ChromaDB**: Vector database for document embeddings
- **OpenAI**: GPT-3.5-turbo for question answering
- **JWT**: Authentication tokens

### Frontend
- **React 18**: Modern React with hooks
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Dropzone**: File upload component

## 📋 Prerequisites

- Node.js 18+ 
- Python 3.11+
- PostgreSQL database
- OpenAI API key

## 🚀 Quick Start

### Automated Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-chatbot-system
   ```

2. **Start everything with one command**
   
   **Windows:**
   ```bash
   start-local.bat
   ```
   
   **Linux/Mac:**
   ```bash
   ./start-local.sh
   ```

   This will automatically:
   - Check all prerequisites (Python, Node.js, Docker)
   - Start PostgreSQL in Docker
   - Set up backend environment and dependencies
   - Start backend server
   - Set up frontend dependencies
   - Start frontend server

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

1. **Start PostgreSQL with Docker**
   ```bash
   docker-compose up -d postgres
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   
   # Set up environment variables
   cp env.example .env
   # Edit .env with your configuration (OpenAI API key required)
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Start the services**
   ```bash
   # Backend (in backend directory)
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Frontend (in frontend directory)
   npm start
   ```

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user information

### Document Endpoints
- `POST /documents/upload` - Upload a document
- `GET /documents/` - List user's documents
- `DELETE /documents/{id}` - Delete a document

### Question Answering Endpoints
- `POST /qa/ask` - Ask a question
- `GET /qa/history` - Get query history

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Database (automatically configured with Docker)
DATABASE_URL=postgresql://user:password@localhost:5432/ai_qa_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI (required)
OPENAI_API_KEY=your-openai-api-key-here

# Vector Database
CHROMA_PERSIST_DIRECTORY=./chroma_db

# App Settings
DEBUG=True
ALLOWED_HOSTS=["*"]
```

#### Frontend
```env
REACT_APP_API_URL=http://localhost:8000
```

## 📊 Usage Guide

1. **Registration/Login**: Create an account or sign in
2. **Upload Documents**: Drag and drop PDF or TXT files (max 10MB each)
3. **Ask Questions**: Use the chat interface to ask questions about your documents
4. **View History**: Check your query history for past questions and answers
5. **Manage Documents**: View and delete uploaded documents

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- User isolation for documents and queries
- Input validation and sanitization
- CORS configuration
- File type and size validation

## 🚀 Deployment

### Production Deployment

1. **Update environment variables for production**
   ```bash
   SECRET_KEY=your-very-secure-secret-key
   DEBUG=False
   ALLOWED_HOSTS=["your-domain.com"]
   ```

2. **Set up production database**
   - Use a managed PostgreSQL service (AWS RDS, Google Cloud SQL, etc.)
   - Update DATABASE_URL in production environment

3. **Deploy backend to your preferred hosting service**
   - Render, Railway, Heroku, or AWS
   - Make sure to set up PostgreSQL database connection

4. **Deploy frontend**
   - Vercel, Netlify, or any static hosting service
   - Update REACT_APP_API_URL to point to your backend

## 🔧 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Check if Docker is running
docker info

# Check Docker Compose version
docker-compose --version
```

#### PostgreSQL Connection Issues
```bash
# Check if PostgreSQL container is running
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres
```

#### Backend Issues
```bash
# Check if virtual environment is activated
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Frontend Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 