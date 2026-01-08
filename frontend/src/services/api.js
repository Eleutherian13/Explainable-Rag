import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const uploadDocuments = async (files) => {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('files', file);
  });

  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const submitQuery = async (query, indexId) => {
  const response = await api.post('/query', {
    query,
    index_id: indexId,
    top_k: 5,
  });

  return response.data;
};

export const getStatus = async () => {
  const response = await api.get('/status');
  return response.data;
};

export const clearSession = async (indexId) => {
  const response = await api.post('/clear', null, {
    params: { index_id: indexId },
  });
  return response.data;
};

export default api;
