import React, { useEffect, useState } from 'react';
import { useAppStore } from '../store/appStore';
import DocumentUpload from './DocumentUpload';
import QueryForm from './QueryForm';
import ResultsPanel from './ResultsPanel';
import GraphVisualization from './GraphVisualization';
import ErrorAlert from './ErrorAlert';
import { BarChart3, Info } from 'lucide-react';

export default function Dashboard() {
  const [showResults, setShowResults] = useState(false);
  const [activeTab, setActiveTab] = useState('upload');
  const indexId = useAppStore((state) => state.indexId);
  const results = useAppStore((state) => state.results);

  useEffect(() => {
    if (results) {
      setShowResults(true);
      setActiveTab('graph');
    }
  }, [results]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <ErrorAlert />

      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center gap-3 mb-2">
            <BarChart3 className="w-8 h-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-900">Explainable RAG</h1>
          </div>
          <p className="text-gray-600">Knowledge Graphs with AI-Powered Insights</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="space-y-8">
          {/* Upload and Query Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <DocumentUpload />
            <QueryForm />
          </div>

          {/* Results Section */}
          {results && (
            <div className="space-y-4">
              <div className="flex gap-2 border-b">
                <button
                  onClick={() => setActiveTab('answer')}
                  className={`px-4 py-2 font-semibold border-b-2 transition-colors ${
                    activeTab === 'answer'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Answer
                </button>
                <button
                  onClick={() => setActiveTab('graph')}
                  className={`px-4 py-2 font-semibold border-b-2 transition-colors ${
                    activeTab === 'graph'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Knowledge Graph
                </button>
                <button
                  onClick={() => setActiveTab('entities')}
                  className={`px-4 py-2 font-semibold border-b-2 transition-colors ${
                    activeTab === 'entities'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Entities ({results.entities?.length || 0})
                </button>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                {activeTab === 'answer' && (
                  <div>
                    <h3 className="text-xl font-bold mb-4">Generated Answer</h3>
                    <div className="text-gray-700 leading-relaxed">{results.answer}</div>
                  </div>
                )}

                {activeTab === 'graph' && (
                  <div>
                    <h3 className="text-xl font-bold mb-4">Knowledge Graph</h3>
                    <GraphVisualization graphData={results.graph_data} />
                  </div>
                )}

                {activeTab === 'entities' && (
                  <div>
                    <h3 className="text-xl font-bold mb-4">Extracted Entities</h3>
                    {results.entities && results.entities.length > 0 ? (
                      <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                          <thead className="bg-gray-100 border-b">
                            <tr>
                              <th className="px-4 py-2 text-left font-semibold text-gray-700">Name</th>
                              <th className="px-4 py-2 text-left font-semibold text-gray-700">Type</th>
                            </tr>
                          </thead>
                          <tbody>
                            {results.entities.map((entity, idx) => (
                              <tr key={idx} className="border-b hover:bg-gray-50">
                                <td className="px-4 py-2 text-gray-900">{entity.name}</td>
                                <td className="px-4 py-2">
                                  <span className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-semibold">
                                    {entity.type}
                                  </span>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    ) : (
                      <p className="text-gray-500">No entities found</p>
                    )}
                  </div>
                )}
              </div>

              {/* Source Snippets */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-xl font-bold mb-4">Source Snippets</h3>
                <div className="space-y-4">
                  {results.snippets && results.snippets.length > 0 ? (
                    results.snippets.map((snippet, idx) => (
                      <div
                        key={idx}
                        className="bg-gray-50 p-4 rounded border border-gray-200"
                      >
                        <p className="text-sm text-gray-600 mb-1 font-semibold">
                          Snippet {idx + 1}
                        </p>
                        <p className="text-gray-700 text-sm line-clamp-4">{snippet}</p>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500">No snippets available</p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Info Section */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-start gap-3">
              <Info className="w-6 h-6 text-blue-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-bold text-gray-900 mb-2">About This Application</h3>
                <p className="text-gray-600 text-sm mb-2">
                  This is an Explainable RAG system that uses knowledge graphs to provide
                  transparent, traceable answers grounded in your uploaded documents.
                </p>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Upload PDFs or text files to build a searchable knowledge base</li>
                  <li>• Ask natural language questions and receive grounded answers</li>
                  <li>• View extracted entities and relationships in an interactive graph</li>
                  <li>• Inspect source snippets to verify answer accuracy</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600 text-sm">
          <p>Explainable RAG with Knowledge Graphs © 2026</p>
        </div>
      </footer>
    </div>
  );
}
