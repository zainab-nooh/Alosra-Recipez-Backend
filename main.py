from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.user_controller import router as UserRouter
from controllers.category_controller import router as CategoryRouter
from controllers.recipe_controller import router as RecipeRouter
from controllers.cart_controller import router as CartRouter
from controllers.order_controller import router as OrderRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://127.0.0.1:8000',
        'http://localhost:19006',  # Expo web
        'http://127.0.0.1:19006',  # Expo web alternative
        'http://localhost:3000',   # React dev server
        'http://127.0.0.1:3000'    # React dev server alternative
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(UserRouter, prefix='/auth')
app.include_router(CategoryRouter, prefix='/api')
app.include_router(RecipeRouter, prefix='/api')
app.include_router(CartRouter, prefix='/api')
app.include_router(OrderRouter, prefix='/api')

@app.get('/')
def home():
    return {'message': 'Welcome to Alosra Recipe Kit API'}