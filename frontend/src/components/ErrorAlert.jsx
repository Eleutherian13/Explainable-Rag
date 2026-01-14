import React from 'react';
import { AlertCircle } from 'lucide-react';
import { useAppStore } from '../store/appStore';

export default function ErrorAlert() {
  const error = useAppStore((state) => state.error);
  const setError = useAppStore((state) => state.setError);

  if (!error) return null;

  return (
    <div className="fixed top-4 right-4 bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3 shadow-lg z-40 max-w-md">
      <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
      <div className="flex-1">
        <p className="text-sm font-medium text-red-800">{error}</p>
      </div>
      <button
        onClick={() => setError(null)}
        className="text-red-600 hover:text-red-800 font-bold"
      >
        ×
      </button>
    </div>
  );
}
