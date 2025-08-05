from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.schema import Document
from typing import List
import time
import openai
from app.config import settings


class LLMService:
    def __init__(self):
        self.use_fallback = False
        
        if not settings.openai_api_key or settings.openai_api_key == "":
            self.use_fallback = True
            print("⚠️  OpenAI API key not configured. Using fallback mode.")
            return
        
        try:
            # Configure OpenAI for v1 API
            openai.api_key = settings.openai_api_key
            openai.api_base = "https://api.openai.com/v1"  # v1 API endpoint
            
            # Test the API key
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",  # Use standard model for v1
                temperature=0.7,
                openai_api_key=settings.openai_api_key,
                max_tokens=1000  # Limit response length to reduce costs
            )
        except Exception as e:
            print(f"⚠️  Failed to initialize OpenAI: {e}. Using fallback mode.")
            self.use_fallback = True
    
    def _fallback_answer(self, question: str, context_documents: List[Document]) -> str:
        """Simple fallback answer when OpenAI is not available"""
        if not context_documents:
            return "I don't have any documents to search through. Please upload some documents first."
        
        # Simple keyword matching fallback
        context = "\n\n".join([doc.page_content for doc in context_documents])
        question_lower = question.lower()
        
        # Check if any document contains keywords from the question
        relevant_parts = []
        for doc in context_documents:
            content_lower = doc.page_content.lower()
            if any(word in content_lower for word in question_lower.split() if len(word) > 3):
                relevant_parts.append(doc.page_content[:200] + "...")
        
        if relevant_parts:
            return f"Based on the documents, here's what I found:\n\n" + "\n\n".join(relevant_parts[:3])
        else:
            return "I found some documents but couldn't find specific information to answer your question. Please try rephrasing your question or upload more relevant documents."
    
    def answer_question(self, question: str, context_documents: List[Document]) -> str:
        """Generate an answer based on the question and context documents"""
        
        if self.use_fallback:
            return self._fallback_answer(question, context_documents)
        
        # Prepare context from documents
        context = "\n\n".join([doc.page_content for doc in context_documents])
        
        try:
            # Use OpenAI v1 API directly
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a helpful AI assistant that answers questions based on the provided context. 
                        Use only the information from the context to answer the question. If the context doesn't contain enough information to answer the question, 
                        say "I don't have enough information to answer this question based on the provided documents."
                        
                        Context:
                        {context}
                        """
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to keyword matching if API fails
            return self._fallback_answer(question, context_documents)
    
    def summarize_documents(self, context_documents: List[Document]) -> str:
        """Generate a summary of the provided documents"""
        
        if not context_documents:
            return "No documents to summarize. Please upload some documents first."
        
        if self.use_fallback:
            return self._fallback_summarize(context_documents)
        
        # Prepare context from documents
        context = "\n\n".join([doc.page_content for doc in context_documents])
        
        try:
            # Use OpenAI v1 API directly for summarization
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a helpful AI assistant that creates concise summaries of documents. 
                        Create a clear, well-structured summary that captures the main points and key information from the provided content.
                        Focus on the most important details and organize the summary logically."""
                    },
                    {
                        "role": "user",
                        "content": f"Please provide a comprehensive summary of the following documents:\n\n{context}"
                    }
                ],
                max_tokens=1500,  # Allow more tokens for summaries
                temperature=0.3   # Lower temperature for more focused summaries
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error during summarization: {e}")
            # Fallback to simple summary if API fails
            return self._fallback_summarize(context_documents)
    
    def _fallback_summarize(self, context_documents: List[Document]) -> str:
        """Simple fallback summarization when OpenAI is not available"""
        if not context_documents:
            return "No documents to summarize."
        
        # Create a simple summary by extracting key sentences
        all_content = "\n\n".join([doc.page_content for doc in context_documents])
        
        # Split into sentences and take first few
        sentences = all_content.split('. ')
        summary_sentences = sentences[:5]  # Take first 5 sentences
        
        return f"Summary of documents:\n\n{'. '.join(summary_sentences)}..."
    
    def answer_question_with_timing(self, question: str, context_documents: List[Document]) -> tuple[str, float]:
        """Generate an answer with timing information"""
        start_time = time.time()
        
        # Check if this is a summarization request
        question_lower = question.lower().strip()
        if any(word in question_lower for word in ['summarize', 'summary', 'summarise', 'summarization']):
            answer = self.summarize_documents(context_documents)
        else:
            answer = self.answer_question(question, context_documents)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        return answer, response_time


# Global instance
llm_service = LLMService() 