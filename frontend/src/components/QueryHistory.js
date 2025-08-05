import React from 'react';
import { History, Clock, FileText, User, Bot } from 'lucide-react';

const QueryHistory = ({ history }) => {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatTime = (seconds) => {
    return `${seconds.toFixed(2)}s`;
  };

  if (history.length === 0) {
    return (
      <div className="p-6 text-center">
        <History className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No query history</h3>
        <p className="text-gray-600">
          Your question and answer history will appear here once you start asking questions.
        </p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Query History</h3>
        <p className="text-sm text-gray-600">
          View your past questions and AI responses with timing information.
        </p>
      </div>

      <div className="space-y-6">
        {history.map((query) => (
          <div
            key={query.id}
            className="bg-gray-50 rounded-lg p-4 border border-gray-200"
          >
            {/* Question */}
            <div className="mb-4">
              <div className="flex items-start space-x-2">
                <User className="h-5 w-5 mt-0.5 text-primary-600" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 mb-1">Question:</p>
                  <p className="text-sm text-gray-700">{query.question}</p>
                </div>
              </div>
            </div>

            {/* Answer */}
            <div className="mb-4">
              <div className="flex items-start space-x-2">
                <Bot className="h-5 w-5 mt-0.5 text-gray-600" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 mb-1">Answer:</p>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">{query.response}</p>
                </div>
              </div>
            </div>

            {/* Metadata */}
            <div className="flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-200">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-1">
                  <Clock className="h-3 w-3" />
                  <span>{formatTime(query.response_time)}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <History className="h-3 w-3" />
                  <span>{formatDate(query.timestamp)}</span>
                </div>
              </div>
              
              {query.source_documents && (
                <div className="flex items-center space-x-1">
                  <FileText className="h-3 w-3" />
                  <span>
                    {JSON.parse(query.source_documents).length} source(s)
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-700">
          <strong>Note:</strong> This history shows your recent questions and the AI's responses. 
          Response times include both vector search and LLM processing time.
        </p>
      </div>
    </div>
  );
};

export default QueryHistory; 