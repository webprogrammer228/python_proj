from flask import Blueprint, jsonify, request, abort
from database import db
import base64
import random

animal_type = Blueprint('animal_type', __name__)

@animal_type.route('/animals/types/<typeId>', methods=['GET'])
def get_animal_type(typeId):
    typeId = int(typeId)  
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
      encoded_credentials = auth_header.split(' ')[1]
      credentials = base64.b64decode(encoded_credentials).decode('utf-8')
      email, password = credentials.split(':')
      user = db.accounts.find_one({'email': email, 'password': password})
      if user is None:
        abort(401, 'Invalid email or password')
       
    if typeId <= 0 or typeId is None:
      return jsonify({"message": "Invalid typeId"}), 400   
    animal_type = db.animals_types.find_one({'id': typeId})
    if not animal_type:
        abort(404, f"Тип животного с typeId {typeId} не найден")


    response = {
        "id": animal_type["id"],
        "type": animal_type["type"]
    }

    return jsonify(response), 200
  
@animal_type.route('/animals/types', methods=['POST'])
def create_new_animal_type():
    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return jsonify({"error": "Authorization header is missing or invalid"}), 401
    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')

    user = db.accounts.find_one({'email': email, 'password': password})
    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401

    animal_type = request.json.get('type')
    if not animal_type or not animal_type.strip():
        return jsonify({"error": "Animal type cannot be empty"}), 400
    
    existing_type = db.animals_types.find_one({'type': animal_type})
    if existing_type:
        return jsonify({"error": "Animal type already exists"}), 409
    
    while True:
        new_id = random.randint(1, 1000000)
        existing_type = db.animals_types.find_one({'id': new_id})
        if not existing_type:
            break
      
    result = db.animals_types.insert_one({'type': animal_type, 'id': new_id})
    if not result.acknowledged:
        return jsonify({"error": "Failed to add new animal type"}), 500

    new_animal_type = db.animals_types.find_one({'id': new_id})
    return jsonify({
        "id": new_id,
        "type": new_animal_type["type"]
    }), 201

@animal_type.route('/animals/types/<typeId>', methods=['PUT'])
def new_animal_type(typeId):
    typeId = int(typeId)
    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return abort(401, 'Authorization header is missing or invalid')

    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')
    
    if typeId <= 0 or typeId is None:
      return jsonify({"message": "invalid type id"}), 400

    animal_type = request.json.get('type')
    
    if animal_type is None:
      return jsonify({"error": "Animal type cannot be null"}), 400
    existing_type = db.animals_types.find_one({'type': animal_type})
    if existing_type:
        return jsonify({"error": "Animal type already exists"}), 409
      
    user = db.accounts.find_one({'email': email, 'password': password})
    if user is None:
        return abort(401, 'Invalid email or password')


    if not animal_type or not animal_type.strip():
        return jsonify({"error": "Animal type cannot be empty"}), 400

    existing_type = db.animals_types.find_one({"id": typeId})
    if existing_type is None:
        return jsonify({"error": f"Animal type with id {typeId} not found"}), 404

    if existing_type['type'] != animal_type:
        type_exists = db.animals_types.find_one({"type": animal_type})
        if type_exists:
            return jsonify({"error": f"Animal type {animal_type} already exists"}), 409

    db.animals_types.update_one({"id": typeId}, {"$set": {"type": animal_type}})

    return jsonify({
        "id": typeId,
        "type": animal_type
    }), 200  


@animal_type.route('/animals/types/<typeId>', methods=['DELETE'])
def remove_animal_type(typeId):
    typeId = int(typeId)
    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return abort(401, 'Authorization header is missing or invalid')

    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')
    
    if typeId <= 0 or typeId is None:
      return jsonify({"message": "Invalid id"}), 400

    user = db.accounts.find_one({'email': email, 'password': password})
    if user is None:
        return abort(401, 'Invalid email or password')

    animals_with_type = list(db.animals_types.find({"type_id": typeId}))
    if len(animals_with_type) > 0:
        return jsonify({"error": "Cannot delete animal type because there are animals with this type"}), 400

    result = db.animals_types.delete_one({"id": typeId})
    if result.deleted_count == 0:
        return jsonify({"error": f"Animal type with id {typeId} not found"}), 404 

    return '', 200