from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
import pymongo
import os
from math import ceil

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# MongoDB connection
MONGODB_URI = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGODB_URI)
db = client['parking_system']
vehicles = db['vehicles']
categories = db['categories']  # New collection for vehicle categories and prices

# Admin password
ADMIN_PASSWORD = "1234"

# Default categories and prices (per hour)
DEFAULT_CATEGORIES = [
    {"name": "bike", "base_price": 10},
    {"name": "car", "base_price": 20},
    {"name": "bus", "base_price": 40},
    {"name": "truck", "base_price": 50},
]

# Ensure categories exist in DB
for cat in DEFAULT_CATEGORIES:
    if not categories.find_one({"name": cat["name"]}):
        categories.insert_one(cat)

@app.route('/')
def index():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    if 'authenticated' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    parked_vehicles = list(vehicles.find({"exit_time": None}))
    for vehicle in parked_vehicles:
        vehicle['_id'] = str(vehicle['_id'])
        vehicle['entry_time'] = vehicle['entry_time'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(parked_vehicles)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    if 'authenticated' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    cats = list(categories.find())
    for cat in cats:
        cat['_id'] = str(cat['_id'])
    return jsonify(cats)

@app.route('/api/categories', methods=['POST'])
def update_category_price():
    if 'authenticated' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    name = data.get('name')
    base_price = data.get('base_price')
    if not name or base_price is None:
        return jsonify({"error": "Missing name or base_price"}), 400
    result = categories.update_one({"name": name}, {"$set": {"base_price": base_price}})
    if result.matched_count == 0:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"message": "Base price updated"})

@app.route('/api/vehicles', methods=['POST'])
def add_vehicle():
    if 'authenticated' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    vehicle_no = request.json.get('vehicle_no').upper()
    category = request.json.get('category', '').lower()
    
    # Validate category
    cat = categories.find_one({"name": category})
    if not cat:
        return jsonify({"error": "Invalid category"}), 400
    
    # Check if vehicle already exists
    existing_vehicle = vehicles.find_one({
        "vehicle_no": vehicle_no,
        "exit_time": None
    })
    
    if existing_vehicle:
        return jsonify({"error": "Vehicle already parked"}), 400
    
    vehicle_data = {
        "vehicle_no": vehicle_no,
        "category": category,
        "entry_time": datetime.now(),
        "exit_time": None
    }
    
    vehicles.insert_one(vehicle_data)
    return jsonify({"message": "Vehicle added successfully"})

@app.route('/api/vehicles/<vehicle_no>/exit', methods=['POST'])
def record_exit(vehicle_no):
    if 'authenticated' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    vehicle = vehicles.find_one({
        "vehicle_no": vehicle_no.upper(),
        "exit_time": None
    })
    
    if not vehicle:
        return jsonify({"error": "Vehicle not found or already exited"}), 404
    
    exit_time = datetime.now()
    duration = exit_time - vehicle['entry_time']
    hours = duration.total_seconds() / 3600
    rounded_hours = max(1, int(ceil(hours)))
    
    # Get base price for category
    cat = categories.find_one({"name": vehicle.get('category', 'car')})
    base_price = cat['base_price'] if cat else 20
    total_price = base_price * rounded_hours
    
    vehicles.update_one(
        {"_id": vehicle['_id']},
        {"$set": {"exit_time": exit_time}}
    )
    
    return jsonify({
        "message": "Exit recorded successfully",
        "duration": f"{hours:.2f} hours (charged as {rounded_hours} hour{'s' if rounded_hours > 1 else ''})",
        "category": vehicle.get('category', 'car'),
        "base_price": base_price,
        "total_price": f"{total_price:.2f}",
        "entry_time": vehicle['entry_time'].strftime("%Y-%m-%d %H:%M:%S"),
        "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/manage-prices')
def manage_prices():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    return render_template('manage-prices.html')

if __name__ == '__main__':
    app.run(debug=True) 