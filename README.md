# Alosra Recipez - Backend API

![Alosra Recipez Logo](https://via.placeholder.com/400x200/007AFF/FFFFFF?text=Alosra+Recipez+API)

## Overview

**Alosra Recipez Backend** is a FastAPI-powered REST API that serves as the backbone for the Alosra Recipe Kit mobile application. This API provides comprehensive recipe management, user authentication, cart functionality, and order processing for a recipe-to-ingredients delivery service in partnership with Alosra Supermarket in Bahrain.

### What It Does
- **Recipe Management**: Browse recipes by categories (Arabic, Asian, Italian, Healthy options)
- **User Authentication**: Secure JWT-based authentication system
- **Cart Management**: Add recipes with dynamic serving size calculations
- **Order Processing**: Convert cart items to orders with delivery tracking
- **User Profiles**: Manage customer information and delivery addresses

### Why We Built It
The traditional grocery shopping experience for cooking specific dishes involves guesswork with ingredient quantities and measurements. Alosra Recipez solves this by partnering with local supermarkets to deliver pre-measured ingredients with professional cooking guidance, making home cooking accessible and enjoyable for busy families and cooking enthusiasts in Bahrain.

## 🚀 Getting Started

### Live API
- **Production API**: `https://alosra-recipez-api.onrender.com` *(will be updated after deployment)*
- **API Documentation**: `https://alosra-recipez-api.onrender.com/docs`

### Planning Materials
- **Trello Board**: [Project Planning & Development Tracking](https://trello.com/b/your-board-id/alosra-recipez-development)
- **ERD & System Design**: Available in Trello board under "System Design & ERD"

## 🛠️ Technologies Used

### Core Framework
- **FastAPI** - Modern, fast Python web framework for building APIs
- **Python 3.9+** - Programming language
- **Uvicorn** - ASGI server for FastAPI

### Database & ORM
- **PostgreSQL** - Primary database for production
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Alembic** - Database migration tool

### Authentication & Security
- **JWT (JSON Web Tokens)** - Secure user authentication
- **Passlib with bcrypt** - Password hashing
- **Python-JOSE** - JWT token encoding/decoding

### Development & Validation
- **Pydantic** - Data validation and serialization
- **Python-dotenv** - Environment variable management
- **CORS Middleware** - Cross-origin resource sharing for mobile app

### Testing & Documentation
- **Pytest** - Testing framework
- **FastAPI Auto-docs** - Automatic API documentation
- **Swagger/OpenAPI** - Interactive API documentation

## 📁 Project Structure

```
alosra-recipez-backend/
├── config/
│   └── enviroment.py        # Environment configuration & settings
├── controllers/
│   ├── cart_controller.py   # Cart management endpoints
│   ├── category_controller.py # Category management endpoints
│   ├── order_controller.py  # Order processing endpoints
│   ├── recipe_controller.py # Recipe endpoints
│   └── user_controller.py   # User management endpoints
├── dependencies/
│   └── auth.py             # Authentication dependencies
├── models/
│   ├── base.py             # Base model with common fields
│   ├── cart.py             # Cart model
│   ├── category.py         # Category model
│   ├── order.py            # Order & OrderItem models
│   ├── recipe.py           # Recipe model
│   └── user.py             # User database model
├── serializers/
│   ├── cart_serializers.py # Cart request/response schemas
│   ├── category_serializers.py # Category schemas
│   ├── order_serializers.py # Order schemas
│   ├── recipe_serializers.py # Recipe schemas
│   └── user_serializers.py # User schemas
├── utils/
│   └── security.py         # Security utilities & password hashing
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore file
├── database.py            # Database initialization & session management
├── main.py                # FastAPI application entry point
├── Pipfile                # Pipenv dependency file
├── Pipfile.lock           # Locked dependency versions
├── README.md              # This file
├── requirements.txt       # Python dependencies
└── seed.py                # Sample data seeding script
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- PostgreSQL database
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Alosra-Recipez-Backend.git
cd Alosra-Recipez-Backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your database credentials
```

### 5. Environment Variables
Create a `.env` file with the following variables:
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/alosra_recipez_db

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=Alosra Recipez API
DEBUG=True
API_V1_STR=/api/v1
```

### 6. Database Setup
```bash
# Create database tables
python -c "from database import create_tables; create_tables()"

# Seed sample data
python seed.py
```

### 7. Run Development Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /users/me` - Get current user profile
- `PUT /users/profile` - Update user profile

### Categories & Recipes
- `GET /categories` - List all categories
- `GET /categories/{category_id}` - Get category details
- `GET /categories/{category_id}/recipes` - Get recipes by category
- `GET /recipes` - List all recipes with optional filtering
- `GET /recipes/{recipe_id}` - Get recipe details

### Cart Management
- `GET /cart` - Get user's cart
- `POST /cart/add` - Add item to cart
- `PUT /cart/item/{item_id}` - Update cart item quantity
- `DELETE /cart/item/{item_id}` - Remove cart item
- `DELETE /cart/clear` - Clear entire cart

### Order Processing
- `POST /orders` - Create new order from cart
- `GET /orders` - Get user's order history
- `GET /orders/{order_id}` - Get order details
- `PUT /orders/{order_id}/status` - Update order status

### Example API Usage
```bash
# Register new user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ahmed Al-Mansoori",
    "email": "ahmed@example.com",
    "password": "securepassword",
    "phone": "+973-1234-5678",
    "address": "Manama, Bahrain"
  }'

# Get all categories
curl -X GET "http://localhost:8000/categories" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Add recipe to cart
curl -X POST "http://localhost:8000/cart/add" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "recipe_id": 1,
    "number_of_people": 4
  }'
```

## 🗄️ Database Schema

### Key Entities
- **Users**: Customer accounts with authentication and profile information
- **Categories**: Recipe categories (Arabic, Asian, Italian, Healthy Options)
- **Recipes**: Individual recipes with pricing, difficulty, and preparation details
- **Orders**: Customer orders with delivery information and status tracking
- **Order Items**: Individual recipes within orders with quantities and pricing
- **Cart Items**: Temporary shopping cart storage with user-specific items

### Base Model Features
All models inherit from `BaseModel` which provides:
- `id`: Primary key (auto-incrementing integer)
- `created_at`: Timestamp when record was created
- `updated_at`: Timestamp when record was last modified

### Relationships
- Users → Orders (1:N)
- Users → Cart Items (1:N)
- Categories → Recipes (1:N)
- Recipes → Order Items (1:N)
- Recipes → Cart Items (1:N)
- Orders → Order Items (1:N)

### Key Features
- **Unique Constraints**: Cart items are unique per user-recipe combination
- **Cascade Deletes**: User deletion removes associated orders and cart items
- **Price Calculations**: Dynamic pricing based on number of people served
- **Order Status Tracking**: Pending → Confirmed → Preparing → Out for Delivery → Delivered

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Test Categories
- **Authentication Tests**: User registration, login, JWT validation
- **Recipe Tests**: Category listing, recipe retrieval, filtering
- **Cart Tests**: Add/remove items, quantity updates, price calculations
- **Order Tests**: Order creation, status updates, history retrieval

## 🚀 Deployment

### Render Deployment
```bash
# Connect your GitHub repository to Render

# Create new Web Service on Render Dashboard
# 1. Connect GitHub repository
# 2. Choose branch (main/master)
# 3. Set build and start commands
```

### Render Configuration
```yaml
# render.yaml (optional - for infrastructure as code)
services:
  - type: web
    name: alosra-recipez-api
    runtime: python3
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
```

### Render Dashboard Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment**: Python 3.9+
- **Auto-Deploy**: Enable for main branch

### Database Setup on Render
```bash
# Add PostgreSQL database in Render Dashboard
# 1. Go to Dashboard > New > PostgreSQL
# 2. Choose database plan (Free tier available)
# 3. Copy DATABASE_URL from database dashboard
# 4. Add DATABASE_URL to web service environment variables
```

### Environment Variables for Production
```env
DATABASE_URL=postgresql://... (provided by Render PostgreSQL)
SECRET_KEY=your-strong-production-secret
DEBUG=False
APP_NAME=Alosra Recipez API
PORT=10000
PYTHON_VERSION=3.9.16
```

### Database Migration on Render
```bash
# After deployment, run database setup via Render Shell:
# 1. Go to your web service dashboard
# 2. Click "Shell" tab
# 3. Run migration commands:

python -c "from database import create_tables; create_tables()"
python seed.py
```

## 📊 Performance & Monitoring

### Database Optimization
- Foreign key indexes on all relationship columns
- Composite indexes on frequently queried combinations
- Database connection pooling for production
- Lazy loading with `joinedload` for related data

### API Performance
- Efficient SQLAlchemy queries with proper joins
- Response serialization with Pydantic
- Request/response validation and error handling
- Optimized cart and order calculations

### Monitoring (Production)
- Application logs with structured logging
- Database query performance monitoring
- API endpoint response time tracking
- Error tracking and alerting

## 🔒 Security Features

- **JWT Authentication** with configurable expiration times
- **Password Hashing** using bcrypt with salt via Passlib
- **Input Validation** with comprehensive Pydantic schemas
- **SQL Injection Protection** through SQLAlchemy ORM
- **CORS Configuration** for secure mobile app access
- **User Authorization** ensuring users can only access their own data
- **Secure Password Requirements** and validation

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and add tests
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

### Code Standards
- Follow PEP 8 Python style guide
- Add type hints to all function signatures
- Write unit tests for new features
- Update documentation for API changes
- Use meaningful variable and function names

## 📝 Next Steps

### Planned Enhancements
- **Real-time Order Tracking**: WebSocket integration for live order status updates
- **Payment Gateway Integration**: Stripe or local Bahraini payment processors
- **Recipe Recommendations**: ML-based personalized recipe suggestions
- **Inventory Management**: Real-time ingredient availability checking
- **Admin Dashboard**: Recipe and order management interface
- **Notification System**: Email/SMS notifications for order updates
- **Multi-language Support**: Arabic language interface
- **Advanced Search**: Full-text search with filters and sorting
- **Recipe Ratings & Reviews**: Customer feedback system
- **Nutritional Information**: Detailed nutritional data for recipes

### Performance Improvements
- Redis caching for frequently accessed data
- Database query optimization and advanced indexing
- Background task processing for order workflows
- API response compression and CDN integration
- Database connection pooling optimization

### Security Enhancements
- API rate limiting and throttling
- Enhanced input validation and sanitization
- Audit logging for all data modifications
- Two-factor authentication support
- Role-based access control (RBAC)

## 📞 Support & Contact

### Credits
- **Developer**: Zainab Nooh
- **Project Duration**: 7 Days sprint development
- **Institution**: General Assembly
- **Course**: Software Engineering Immersive
- **Instructor**: Kristina VanBergen-DeSilva, Arthur Bernier Jr
- **Trello**: [Board](https://trello.com/invite/b/68c887811e53f9b6c599fc93/ATTI1bb68c3e2b0734f35638a5acb7046e0e6D55DD19/alosra-recipez)
- **ERD**: [Alosra-Recipez-ERD](https://drive.google.com/file/d/1xK3a63Aosz0zBxTmPSNfPNyck5wx8n9E/view?usp=sharing)
- **Wireframe**: [Alosra-Recipez-Wireframe](https://excalidraw.com/#json=lpgfANaD60Ycjg9txNL5N,nmz9QW7U0urdnvqE_XcA8A)

### Issues & Bug Reports
- **GitHub Issues**: [Create Issue](https://github.com/zainab-nooh/Alosra-Recipez-Backend/issues)
- **Documentation**: Available in `/docs` endpoint when running
- **API Testing**: Use interactive docs at `/docs` for testing endpoints

### Business Context
This API was developed as part of a full-stack web development project, focusing on solving real-world problems in the Bahraini food delivery market by partnering with local supermarkets to provide pre-measured cooking ingredients with step-by-step cooking guidance.

### Mobile App Integration
This backend is specifically designed to work seamlessly with React Native/Expo frontend applications, providing:
- RESTful API endpoints optimized for mobile consumption
- JWT-based authentication suitable for mobile token storage
- JSON responses optimized for mobile data usage
- CORS configuration for cross-platform mobile development

---

## 📄 License

This project is developed for educational purposes as part of the General Assembly Software Engineering program.

---

**Built with ❤️ for the Bahraini cooking community**