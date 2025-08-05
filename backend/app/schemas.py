from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class DocumentUpload(BaseModel):
    filename: str
    content: str


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    response_time: float
    source_documents: Optional[List[str]] = None


class QueryLogResponse(BaseModel):
    id: int
    timestamp: datetime
    question: str
    response: str
    response_time: float
    source_documents: Optional[str] = None
    
    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True 