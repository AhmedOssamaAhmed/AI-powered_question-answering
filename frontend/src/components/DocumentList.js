import React from 'react';
import { FileText, Trash2, Calendar, File } from 'lucide-react';
import toast from 'react-hot-toast';
import axios from 'axios';

const DocumentList = ({ documents, onDelete }) => {
  const handleDelete = async (documentId) => {
    if (window.confirm('Are you sure you want to delete this document?')) {
      try {
        await axios.delete(`/documents/${documentId}`);
        toast.success('Document deleted successfully');
        if (onDelete) {
          onDelete();
        }
      } catch (error) {
        toast.error(error.response?.data?.detail || 'Failed to delete document');
      }
    }
  };

  const getFileIcon = (fileType) => {
    switch (fileType) {
      case 'pdf':
        return <FileText className="h-5 w-5 text-red-500" />;
      case 'txt':
        return <File className="h-5 w-5 text-blue-500" />;
      default:
        return <File className="h-5 w-5 text-gray-500" />;
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (documents.length === 0) {
    return (
      <div className="p-6 text-center">
        <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No documents uploaded</h3>
        <p className="text-gray-600">
          Upload your first document to start building your knowledge base.
        </p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-2">My Documents</h3>
        <p className="text-sm text-gray-600">
          Manage your uploaded documents. Click the trash icon to delete a document.
        </p>
      </div>

      <div className="space-y-4">
        {documents.map((document) => (
          <div
            key={document.id}
            className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors"
          >
            <div className="flex items-center space-x-4">
              {getFileIcon(document.file_type)}
              <div>
                <h4 className="text-sm font-medium text-gray-900">
                  {document.filename}
                </h4>
                <div className="flex items-center space-x-4 text-xs text-gray-500 mt-1">
                  <span className="flex items-center space-x-1">
                    <Calendar className="h-3 w-3" />
                    <span>{formatDate(document.uploaded_at)}</span>
                  </span>
                  <span className="capitalize">{document.file_type} file</span>
                </div>
              </div>
            </div>
            
            <button
              onClick={() => handleDelete(document.id)}
              className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
              title="Delete document"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-700">
          <strong>Note:</strong> Deleting a document will remove it from your knowledge base and it will no longer be available for question answering.
        </p>
      </div>
    </div>
  );
};

export default DocumentList; 