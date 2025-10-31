
# backend/app.py - Final Clean Code for MySQL/SQLAlchemy

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  
from flask_migrate import Migrate        
from datetime import datetime            
import os # Keep os for environment variable access

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__)

# --- MYSQL CONFIGURATION ---
# NOTE: Replace USER, PASSWORD, HOST, and DATABASE_NAME with your actual MySQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/piston_archive'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- DATABASE MODELS ---
class Car(db.Model):
    __tablename__ = 'cars'  # Make sure this matches your table name in phpMyAdmin
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    era = db.Column(db.String(50))
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))

    def __repr__(self):
        return f"<Car {self.name}>"

# 2. Review Model (Stores user-submitted reviews)
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# 3. User Model (Stores user sign-up data)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    interest = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}')"

# --- ROUTES ---

@app.route('/')
def home():
    cars = Car.query.all()

    # Convert SQLAlchemy objects into dictionaries
    car_list = [
        {
            'id': car.id,
            'name': car.name,
            'era': car.era,
            'category': car.category,
            'price': car.price,
            'description': car.description,
            'image_url': car.image_url
        }
        for car in cars
    ]

    return render_template('cars.html', cars=car_list)


@app.route('/submit_review', methods=['POST'])
def submit_review():
    """Handles the review form submission and saves it to the MySQL database."""
    try:
        # 1. Get data from the form
        user_name = request.form.get('reviewName')
        user_email = request.form.get('reviewEmail')
        rating = int(request.form.get('reviewRating'))
        text = request.form.get('reviewText')
        
        # 2. Create and commit the Review object
        new_review = Review(
            user_name=user_name, 
            user_email=user_email, 
            rating=rating, 
            text=text, 
            date_posted=datetime.utcnow()
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        return redirect(url_for('home'))
        
    except Exception as e:
        db.session.rollback() # Undo changes if an error occurs
        # Return an internal server error status if saving fails
        return f"Error saving review: {e}", 500

@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    """Handles the sign-up form submission and saves it to the MySQL database."""
    try:
        # 1. Get data from the form
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('signupEmail')
        interest = request.form.get('interests')

        # 2. Create and commit the User object
        new_user = User(
            first_name=first_name, 
            last_name=last_name,
            email=email, 
            interest=interest
        )

        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('home'))
        
    except Exception as e:
        db.session.rollback()
        # Return a bad request status if signup fails (e.g., email duplicate)
        return f"Error signing up (Email may already exist): {e}", 400

# --- API ROUTE (Optional - Example for fetching data) ---
@app.route('/api/cars', methods=['GET'])
def get_cars_json():
    """Returns all car data in JSON format."""
    # You would typically convert this to JSON, but for simplicity:
    return jsonify({"message": "API endpoint ready to serve data."}) 

if __name__ == '__main__':
    # This block must remain commented out for Gunicorn deployment.
    # app.run(debug=True)
    pass

# backend/seed_data.py (Partial update for clarity)

INITIAL_CARS = [
    # ... (Car 1) ...
    {
        "id": 4,
        "name": "1961 Jaguar E-Type",
        # FIX: Ensure this maps correctly to 'british-classics'
        "era": "British Classics", 
        # ... other fields ...
        "category": "british-classics" 
    },
    {
        "id": 5,
        "name": "1969 Chevrolet Camaro SS",
        # FIX: Ensure this maps correctly to 'muscle-car'
        "era": "Muscle Car", 
        # ... other fields ...
        "category": "muscle-car"
    },
    # ... (Ensure all 6 cars have a value that exactly matches one of the button slugs)
]