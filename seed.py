from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from database import engine
from models.user import UserModel
from models.category import Category
from models.recipe import Recipe
from utils.security import hash_password
from database import get_db
from models.base import Base

from models import UserModel, Category, Recipe, Order, OrderItem, CartItem

# Create session
SessionLocal = sessionmaker(bind=engine)

def seed_categories():
    """Seed initial categories"""
    db = SessionLocal()
    
    categories_data = [
        {
            'name': 'Arabic Cuisine',
            'description': 'Traditional Middle Eastern and Bahraini dishes with authentic spices and flavors',
            'image_url': 'https://example.com/images/arabic-cuisine.jpg',
            'display_order': 1
        },
        {
            'name': 'Asian Cuisine',
            'description': 'Delicious flavors from across Asia - Japanese, Chinese, Thai, and Indian dishes',
            'image_url': 'https://example.com/images/asian-cuisine.jpg',
            'display_order': 2
        },
        {
            'name': 'Italian Cuisine',
            'description': 'Classic Italian recipes with fresh ingredients and traditional cooking methods',
            'image_url': 'https://example.com/images/italian-cuisine.jpg',
            'display_order': 3
        },
        {
            'name': 'Healthy Options',
            'description': 'Nutritious and balanced meals for a healthy lifestyle',
            'image_url': 'https://example.com/images/healthy-cuisine.jpg',
            'display_order': 4
        }
    ]
    
    for category_data in categories_data:
        # Check if category already exists
        existing_category = db.query(Category).filter(Category.name == category_data['name']).first()
        if not existing_category:
            category = Category(**category_data)
            db.add(category)
    
    db.commit()
    db.close()
    print("Categories seeded successfully!")

def seed_recipes():
    """Seed initial recipes"""
    db = SessionLocal()
    
    # Get category IDs
    arabic_category = db.query(Category).filter(Category.name == 'Arabic Cuisine').first()
    asian_category = db.query(Category).filter(Category.name == 'Asian Cuisine').first()
    italian_category = db.query(Category).filter(Category.name == 'Italian Cuisine').first()
    healthy_category = db.query(Category).filter(Category.name == 'Healthy Options').first()
    
    recipes_data = [
        # Arabic Cuisine
        {
            'name': 'Chicken Machboos',
            'description': 'Traditional Bahraini spiced rice dish with tender chicken, aromatic spices, and basmati rice. A beloved comfort food perfect for family gatherings.',
            'category_id': arabic_category.id,
            'base_price': Decimal('8.50'),
            'prep_time_minutes': 45,
            'difficulty': 'medium',
            'image_url': 'https://example.com/images/chicken-machboos.jpg'
        },
        {
            'name': 'Lamb Kabsa',
            'description': 'Aromatic rice dish with tender lamb, mixed vegetables, and traditional Middle Eastern spices. A festive meal that brings families together.',
            'category_id': arabic_category.id,
            'base_price': Decimal('12.00'),
            'prep_time_minutes': 60,
            'difficulty': 'hard',
            'image_url': 'https://example.com/images/lamb-kabsa.jpg'
        },
        {
            'name': 'Hummus with Falafel',
            'description': 'Creamy hummus served with crispy homemade falafel, fresh vegetables, and warm pita bread. A healthy and satisfying vegetarian option.',
            'category_id': arabic_category.id,
            'base_price': Decimal('6.75'),
            'prep_time_minutes': 30,
            'difficulty': 'easy',
            'image_url': 'https://example.com/images/hummus-falafel.jpg'
        },
        
        # Asian Cuisine
        {
            'name': 'Chicken Teriyaki',
            'description': 'Japanese-style glazed chicken with steamed vegetables and jasmine rice. Sweet and savory flavors that everyone will love.',
            'category_id': asian_category.id,
            'base_price': Decimal('9.00'),
            'prep_time_minutes': 30,
            'difficulty': 'easy',
            'image_url': 'https://example.com/images/chicken-teriyaki.jpg'
        },
        {
            'name': 'Thai Green Curry',
            'description': 'Spicy and creamy green curry with chicken, Thai basil, and coconut milk. Served with fragrant jasmine rice.',
            'category_id': asian_category.id,
            'base_price': Decimal('10.25'),
            'prep_time_minutes': 35,
            'difficulty': 'medium',
            'image_url': 'https://example.com/images/thai-green-curry.jpg'
        },
        {
            'name': 'Beef Stir Fry',
            'description': 'Quick and healthy stir-fried beef with mixed vegetables in a savory sauce. Perfect for busy weeknight dinners.',
            'category_id': asian_category.id,
            'base_price': Decimal('11.50'),
            'prep_time_minutes': 20,
            'difficulty': 'easy',
            'image_url': 'https://example.com/images/beef-stir-fry.jpg'
        },
        
        # Italian Cuisine
        {
            'name': 'Spaghetti Carbonara',
            'description': 'Classic Roman pasta dish with eggs, pancetta, parmesan cheese, and black pepper. Simple ingredients, extraordinary taste.',
            'category_id': italian_category.id,
            'base_price': Decimal('7.50'),
            'prep_time_minutes': 25,
            'difficulty': 'medium',
            'image_url': 'https://example.com/images/spaghetti-carbonara.jpg'
        },
        {
            'name': 'Margherita Pizza',
            'description': 'Classic Italian pizza with fresh mozzarella, tomatoes, and basil. Made with authentic Italian ingredients and traditional methods.',
            'category_id': italian_category.id,
            'base_price': Decimal('9.75'),
            'prep_time_minutes': 40,
            'difficulty': 'medium',
            'image_url': 'https://example.com/images/margherita-pizza.jpg'
        },
        {
            'name': 'Chicken Parmigiana',
            'description': 'Breaded chicken breast topped with marinara sauce and melted mozzarella cheese. Served with spaghetti pasta.',
            'category_id': italian_category.id,
            'base_price': Decimal('11.25'),
            'prep_time_minutes': 35,
            'difficulty': 'medium',
            'image_url': 'https://example.com/images/chicken-parmigiana.jpg'
        },
        
        # Healthy Options
        {
            'name': 'Grilled Salmon Bowl',
            'description': 'Fresh grilled salmon with quinoa, avocado, mixed greens, and lemon vinaigrette. Packed with omega-3s and nutrients.',
            'category_id': healthy_category.id,
            'base_price': Decimal('13.50'),
            'prep_time_minutes': 25,
            'difficulty': 'easy',
            'image_url': 'https://example.com/images/grilled-salmon-bowl.jpg'
        },
        {
            'name': 'Mediterranean Chickpea Salad',
            'description': 'Protein-rich chickpea salad with cucumbers, tomatoes, olives, and feta cheese. Light yet satisfying.',
            'category_id': healthy_category.id,
            'base_price': Decimal('8.25'),
            'prep_time_minutes': 15,
            'difficulty': 'easy',
            'image_url': 'https://example.com/images/mediterranean-chickpea-salad.jpg'
        },
        {
            'name': 'Quinoa Stuffed Bell Peppers',
            'description': 'Colorful bell peppers stuffed with quinoa, vegetables, and herbs. A complete vegetarian meal full of nutrients.',
            'category_id': healthy_category.id,
            'base_price': Decimal('9.50'),
            'prep_time_minutes': 45,
            'difficulty': 'medium',
            'image_url': 'https://example.com/images/quinoa-stuffed-peppers.jpg'
        }
    ]
    
    for recipe_data in recipes_data:
        # Check if recipe already exists
        existing_recipe = db.query(Recipe).filter(Recipe.name == recipe_data['name']).first()
        if not existing_recipe:
            recipe = Recipe(**recipe_data)
            db.add(recipe)
    
    db.commit()
    db.close()
    print("Recipes seeded successfully!")

def seed_test_user():
    """Create a test user for development"""
    db = SessionLocal()
    
    # Check if test user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == 'test@alosra.com').first()
    if not existing_user:
        test_user = UserModel(
            name='Ahmed Al-Mansoori',
            email='test@alosra.com',
            password_hash=hash_password('password123'),
            phone='+973-1234-5678',
            address='Building 123, Road 456, Manama, Bahrain'
        )
        db.add(test_user)
        db.commit()
        print("Test user created: test@alosra.com / password123")
    else:
        print("Test user already exists")
    
    db.close()

def seed_all():
    """Seed all initial data"""
    print("Starting database seeding...")
    seed_categories()
    seed_recipes()
    seed_test_user()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    # This allows you to run: python seed.py
    seed_all()