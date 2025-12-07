import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('🚀 [AXIOS REQUEST]', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      fullURL: `${config.baseURL}${config.url}`,
      params: config.params,
      data: config.data,
      headers: config.headers,
      file: '/home/tapendra/Downloads/projects/news/frontend/src/services/api.js',
      timestamp: new Date().toISOString()
    });

    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔐 [AXIOS] Auth token added to request');
    }
    return config;
  },
  (error) => {
    console.error('❌ [AXIOS REQUEST ERROR]', {
      error: error.message,
      config: error.config
    });
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('✅ [AXIOS RESPONSE SUCCESS]', {
      status: response.status,
      statusText: response.statusText,
      url: response.config.url,
      method: response.config.method?.toUpperCase(),
      dataKeys: response.data ? Object.keys(response.data) : null,
      dataSize: JSON.stringify(response.data).length + ' bytes',
      headers: response.headers,
      data: response.data,
      timestamp: new Date().toISOString()
    });
    return response;
  },
  (error) => {
    console.error('❌ [AXIOS RESPONSE ERROR]', {
      message: error.message,
      url: error.config?.url,
      method: error.config?.method?.toUpperCase(),
      status: error.response?.status,
      statusText: error.response?.statusText,
      responseData: error.response?.data,
      errorType: error.response ? 'Server Error' : error.request ? 'Network Error' : 'Unknown Error',
      timestamp: new Date().toISOString()
    });

    if (error.response) {
      // Server responded with error
      console.error('🔴 [SERVER ERROR]', {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers
      });
    } else if (error.request) {
      // Request made but no response
      console.error('🔴 [NETWORK ERROR]', {
        request: error.request,
        message: 'No response received from server'
      });
    } else {
      // Something else happened
      console.error('🔴 [REQUEST SETUP ERROR]', {
        message: error.message
      });
    }
    return Promise.reject(error);
  }
);

export default api;
