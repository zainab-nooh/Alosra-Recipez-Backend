// React Native/Expo API Service
// Install: expo install expo-secure-store
// Install: npm install axios

import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000', // Change this to your backend URL
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Add token to requests if available
api.interceptors.request.use(async (config) => {
  try {
    const token = await SecureStore.getItemAsync('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  } catch (error) {
    console.log('Error getting token:', error);
  }
  return config;
});

// Handle token expiration and network errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      await SecureStore.deleteItemAsync('auth_token');
      // You might want to navigate to login screen here
    }
    
    // Handle network errors
    if (!error.response) {
      error.message = 'Network error. Please check your connection.';
    }
    
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  // Register user
  register: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  },

  // Login user
  login: async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials);
      const { token } = response.data;
      
      // Store token securely
      await SecureStore.setItemAsync('auth_token', token);
      
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  },

  // Get current user profile
  getProfile: async () => {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get profile');
    }
  },

  // Update user profile
  updateProfile: async (userData) => {
    try {
      const response = await api.put('/auth/profile', userData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to update profile');
    }
  },

  // Logout
  logout: async () => {
    try {
      await SecureStore.deleteItemAsync('auth_token');
    } catch (error) {
      console.log('Error during logout:', error);
    }
  },

  // Check if user is logged in
  isLoggedIn: async () => {
    try {
      const token = await SecureStore.getItemAsync('auth_token');
      return !!token;
    } catch (error) {
      return false;
    }
  }
};

// Recipes API
export const recipesAPI = {
  // Get all recipes with optional filters
  getAll: async (params = {}) => {
    try {
      const response = await api.get('/api/recipes/', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch recipes');
    }
  },

  // Get specific recipe
  getById: async (recipeId) => {
    try {
      const response = await api.get(`/api/recipes/${recipeId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch recipe');
    }
  },

  // Get recipe with pricing
  getWithPricing: async (recipeId, people = 1) => {
    try {
      const response = await api.get(`/api/recipes/${recipeId}/pricing`, {
        params: { people }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch recipe pricing');
    }
  }
};

// Categories API
export const categoriesAPI = {
  // Get all categories
  getAll: async () => {
    try {
      const response = await api.get('/api/categories/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch categories');
    }
  }
};

// Cart API
export const cartAPI = {
  // Get cart items
  getItems: async () => {
    try {
      const response = await api.get('/api/cart/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch cart items');
    }
  },

  // Add item to cart
  addItem: async (itemData) => {
    try {
      const response = await api.post('/api/cart/', itemData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to add item to cart');
    }
  },

  // Update cart item
  updateItem: async (itemId, itemData) => {
    try {
      const response = await api.put(`/api/cart/${itemId}`, itemData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to update cart item');
    }
  },

  // Remove item from cart
  removeItem: async (itemId) => {
    try {
      const response = await api.delete(`/api/cart/${itemId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to remove item from cart');
    }
  }
};

// Orders API
export const ordersAPI = {
  // Get all orders
  getAll: async () => {
    try {
      const response = await api.get('/api/orders/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch orders');
    }
  },

  // Create new order
  create: async (orderData) => {
    try {
      const response = await api.post('/api/orders/', orderData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to create order');
    }
  },

  // Get specific order
  getById: async (orderId) => {
    try {
      const response = await api.get(`/api/orders/${orderId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch order');
    }
  }
};

export default api;

