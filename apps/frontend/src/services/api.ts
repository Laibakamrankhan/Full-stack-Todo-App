import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle various error cases
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Remove token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    } else if (error.response?.status === 403) {
      // Handle forbidden access
      console.error('Access forbidden:', error.response.data);
    } else if (error.response?.status === 404) {
      // Handle not found
      console.error('Resource not found:', error.response.data);
    } else if (error.response?.status === 500) {
      // Handle server errors
      console.error('Server error:', error.response.data);
    }

    return Promise.reject(error);
  }
);

export default api;