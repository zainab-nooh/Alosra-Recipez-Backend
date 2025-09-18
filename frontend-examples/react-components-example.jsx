// React Components Example
// This shows how to use the API service in React components

import React, { useState, useEffect } from 'react';
import { authAPI, recipesAPI, categoriesAPI } from './react-api-service';

// Login Component
export const LoginForm = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await authAPI.login(credentials);
      onLogin(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={credentials.email}
          onChange={(e) => setCredentials({...credentials, email: e.target.value})}
          required
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={credentials.password}
          onChange={(e) => setCredentials({...credentials, password: e.target.value})}
          required
        />
      </div>
      {error && <div style={{color: 'red'}}>{error}</div>}
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};

// Registration Component
export const RegisterForm = ({ onRegister }) => {
  const [userData, setUserData] = useState({
    name: '',
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await authAPI.register(userData);
      onRegister(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name:</label>
        <input
          type="text"
          value={userData.name}
          onChange={(e) => setUserData({...userData, name: e.target.value})}
          required
        />
      </div>
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={userData.email}
          onChange={(e) => setUserData({...userData, email: e.target.value})}
          required
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={userData.password}
          onChange={(e) => setUserData({...userData, password: e.target.value})}
          required
        />
      </div>
      {error && <div style={{color: 'red'}}>{error}</div>}
      <button type="submit" disabled={loading}>
        {loading ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
};

// Recipes List Component
export const RecipesList = () => {
  const [recipes, setRecipes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category_id: '',
    difficulty: ''
  });

  useEffect(() => {
    loadData();
  }, [filters]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [recipesData, categoriesData] = await Promise.all([
        recipesAPI.getAll(filters),
        categoriesAPI.getAll()
      ]);
      setRecipes(recipesData);
      setCategories(categoriesData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({...prev, [key]: value}));
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Recipes</h2>
      
      {/* Filters */}
      <div style={{marginBottom: '20px'}}>
        <select 
          value={filters.category_id} 
          onChange={(e) => handleFilterChange('category_id', e.target.value)}
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
        
        <select 
          value={filters.difficulty} 
          onChange={(e) => handleFilterChange('difficulty', e.target.value)}
        >
          <option value="">All Difficulties</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      {/* Recipes Grid */}
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px'}}>
        {recipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </div>
  );
};

// Individual Recipe Card Component
export const RecipeCard = ({ recipe }) => {
  const [pricing, setPricing] = useState(null);
  const [people, setPeople] = useState(1);

  const loadPricing = async () => {
    try {
      const data = await recipesAPI.getWithPricing(recipe.id, people);
      setPricing(data);
    } catch (error) {
      console.error('Error loading pricing:', error);
    }
  };

  useEffect(() => {
    loadPricing();
  }, [recipe.id, people]);

  return (
    <div style={{border: '1px solid #ccc', padding: '15px', borderRadius: '8px'}}>
      <h3>{recipe.name}</h3>
      <p><strong>Category:</strong> {recipe.category?.name}</p>
      <p><strong>Difficulty:</strong> {recipe.difficulty}</p>
      <p><strong>Description:</strong> {recipe.description}</p>
      <p><strong>Base Price:</strong> ${recipe.base_price}</p>
      
      {pricing && (
        <div>
          <label>
            People: 
            <input 
              type="number" 
              min="1" 
              max="20" 
              value={people} 
              onChange={(e) => setPeople(parseInt(e.target.value))}
              style={{width: '60px', marginLeft: '5px'}}
            />
          </label>
          <p><strong>Total Price:</strong> ${pricing.calculated_price}</p>
        </div>
      )}
    </div>
  );
};

// Main App Component
export const App = () => {
  const [user, setUser] = useState(null);
  const [isLogin, setIsLogin] = useState(true);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    authAPI.logout();
    setUser(null);
  };

  if (!user) {
    return (
      <div>
        <h1>Alosra Recipez</h1>
        <button onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? 'Switch to Register' : 'Switch to Login'}
        </button>
        {isLogin ? (
          <LoginForm onLogin={handleLogin} />
        ) : (
          <RegisterForm onRegister={handleLogin} />
        )}
      </div>
    );
  }

  return (
    <div>
      <header style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px'}}>
        <h1>Alosra Recipez</h1>
        <div>
          <span>Welcome, {user.username}!</span>
          <button onClick={handleLogout} style={{marginLeft: '10px'}}>Logout</button>
        </div>
      </header>
      <main>
        <RecipesList />
      </main>
    </div>
  );
};

