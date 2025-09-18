// React API Service Example
// Install: npm install axios

import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  // Register user
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  // Login user
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    const { token } = response.data;
    localStorage.setItem('token', token);
    return response.data;
  },

  // Get current user profile
  getProfile: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  // Update user profile
  updateProfile: async (userData) => {
    const response = await api.put('/auth/profile', userData);
    return response.data;
  },

  // Logout
  logout: () => {
    localStorage.removeItem('token');
  }
};

// Recipes API
export const recipesAPI = {
  // Get all recipes with optional filters
  getAll: async (params = {}) => {
    const response = await api.get('/api/recipes/', { params });
    return response.data;
  },

  // Get specific recipe
  getById: async (recipeId) => {
    const response = await api.get(`/api/recipes/${recipeId}`);
    return response.data;
  },

  // Get recipe with pricing
  getWithPricing: async (recipeId, people = 1) => {
    const response = await api.get(`/api/recipes/${recipeId}/pricing`, {
      params: { people }
    });
    return response.data;
  }
};

// Categories API
export const categoriesAPI = {
  // Get all categories
  getAll: async () => {
    const response = await api.get('/api/categories/');
    return response.data;
  }
};

// Cart API
export const cartAPI = {
  // Get cart items
  getItems: async () => {
    const response = await api.get('/api/cart/');
    return response.data;
  },

  // Add item to cart
  addItem: async (itemData) => {
    const response = await api.post('/api/cart/', itemData);
    return response.data;
  },

  // Update cart item
  updateItem: async (itemId, itemData) => {
    const response = await api.put(`/api/cart/${itemId}`, itemData);
    return response.data;
  },

  // Remove item from cart
  removeItem: async (itemId) => {
    const response = await api.delete(`/api/cart/${itemId}`);
    return response.data;
  }
};

// Orders API
export const ordersAPI = {
  // Get all orders
  getAll: async () => {
    const response = await api.get('/api/orders/');
    return response.data;
  },

  // Create new order
  create: async (orderData) => {
    const response = await api.post('/api/orders/', orderData);
    return response.data;
  },

  // Get specific order
  getById: async (orderId) => {
    const response = await api.get(`/api/orders/${orderId}`);
    return response.data;
  }
};

export default api;

