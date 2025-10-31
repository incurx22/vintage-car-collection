# backend/seed_data.py

import os
from app import app, db, Car, Review, User 
from datetime import datetime

# --- Final List of Six Cars to be inserted into the 'cars' table ---
INITIAL_CAR_DATA = [
    {
        "id": 1,
        "name": "Ferrari 488",
        "era": "Golden Age",
        "description": "The legendary James Bond tourer. Epitome of 1960s British luxury and engineering.",
        "year": 1964,
        "price": 1200000.00,
        "image_url": "images/db5.jpg",
        "category": "british-classics"
    },
    {
        "id": 2,
        "name": "Ford Mustang 1969",
        "era": "Fifties Fins",
        "description": "An iconic symbol of American design from the 1950s, recognizable by its huge tail fins.",
        "year": 1957,
        "price": 95000.00,
        "image_url": "images/belair.jpg",
        "category": "fifties-era"
    },
    {
        "id": 3,
        "name": "Lamborghini Aventador",
        "era": "Muscle Car",
        "description": "One of the most revered muscle cars, featuring high-performance V8 engine options.",
        "year": 1970,
        "price": 150000.00,
        "image_url": "images/challenger.jpg",
        "category": "muscle-car"
    }
    
]

def seed_database():
    """Inserts initial car data into the MySQL database."""
    with app.app_context():
        # WARNING: Use db.session.query(Car).delete() only if you are confident 
        # you want to wipe out all data and replace it.
        
        if Car.query.count() < 6: # Only seed if the database is incomplete
            # Cleanly delete all existing data before seeding the new list
            db.session.query(Car).delete() 
            db.session.commit()
            
            for data in INITIAL_CAR_DATA:
                car = Car(
                    id=data['id'],
                    name=data['name'],
                    year=data['year'],
                    price=data['price'],
                    era=data['era'],
                    description=data['description'],
                    image_url=data['image_url']
                )
                db.session.add(car)
            
            db.session.commit()
            print(f"Database successfully cleared and seeded with {len(INITIAL_CAR_DATA)} cars.")
        else:
            print("Database already contains the full collection.")

if __name__ == '__main__':
    seed_database()