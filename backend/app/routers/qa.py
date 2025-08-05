from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from app.database import get_db
from app.models import User, QueryLog
from app.schemas import QuestionRequest, QuestionResponse, QueryLogResponse
from app.auth import get_current_active_user
from app.vector_store import vector_store_manager
from app.llm_service import llm_service
from app.config import settings

router = APIRouter(prefix="/qa", tags=["question-answering"])


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    question_request: QuestionRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Ask a question and get an AI-powered answer"""
    
    try:
        # First check if user has any documents
        has_docs = vector_store_manager.has_documents_for_user(current_user.id)
        
        if not has_docs:
            # No documents found for user
            response = "I don't have any documents to search through. Please upload some documents first."
            response_time = 0.0
            source_documents = []
        else:
            # Search for relevant documents
            relevant_docs = vector_store_manager.similarity_search(
                question_request.question, 
                current_user.id
            )
            
            if not relevant_docs:
                # No relevant documents found for the specific question
                response = "I found your documents but couldn't find specific information to answer your question. Please try rephrasing your question or ask about a different topic."
                response_time = 0.0
                source_documents = []
            else:
                # Generate answer using LLM
                response, response_time = llm_service.answer_question_with_timing(
                    question_request.question, 
                    relevant_docs
                )
                
                # Extract source document information
                source_documents = [doc.metadata.get('source', 'Unknown') for doc in relevant_docs]
        
        # Log the query
        query_log = QueryLog(
            user_id=current_user.id,
            question=question_request.question,
            response=response,
            response_time=response_time,
            source_documents=json.dumps(source_documents) if source_documents else None
        )
        db.add(query_log)
        db.commit()
        
        return QuestionResponse(
            answer=response,
            response_time=response_time,
            source_documents=source_documents
        )
        
    except ValueError as e:
        if "OpenAI API key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service is not configured. Please contact the administrator to set up the OpenAI API key."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    except Exception as e:
        error_message = str(e)
        
        # Handle specific OpenAI errors
        if "insufficient_quota" in error_message or "quota" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenAI API quota exceeded. Please check your billing at https://platform.openai.com/account/billing or try again later."
            )
        elif "rate_limit" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please wait a moment and try again."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing question: {error_message}"
            )


@router.get("/history", response_model=List[QueryLogResponse])
async def get_query_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get query history for the current user"""
    query_logs = db.query(QueryLog).filter(
        QueryLog.user_id == current_user.id
    ).order_by(QueryLog.timestamp.desc()).all()
    
    return query_logs


@router.get("/debug/documents")
async def debug_user_documents(
    current_user: User = Depends(get_current_active_user)
):
    """Debug endpoint to check if user has documents in vector store"""
    try:
        # Get detailed collection information
        collection_info = vector_store_manager.get_user_collection_info(current_user.id)
        
        # Add additional info
        collection_info.update({
            "chroma_directory": settings.chroma_persist_directory,
            "total_user_collections": len(vector_store_manager.user_collections)
        })
        
        return collection_info
    except Exception as e:
        return {
            "user_id": current_user.id,
            "error": str(e),
            "has_documents": False
        }


@router.post("/debug/reload-vectorstore")
async def reload_vectorstore(
    current_user: User = Depends(get_current_active_user)
):
    """Debug endpoint to reload the vector store"""
    try:
        vector_store_manager.reload_vectorstore()
        
        # Check if documents are now available
        has_docs = vector_store_manager.has_documents_for_user(current_user.id)
        
        return {
            "message": "Vector store reloaded successfully",
            "user_id": current_user.id,
            "has_documents": has_docs
        }
    except Exception as e:
        return {
            "error": str(e),
            "user_id": current_user.id
        } 