from flask import Blueprint, jsonify, request, abort
from database import db
import base64

locations = Blueprint('locations', __name__)
    
@locations.route('/locations/<pointId>', methods=['GET'])
def get_location(pointId):
    pointId = int(pointId)
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')

        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
            abort(401, 'Invalid email or password')

    if not pointId or pointId <= 0:
      return jsonify({"message": "Invalid id"}), 400

    location = db.locations.find_one({'id': pointId})
    if not location:
        abort(404, f"Точка локации с pointId {pointId} не найдена")

    response = {
        "id": location.get('id', None),
        "latitude": location.get('latitude', None),
        "longitude": location.get('longitude', None)
    }

    return jsonify(response), 200
    
@locations.route('/locations', methods=['POST'])
def create_location():
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
      encoded_credentials = auth_header.split(' ')[1]
      credentials = base64.b64decode(encoded_credentials).decode('utf-8')
      email, password = credentials.split(':')

      user = db.accounts.find_one({'email': email, 'password': password})
      if user is None:
        abort(401, 'Invalid email or password')
    
    if not auth_header:
      return jsonify({"message": 'Not auth account'}), 401    
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')

    if latitude is None or latitude < -90 or latitude > 90 or \
        longitude is None or longitude < -180 or longitude > 180:
        return jsonify({'error': 'Invalid latitude or longitude'}), 400
      
    if db.locations.find_one({'latitude': latitude, 'longitude': longitude}):
        return jsonify({'error': 'Location with such latitude and longitude already exists'}), 409

    new_id = db.locations.count_documents({}) + 1
    location = {
        'id': new_id,
        'latitude': latitude,
        'longitude': longitude
    }
    db.locations.insert_one(location)
    
    result = {
        'id': new_id,
        'latitude': latitude,
        'longitude': longitude
    }
    return jsonify(result), 201

@locations.route('/locations/<pointId>', methods=['PUT'])
def update_location(pointId):
    pointId = int(pointId)
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')

        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
          abort(401, 'Invalid email or password')

    if not auth_header:
      return jsonify({"error:": "Not auth user"}), 401
    
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')

    if pointId <= 0 or pointId is None:
      return jsonify({'error' : 'Invalid pointId'}), 400 

    if latitude is None or latitude < -90 or latitude > 90 or \
            longitude is None or longitude < -180 or longitude > 180:
        return jsonify({'error': 'Invalid coordinates'}), 400

    location = db.locations.find_one({'id': pointId})

    if location is None:
        return jsonify({'error': 'Location not found'}), 404

    existing_location = db.locations.find_one({'latitude': latitude, 'longitude': longitude})
    if existing_location is not None and existing_location['id'] != pointId:
        return jsonify({'error': 'Location with these coordinates already exists'}), 409

    db.locations.update_one({'id': pointId}, {'$set': {'latitude': latitude, 'longitude': longitude}})

    updated_location = db.locations.find_one({'id': pointId}, {'_id': 0})
    return jsonify(updated_location), 200

@locations.route('/locations/<pointId>', methods=['DELETE'])
def delete_location(pointId):
    pointId = int(pointId)
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')

        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
            abort(401, 'Invalid email or password')

    if not auth_header:
      return jsonify({"message": "Unauthorized account"}), 401
    location = db.locations.find_one({'id': pointId})

    if pointId <= 0 or pointId is None:
      return jsonify({'error' : 'Invaid pointId'}), 400 
    if location is None:
        return jsonify({'error': 'Location not found'}), 404

    if db.animals.count_documents({'locationId': pointId}) > 0:
        return jsonify({'error': 'Location is associated with an animal'}), 400

    db.locations.delete_one({'id': pointId})

    return jsonify({}), 200