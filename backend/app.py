from flask import Flask, render_template, jsonify
# flask_cors is no longer strictly needed but kept if you want to reuse the /api route
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 

# Vintage Car Data
CARS_DATA = [
    {
        "id": 1,
        "name": "1964 Aston Martin DB5",
        "era": "Golden Age",
        "description": "Famous for its role in James Bond films, the DB5 is the epitome of 1960s British luxury sports touring.",
        "year": 1964,
        "price": 1200000,
        "image_url": "db5.jpg"
    },
    {
        "id": 2,
        "name": "1957 Chevrolet Bel Air",
        "era": "Fifties Fins",
        "description": "An iconic symbol of American automotive design and culture from the 1950s, recognizable by its huge tail fins.",
        "year": 1957,
        "price": 95000,
        "image_url": "belair.jpg"
    },
    {
        "id": 3,
        "name": "1970 Dodge Challenger R/T",
        "era": "Muscle Car",
        "description": "One of the most revered muscle cars. The R/T package featured the high-performance V8 engine options.",
        "year": 1970,
        "price": 150000,
        "image_url": "challenger.jpg"
    }
]

# 1. Main Route - Renders the Dynamic HTML Page (The New Frontend)
@app.route('/', methods=['GET'])
def home():
    """Renders the HTML template and passes the car data to it."""
    # Flask uses Jinja2 to render cars.html dynamically
    # The 'cars' variable in the HTML will be the CARS_DATA list
    return render_template('cars.html', cars=CARS_DATA)

# 2. API Route (Kept for consistency, but not used by the new frontend)
@app.route('/api/cars', methods=['GET'])
def get_cars():
    return jsonify(CARS_DATA)

if __name__ == '__main__':
    # Running on default Flask port 5000
    app.run(debug=True)