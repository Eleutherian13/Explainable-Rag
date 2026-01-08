import React from 'react';
import { Copy, Download, X } from 'lucide-react';

export default function ResultsPanel({ results, onClose }) {
  const [copied, setCopied] = React.useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(results.answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadResults = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'results.json';
    link.click();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-96 overflow-y-auto">
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center">
          <h3 className="text-xl font-bold">Query Results</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Answer */}
          <section>
            <h4 className="text-lg font-semibold mb-2">Answer</h4>
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <p className="text-gray-800">{results.answer}</p>
              <button
                onClick={copyToClipboard}
                className="mt-2 text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
              >
                <Copy className="w-4 h-4" />
                {copied ? 'Copied!' : 'Copy answer'}
              </button>
            </div>
          </section>

          {/* Entities */}
          {results.entities && results.entities.length > 0 && (
            <section>
              <h4 className="text-lg font-semibold mb-2">Extracted Entities</h4>
              <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto">
                {results.entities.map((entity, idx) => (
                  <div
                    key={idx}
                    className="bg-green-50 p-3 rounded border border-green-200 text-sm"
                  >
                    <p className="font-semibold text-gray-800">{entity.name}</p>
                    <p className="text-green-600 text-xs">{entity.type}</p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Snippets */}
          {results.snippets && results.snippets.length > 0 && (
            <section>
              <h4 className="text-lg font-semibold mb-2">Source Snippets</h4>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {results.snippets.map((snippet, idx) => (
                  <div
                    key={idx}
                    className="bg-gray-50 p-3 rounded border border-gray-200 text-sm text-gray-700"
                  >
                    <p className="line-clamp-3">{snippet}</p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Action buttons */}
          <div className="flex gap-2 pt-4 border-t">
            <button
              onClick={downloadResults}
              className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 flex items-center justify-center gap-2"
            >
              <Download className="w-4 h-4" />
              Download JSON
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
