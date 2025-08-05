import PyPDF2
import io
from typing import Tuple
import magic


class DocumentProcessor:
    @staticmethod
    def extract_text_from_file(file_content: bytes, filename: str) -> Tuple[str, str]:
        """Extract text content from uploaded file"""
        
        # Detect file type
        file_type = magic.from_buffer(file_content, mime=True)
        
        if file_type == "text/plain":
            # Handle .txt files
            try:
                text = file_content.decode('utf-8')
                return text, "txt"
            except UnicodeDecodeError:
                try:
                    text = file_content.decode('latin-1')
                    return text, "txt"
                except:
                    raise ValueError("Unable to decode text file")
        
        elif file_type == "application/pdf":
            # Handle .pdf files
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text, "pdf"
            except Exception as e:
                raise ValueError(f"Error processing PDF file: {str(e)}")
        
        else:
            raise ValueError(f"Unsupported file type: {file_type}. Only .txt and .pdf files are supported.")
    
    @staticmethod
    def validate_file_size(file_content: bytes, max_size_mb: int = 10) -> bool:
        """Validate file size"""
        size_mb = len(file_content) / (1024 * 1024)
        return size_mb <= max_size_mb
    
    @staticmethod
    def validate_file_content(text: str, min_length: int = 10) -> bool:
        """Validate that the extracted text has meaningful content"""
        return len(text.strip()) >= min_length 