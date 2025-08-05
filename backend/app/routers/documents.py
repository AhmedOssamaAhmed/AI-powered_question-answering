from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import json
from app.database import get_db
from app.models import User, Document
from app.schemas import DocumentResponse
from app.auth import get_current_active_user
from app.document_processor import DocumentProcessor
from app.vector_store import vector_store_manager

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a document for processing"""
    
    # Read file content
    file_content = await file.read()
    
    # Validate file size (10MB limit)
    if not DocumentProcessor.validate_file_size(file_content, max_size_mb=10):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large. Maximum size is 10MB."
        )
    
    try:
        # Extract text from file
        text_content, file_type = DocumentProcessor.extract_text_from_file(file_content, file.filename)
        
        # Validate content
        if not DocumentProcessor.validate_file_content(text_content):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File content is too short or empty."
            )
        
        # Save document to database
        db_document = Document(
            user_id=current_user.id,
            filename=file.filename,
            file_type=file_type,
            content=text_content
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Add to vector store
        document_data = {
            'id': db_document.id,
            'filename': db_document.filename,
            'content': db_document.content
        }
        
        try:
            vector_ids = vector_store_manager.add_documents([document_data], current_user.id)
            print(f"✅ Document added to vector store with IDs: {vector_ids}")
            
            # Force persistence to ensure data is saved
            vector_store_manager.vectorstore.persist()
            
        except Exception as e:
            print(f"❌ Error adding document to vector store: {e}")
            # Continue anyway as the document is saved in the database
        
        return db_document
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all documents for the current user"""
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"} 