import React, { useState, useEffect } from 'react';
import DocumentUpload from './DocumentUpload';
import QuestionAnswering from './QuestionAnswering';
import DocumentList from './DocumentList';
import QueryHistory from './QueryHistory';
import { FileText, MessageSquare, History, Upload } from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [documents, setDocuments] = useState([]);
  const [queryHistory, setQueryHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const tabs = [
    { id: 'upload', label: 'Upload Documents', icon: Upload },
    { id: 'documents', label: 'My Documents', icon: FileText },
    { id: 'qa', label: 'Ask Questions', icon: MessageSquare },
    { id: 'history', label: 'Query History', icon: History },
  ];

  const fetchDocuments = async () => {
    try {
      const response = await axios.get('/documents/');
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const fetchQueryHistory = async () => {
    try {
      const response = await axios.get('/qa/history');
      setQueryHistory(response.data);
    } catch (error) {
      console.error('Error fetching query history:', error);
    }
  };

  useEffect(() => {
    fetchDocuments();
    fetchQueryHistory();
  }, []);

  const handleDocumentUpload = () => {
    fetchDocuments();
  };

  const handleDocumentDelete = () => {
    fetchDocuments();
  };

  const handleNewQuery = () => {
    fetchQueryHistory();
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'upload':
        return <DocumentUpload onUpload={handleDocumentUpload} />;
      case 'documents':
        return <DocumentList documents={documents} onDelete={handleDocumentDelete} />;
      case 'qa':
        return <QuestionAnswering documents={documents} onNewQuery={handleNewQuery} />;
      case 'history':
        return <QueryHistory history={queryHistory} />;
      default:
        return <DocumentUpload onUpload={handleDocumentUpload} />;
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Dashboard</h2>
        <p className="text-gray-600">
          Upload documents, ask questions, and explore your AI-powered knowledge base.
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-8">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="bg-white rounded-lg shadow">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default Dashboard; 