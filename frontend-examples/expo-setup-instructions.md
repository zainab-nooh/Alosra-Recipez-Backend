# React Native/Expo Setup Instructions

## Prerequisites
1. Node.js installed on your system
2. Expo CLI installed globally: `npm install -g @expo/cli`
3. Expo Go app on your phone (for testing)

## Setup Steps

### 1. Create a new Expo project
```bash
# Navigate to your frontend folder (separate from backend)
cd /path/to/your/frontend/folder

# Create new Expo project
npx create-expo-app AlosraRecipezApp --template blank

# Navigate to the project
cd AlosraRecipezApp
```

### 2. Install required dependencies
```bash
# Install navigation dependencies
npm install @react-navigation/native @react-navigation/stack

# Install required Expo modules
npx expo install expo-secure-store

# Install HTTP client
npm install axios

# Install additional dependencies
npm install react-native-screens react-native-safe-area-context
```

### 3. Copy the provided files
Copy these files from the `frontend-examples` folder to your Expo project:

- `expo-api-service.js` → `src/services/api.js`
- `expo-auth-context.js` → `src/contexts/AuthContext.js`
- `expo-screens/LoginScreen.js` → `src/screens/LoginScreen.js`
- `expo-screens/RegisterScreen.js` → `src/screens/RegisterScreen.js`
- `expo-screens/RecipesScreen.js` → `src/screens/RecipesScreen.js`
- `expo-screens/RecipeDetailScreen.js` → `src/screens/RecipeDetailScreen.js`
- `expo-app.js` → `App.js` (replace the existing App.js)

### 4. Update your project structure
Create the following folder structure:
```
AlosraRecipezApp/
├── src/
│   ├── services/
│   │   └── api.js
│   ├── contexts/
│   │   └── AuthContext.js
│   └── screens/
│       ├── LoginScreen.js
│       ├── RegisterScreen.js
│       ├── RecipesScreen.js
│       └── RecipeDetailScreen.js
├── App.js
├── package.json
└── ...
```

### 5. Update import paths
In your `App.js`, update the import paths to match your folder structure:
```javascript
// Update these imports
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import RecipesScreen from './src/screens/RecipesScreen';
import RecipeDetailScreen from './src/screens/RecipeDetailScreen';
import { AuthProvider, useAuth } from './src/contexts/AuthContext';
```

### 6. Configure your backend URL
In `src/services/api.js`, update the baseURL to match your backend:
```javascript
const api = axios.create({
  baseURL: 'http://YOUR_BACKEND_IP:8000', // Change this to your actual backend IP
  // For local development, use your computer's IP address
  // For example: 'http://192.168.1.100:8000'
});
```

### 7. Start your backend
In your backend folder:
```bash
python main.py
```

### 8. Start your Expo app
In your frontend folder:
```bash
# Start the development server
npx expo start

# Or scan the QR code with Expo Go app
# Or run on specific platform
npx expo start --android
npx expo start --ios
```

## Important Notes

### Network Configuration
- Make sure your phone and computer are on the same WiFi network
- Use your computer's IP address instead of `localhost` in the API baseURL
- Find your IP address:
  - Windows: `ipconfig`
  - Mac/Linux: `ifconfig`

### CORS Configuration
Your backend is already configured with CORS for Expo. If you need to add more origins, update the `main.py` file:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
        'http://localhost:8081',
        'http://localhost:19006',  # Expo web
        'http://127.0.0.1:19006',  # Expo web alternative
        'http://localhost:3000',   # React dev server
        'http://127.0.0.1:3000',   # React dev server alternative
        'exp://192.168.1.100:19000',  # Add your Expo development URL
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
```

### Testing
1. Start your FastAPI backend: `python main.py`
2. Start your Expo app: `npx expo start`
3. Scan the QR code with Expo Go app
4. Test the authentication flow
5. Test the recipes listing and details

## Troubleshooting

### Common Issues
1. **Network Error**: Make sure both devices are on the same network and use the correct IP address
2. **CORS Error**: Check that your backend CORS configuration includes your Expo development URL
3. **Token Issues**: Make sure `expo-secure-store` is properly installed
4. **Navigation Error**: Ensure all navigation dependencies are installed

### Debug Tips
- Use `console.log()` to debug API calls
- Check the Expo development tools for error messages
- Use React Native Debugger for advanced debugging
- Check your backend logs for incoming requests

