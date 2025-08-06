# AI Question Answering System

A comprehensive AI-powered question-answering system built with FastAPI backend and React frontend. This application allows users to upload documents, generate embeddings, and ask questions using an LLM with vector similarity search.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure JWT-based authentication system
- **Document Upload**: Support for PDF and TXT files with automatic text extraction
- **Vector Embeddings**: Document chunking and embedding generation using ChromaDB
- **AI Question Answering**: LLM-powered responses using OpenAI GPT-3.5-turbo
- **Query Logging**: Complete history of questions and responses with timing
- **Multi-user Support**: Isolated document spaces for each user

### User Interface
- **Modern React Frontend**: Beautiful, responsive UI built with Tailwind CSS
- **Drag & Drop Upload**: Intuitive file upload interface
- **Real-time Chat**: Interactive question-answering interface
- **Document Management**: View and delete uploaded documents
- **Query History**: Browse past questions and answers

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │  PostgreSQL DB  │
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   ChromaDB      │
                       │  Vector Store   │
                       └─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database for user data and query logs
- **ChromaDB**: Vector database for document embeddings
- **LangChain**: Framework for LLM applications
- **OpenAI**: GPT-3.5-turbo for question answering
- **Sentence Transformers**: HuggingFace embeddings for document vectors
- **PyPDF2**: PDF text extraction
- **JWT**: Authentication tokens

### Frontend
- **React 18**: Modern React with hooks
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **React Dropzone**: File upload component
- **Lucide React**: Beautiful icons
- **React Hot Toast**: Toast notifications

## 📋 Prerequisites

- Node.js 18+ 
- Python 3.11+
- PostgreSQL database
- OpenAI API key

## 🚀 Quick Start

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-chatbot-system
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Set up environment variables
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Start PostgreSQL database**
   ```bash
   # Install PostgreSQL if you haven't already
   # Create a database named 'ai_qa_db'
   # Update the DATABASE_URL in backend/.env
   ```

5. **Start the backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

6. **Start the frontend**
   ```bash
   cd frontend
   npm start
   ```

7. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

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
DATABASE_URL=postgresql://user:password@localhost:5432/ai_qa_db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
CHROMA_PERSIST_DIRECTORY=./chroma_db
DEBUG=True
```

#### Frontend
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
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

2. **Deploy backend to your preferred hosting service**
   - Render, Railway, Heroku, or AWS
   - Make sure to set up PostgreSQL database

3. **Deploy frontend**
   - Vercel, Netlify, or any static hosting service
   - Update REACT_APP_API_URL to point to your backend

### Cloud Deployment Options

- **Render**: Easy deployment with automatic scaling
- **Railway**: Simple deployment with database
- **AWS EC2**: Full control over infrastructure
- **Vercel**: Frontend deployment
- **Heroku**: Backend deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Limitations

- File size limit: 10MB per document
- Supported formats: PDF and TXT only
- Vector search accuracy depends on document quality
- LLM responses may occasionally be inaccurate
- No real-time collaboration features

## 🔮 Future Enhancements

- Support for more document formats (DOCX, PPTX, etc.)
- Real-time collaboration
- Advanced document preprocessing
- Custom embedding models
- API rate limiting
- Advanced analytics and insights
- Mobile application
- Multi-language support

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the troubleshooting section

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- ChromaDB team for the vector database
- FastAPI and React communities
- All open-source contributors 