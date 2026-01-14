import React, { useState } from "react";
import { Send } from "lucide-react";
import { useAppStore } from "../store/appStore";
import { submitQuery } from "../services/api";

export default function QueryForm() {
  const [localQuery, setLocalQuery] = useState("");
  const indexId = useAppStore((state) => state.indexId);
  const setResults = useAppStore((state) => state.setResults);
  const setLoading = useAppStore((state) => state.setLoading);
  const setError = useAppStore((state) => state.setError);
  const loading = useAppStore((state) => state.loading);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!indexId) {
      setError("Please upload documents first");
      return;
    }

    if (!localQuery.trim()) {
      setError("Please enter a query");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await submitQuery(localQuery, indexId);
      setResults(result);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to process query");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
          <Send className="w-6 h-6" />
          Ask a Question
        </h2>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Query
          </label>
          <textarea
            value={localQuery}
            onChange={(e) => setLocalQuery(e.target.value)}
            disabled={!indexId || loading}
            placeholder="Enter your question here..."
            rows="4"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
        </div>

        <div className="text-sm text-gray-600 mb-4">
          {indexId ? (
            <p className="text-green-600 flex items-center gap-1">
              ✓ Documents indexed and ready
            </p>
          ) : (
            <p className="text-yellow-600">
              ⚠ Upload documents first to enable queries
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={!indexId || loading || !localQuery.trim()}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
              Processing...
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              Submit Query
            </>
          )}
        </button>
      </form>
    </div>
  );
}
