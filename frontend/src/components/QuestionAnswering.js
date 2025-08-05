import React, { useState } from 'react';
import { Send, Bot, User, Clock, FileText } from 'lucide-react';
import toast from 'react-hot-toast';
import axios from 'axios';

const QuestionAnswering = ({ documents, onNewQuery }) => {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversation, setConversation] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      return;
    }

    if (documents.length === 0) {
      toast.error('Please upload some documents first before asking questions.');
      return;
    }

    const userMessage = {
      type: 'user',
      content: question,
      timestamp: new Date(),
    };

    setConversation(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await axios.post('/qa/ask', { 
        question: question.trim() 
      });

      const botMessage = {
        type: 'bot',
        content: response.data.answer,
        responseTime: response.data.response_time,
        sourceDocuments: response.data.source_documents,
        timestamp: new Date(),
      };

      setConversation(prev => [...prev, botMessage]);
      
      if (onNewQuery) {
        onNewQuery();
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to get answer');
    } finally {
      setLoading(false);
      setQuestion('');
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="p-6 h-[600px] flex flex-col">
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Ask Questions</h3>
        <p className="text-sm text-gray-600">
          Ask questions about your uploaded documents and get AI-powered answers.
        </p>
        {documents.length === 0 && (
          <div className="mt-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-sm text-yellow-700">
              <strong>No documents available.</strong> Please upload some documents first to start asking questions.
            </p>
          </div>
        )}
      </div>

      {/* Conversation Area */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {conversation.length === 0 ? (
          <div className="text-center py-8">
            <Bot className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h4 className="text-lg font-medium text-gray-900 mb-2">Start a conversation</h4>
            <p className="text-gray-600">
              Ask a question about your documents to get started.
            </p>
          </div>
        ) : (
          conversation.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-3xl rounded-lg p-4 ${
                  message.type === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <div className="flex items-start space-x-2">
                  {message.type === 'user' ? (
                    <User className="h-5 w-5 mt-0.5 flex-shrink-0" />
                  ) : (
                    <Bot className="h-5 w-5 mt-0.5 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    <p className="text-sm">{message.content}</p>
                    
                    {message.type === 'bot' && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <div className="flex items-center justify-between text-xs text-gray-500">
                          <div className="flex items-center space-x-2">
                            <Clock className="h-3 w-3" />
                            <span>{message.responseTime?.toFixed(2)}s</span>
                          </div>
                          {message.sourceDocuments && message.sourceDocuments.length > 0 && (
                            <div className="flex items-center space-x-1">
                              <FileText className="h-3 w-3" />
                              <span>{message.sourceDocuments.length} source(s)</span>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-4">
              <div className="flex items-center space-x-2">
                <Bot className="h-5 w-5" />
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your documents..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          disabled={loading || documents.length === 0}
        />
        <button
          type="submit"
          disabled={loading || !question.trim() || documents.length === 0}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
};

export default QuestionAnswering; 