from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fleet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Vehicle model
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False, unique=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'license_plate': self.license_plate,
            'brand': self.brand,
            'model': self.model,
            'year': self.year
        }

# Init DB
with app.app_context():
    db.create_all()

# Add vehicle
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    new_vehicle = Vehicle(
        license_plate=data['license_plate'],
        brand=data.get('brand'),
        model=data.get('model'),
        year=data.get('year')
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(new_vehicle.to_dict()), 201

# List vehicles
@app.route('/vehicles', methods=['GET'])
def list_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([v.to_dict() for v in vehicles])

@app.route('/vehicles/<id>', methods=['GET'])
def vehicle(id):
    vehicle = Vehicle.query.get(id)
    if vehicle:
        return jsonify(vehicle.to_dict())
    else:
        return jsonify({'error': 'Vehicle not found'}), 404

# Update vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    data = request.get_json()
    vehicle.license_plate = data.get('license_plate', vehicle.license_plate)
    vehicle.brand = data.get('brand', vehicle.brand)
    vehicle.model = data.get('model', vehicle.model)
    vehicle.year = data.get('year', vehicle.year)
    db.session.commit()
    return jsonify(vehicle.to_dict())

#  Delete vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)