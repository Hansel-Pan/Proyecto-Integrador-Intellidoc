import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token de autenticación
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  // Let the browser add the multipart boundary for FormData requests.
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  }
  return config;
});

// Interceptor para manejar errores 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const authApi = {
  login: (correo, password) => {
    const formData = new FormData();
    formData.append('correo', correo);
    formData.append('password', password);
    return api.post('/auth/login', formData);
  },
  register: (data) => {
    const formData = new FormData();
    formData.append('nombre', data.nombre);
    formData.append('correo', data.correo);
    formData.append('password', data.password);
    formData.append('rol', data.rol || 'usuario');
    return api.post('/auth/register', formData);
  },
  me: () => api.get('/auth/me'),
  updateMe: (data) => api.put('/auth/me', data),
  listUsers: (params) => api.get('/auth/users', { params }),
  createUser: (data) => api.post('/auth/users', data),
  getUser: (id) => api.get(`/auth/users/${id}`),
  updateUser: (id, data) => api.put(`/auth/users/${id}`, data),
  deleteUser: (id) => api.delete(`/auth/users/${id}`),
};

// Repositories endpoints
export const repositoriesApi = {
  list: (params) => api.get('/repositories', { params }),
  create: (data) => api.post('/repositories', data),
  get: (id) => api.get(`/repositories/${id}`),
  update: (id, data) => api.put(`/repositories/${id}`, data),
  delete: (id) => api.delete(`/repositories/${id}`),
};

// Documents endpoints
export const documentsApi = {
  list: (params) => api.get('/documents', { params }),
  search: (params) => api.get('/documents/search', { params }),
  upload: (repositorioId, file) => {
    const formData = new FormData();
    formData.append('repositorio_id', repositorioId);
    formData.append('file', file);
    return api.post('/documents', formData);
  },
  get: (id) => api.get(`/documents/${id}`),
  download: (id) => api.get(`/documents/${id}/download`, { responseType: 'blob' }),
  update: (id, data) => api.put(`/documents/${id}`, data),
  delete: (id) => api.delete(`/documents/${id}`),
};

// Chat endpoints
export const chatApi = {
  ask: (data) => api.post('/chat', data),
  history: (params) => api.get('/chat/history', { params }),
};

// Dashboard endpoints
export const dashboardApi = {
  summary: (params) => api.get('/dashboard/summary', { params }),
  logs: (params) => api.get('/dashboard/logs', { params }),
  reprocess: (id) => api.post(`/dashboard/documents/${id}/reprocess`),
};

export default api;