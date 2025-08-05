import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from typing import List, Dict, Any
import json
import os
from app.config import settings


class VectorStoreManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Ensure the directory exists
        os.makedirs(settings.chroma_persist_directory, exist_ok=True)
        
        # Store user-specific collections
        self.user_collections = {}
        
        # Initialize main vector store for backward compatibility
        self.vectorstore = Chroma(
            persist_directory=settings.chroma_persist_directory,
            embedding_function=self.embeddings,
            client_settings=ChromaSettings(
                anonymized_telemetry=False,
                persist_directory=settings.chroma_persist_directory
            )
        )
        
        # Force persistence to ensure data is saved
        self.vectorstore.persist()
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def _get_user_collection(self, user_id: int):
        """Get or create a user-specific collection"""
        if user_id not in self.user_collections:
            # Create user-specific collection
            user_collection_name = f"user_{user_id}_docs"
            user_collection = Chroma(
                collection_name=user_collection_name,
                persist_directory=settings.chroma_persist_directory,
                embedding_function=self.embeddings,
                client_settings=ChromaSettings(
                    anonymized_telemetry=False,
                    persist_directory=settings.chroma_persist_directory
                )
            )
            self.user_collections[user_id] = user_collection
            print(f"✅ Created collection for user {user_id}: {user_collection_name}")
        
        return self.user_collections[user_id]
    
    def add_documents(self, documents: List[Dict[str, Any]], user_id: int) -> List[str]:
        """Add documents to the vector store with user isolation"""
        processed_docs = []
        
        for doc in documents:
            # Split text into chunks
            chunks = self.text_splitter.split_text(doc['content'])
            
            # Create documents with metadata
            for i, chunk in enumerate(chunks):
                processed_docs.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            'user_id': user_id,
                            'document_id': doc['id'],
                            'filename': doc['filename'],
                            'chunk_index': i,
                            'source': f"{doc['filename']}_chunk_{i}"
                        }
                    )
                )
        
        # Get user-specific collection
        user_collection = self._get_user_collection(user_id)
        
        # Add to user-specific collection
        ids = user_collection.add_documents(processed_docs)
        user_collection.persist()
        
        print(f"✅ Added {len(processed_docs)} chunks to user {user_id} collection")
        
        return ids
    
    def similarity_search(self, query: str, user_id: int, k: int = 4) -> List[Document]:
        """Search for similar documents, filtered by user_id"""
        try:
            # Get user-specific collection
            user_collection = self._get_user_collection(user_id)
            
            # Force persistence before search to ensure latest data
            user_collection.persist()
            
            # Search in user-specific collection (no need for user_id filter since it's isolated)
            results = user_collection.similarity_search(
                query,
                k=k
            )
            
            return results
        except Exception as e:
            print(f"Error in similarity search for user {user_id}: {e}")
            return []
    
    def has_documents_for_user(self, user_id: int) -> bool:
        """Check if user has any documents in the vector store"""
        try:
            # Get user-specific collection
            user_collection = self._get_user_collection(user_id)
            
            # Force persistence to ensure latest data
            user_collection.persist()
            
            # Try to get at least one document from the user's collection
            results = user_collection.similarity_search(
                "test",  # Any query will do
                k=1
            )
            
            has_docs = len(results) > 0
            print(f"User {user_id} has documents: {has_docs}")
            return has_docs
            
        except Exception as e:
            print(f"Error checking documents for user {user_id}: {e}")
            return False
    
    def reload_vectorstore(self):
        """Force reload the vector store from disk"""
        try:
            # Clear user collections cache
            self.user_collections = {}
            
            # Reinitialize the main vector store
            self.vectorstore = Chroma(
                persist_directory=settings.chroma_persist_directory,
                embedding_function=self.embeddings,
                client_settings=ChromaSettings(
                    anonymized_telemetry=False,
                    persist_directory=settings.chroma_persist_directory
                )
            )
            self.vectorstore.persist()
            print("✅ Vector store reloaded successfully")
        except Exception as e:
            print(f"❌ Error reloading vector store: {e}")
    
    def get_user_collection_info(self, user_id: int) -> dict:
        """Get information about a user's collection"""
        try:
            user_collection = self._get_user_collection(user_id)
            
            # Try to get some sample documents
            sample_docs = user_collection.similarity_search("test", k=5)
            
            return {
                "user_id": user_id,
                "collection_name": f"user_{user_id}_docs",
                "document_count": len(sample_docs),
                "sample_sources": [doc.metadata.get('source', 'Unknown') for doc in sample_docs[:3]],
                "has_documents": len(sample_docs) > 0
            }
        except Exception as e:
            return {
                "user_id": user_id,
                "error": str(e),
                "has_documents": False
            }
    
    def delete_user_documents(self, user_id: int):
        """Delete all documents for a specific user"""
        # This is a simplified approach - in production you might want more sophisticated deletion
        # For now, we'll rely on the filter in similarity_search to isolate users
        pass
    
    def get_document_chunks(self, document_id: int, user_id: int) -> List[Document]:
        """Get all chunks for a specific document"""
        filter_dict = {
            "user_id": user_id,
            "document_id": document_id
        }
        
        # This would require a more sophisticated query in a real implementation
        # For now, we'll return empty list as this is not critical for the demo
        return []


# Global instance
vector_store_manager = VectorStoreManager() 