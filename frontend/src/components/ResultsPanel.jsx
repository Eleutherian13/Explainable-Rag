import React from "react";
import { Copy, Download, X, ChevronDown, ChevronUp } from "lucide-react";

export default function ResultsPanel({ results, onClose }) {
  const [copied, setCopied] = React.useState(false);
  const [expandedAnswer, setExpandedAnswer] = React.useState(true);
  const [expandedSnippets, setExpandedSnippets] = React.useState({});

  const copyToClipboard = () => {
    navigator.clipboard.writeText(results.answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadResults = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "results.json";
    link.click();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-5xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center z-10">
          <h3 className="text-xl font-bold">Query Results</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="overflow-y-auto flex-1 p-6 space-y-6">
          {/* Answer Section */}
          <section>
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-lg font-semibold">AI Answer</h4>
              <button
                onClick={() => setExpandedAnswer(!expandedAnswer)}
                className="text-blue-600 hover:text-blue-800"
              >
                {expandedAnswer ? (
                  <ChevronUp className="w-5 h-5" />
                ) : (
                  <ChevronDown className="w-5 h-5" />
                )}
              </button>
            </div>
            {expandedAnswer && (
              <div className="bg-blue-50 p-5 rounded-lg border-2 border-blue-200">
                <p className="text-gray-800 whitespace-pre-wrap break-words leading-relaxed text-base">
                  {results.answer}
                </p>
                <button
                  onClick={copyToClipboard}
                  className="mt-4 text-sm text-blue-600 hover:text-blue-800 flex items-center gap-2 font-medium"
                >
                  <Copy className="w-4 h-4" />
                  {copied ? "Copied!" : "Copy answer"}
                </button>
              </div>
            )}
          </section>

          {/* Entities Section */}
          {results.entities && results.entities.length > 0 && (
            <section>
              <h4 className="text-lg font-semibold mb-3">
                Key Information (Entities)
              </h4>
              <div className="grid grid-cols-2 gap-3">
                {results.entities.map((entity, idx) => (
                  <div
                    key={idx}
                    className="bg-green-50 p-3 rounded-lg border border-green-200"
                  >
                    <p className="font-semibold text-gray-800 break-words">
                      {entity.name}
                    </p>
                    <p className="text-green-600 text-xs mt-1 uppercase tracking-wide">
                      {entity.type}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Source Snippets Section */}
          {results.snippets && results.snippets.length > 0 && (
            <section>
              <h4 className="text-lg font-semibold mb-3">
                Source Snippets ({results.snippets.length})
              </h4>
              <div className="space-y-2">
                {results.snippets.map((snippet, idx) => (
                  <div
                    key={idx}
                    className="border border-gray-300 rounded-lg overflow-hidden bg-white"
                  >
                    <button
                      onClick={() =>
                        setExpandedSnippets((prev) => ({
                          ...prev,
                          [idx]: !prev[idx],
                        }))
                      }
                      className="w-full p-3 flex items-center justify-between hover:bg-gray-50 transition text-left"
                    >
                      <span className="text-sm text-gray-700 font-medium flex-1">
                        Snippet {idx + 1}: {snippet.substring(0, 60).trim()}...
                      </span>
                      {expandedSnippets[idx] ? (
                        <ChevronUp className="w-5 h-5 text-gray-500 flex-shrink-0 ml-2" />
                      ) : (
                        <ChevronDown className="w-5 h-5 text-gray-500 flex-shrink-0 ml-2" />
                      )}
                    </button>
                    {expandedSnippets[idx] && (
                      <div className="border-t border-gray-200 p-4 bg-gray-50">
                        <p className="text-sm text-gray-700 whitespace-pre-wrap break-words leading-relaxed">
                          {snippet}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>

        {/* Footer */}
        <div className="border-t p-4 bg-gray-50">
          <button
            onClick={downloadResults}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition flex items-center justify-center gap-2 font-medium"
          >
            <Download className="w-4 h-4" />
            Download Results as JSON
          </button>
        </div>
      </div>
    </div>
  );
}
