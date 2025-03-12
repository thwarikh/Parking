from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Parking Area Model
class ParkingArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    passcode = db.Column(db.String(10), nullable=False)  # For gatekeepers only
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

# Create Database
with app.app_context():
    db.create_all()

# Get all parking areas
@app.route('/parking', methods=['GET'])
def get_parking_areas():
    areas = ParkingArea.query.all()
    return jsonify([{
        'id': area.id, 'name': area.name, 
        'capacity': area.capacity, 'available_slots': area.available_slots,
        'latitude': area.latitude, 'longitude': area.longitude
    }])

# Gatekeeper updates vehicle entry/exit
@app.route('/update_parking', methods=['POST'])
def update_parking():
    data = request.json
    area = ParkingArea.query.get(data['id'])

    if area and data['passcode'] == area.passcode:
        area.available_slots = data['available_slots']
        db.session.commit()
        return jsonify({'message': 'Updated successfully'}), 200
    return jsonify({'message': 'Unauthorized'}), 403

if __name__ == '__main__':
    app.run(debug=True)
