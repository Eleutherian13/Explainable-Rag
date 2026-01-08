import { create } from 'zustand';

export const useAppStore = create((set) => ({
  indexId: null,
  documents: [],
  query: '',
  results: null,
  loading: false,
  error: null,

  setIndexId: (indexId) => set({ indexId }),
  setDocuments: (documents) => set({ documents }),
  setQuery: (query) => set({ query }),
  setResults: (results) => set({ results }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  
  reset: () => set({
    indexId: null,
    documents: [],
    query: '',
    results: null,
    loading: false,
    error: null
  })
}));
