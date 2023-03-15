from flask import Blueprint, jsonify, request, abort
from database import db
from datetime import datetime
import base64
import pytz

animals = Blueprint('animals', __name__)

@animals.route('/animals/<animalId>', methods=['GET'])
def get_animal_info(animalId):
    animalId = int(animalId)
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')

        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
            return jsonify({'message': 'Invalid email or password'}), 401
  
    if animalId is None or animalId <= 0:
        return jsonify({'message': 'Invalid id'}), 400
    elif db.animals.find_one({'id': animalId}) is None:
        return jsonify({'message': 'Animal not found'}), 404

    animal = db.animals.find_one({'id': animalId})
    visited_locations = animal.get('visitedLocations', [])
    locations = []
    if visited_locations:
      for loc in visited_locations:
        locations.append(loc)
    else:
      locations = []
    if animal:
        return jsonify({
            "id": animal.get('id'), 
            "animalTypes": animal.get('animalTypes'),
            "weight": animal.get('weight'),
            "length": animal.get('length'),
            "height": animal.get('height'),
            "gender": animal.get('gender'),
            "lifeStatus": animal.get('lifeStatus'),
            "chippingDateTime": animal.get('chippingDateTime') if animal.get('chippingDateTime') else None,
            "chipperId": animal.get('chipperId'),
            "chippingLocationId": animal.get('chippingLocationId'),
            "visitedLocations": locations,
            "deathDateTime": animal.get('deathDateTime') if animal.get('deathDateTime') else None,
        }), 200
    else:
        return jsonify({'message': 'Animal not found'}), 404
      
@animals.route('/animals/search', methods=['GET'])
def find_animal_info():
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')

        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
            abort(401, 'Invalid email or password')

    animal_type = request.args.get('animal_type', default=None)
    min_weight = request.args.get('min_weight', default=None, type=float)
    max_weight = request.args.get('max_weight', default=None, type=float)
    min_length = request.args.get('min_length', default=None, type=float)
    max_length = request.args.get('max_length', default=None, type=float)
    min_height = request.args.get('min_height', default=None, type=float)
    max_height = request.args.get('max_height', default=None, type=float)
    from_index = request.args.get('from', default=0, type=int)
    start_date_time = request.args.get('startDateTime', default=None)
    end_data_time = request.args.get('endDateTime', default=None)
    size = request.args.get('size', default=10, type=int)
    gender = request.args.get('gender', default=None)
    life_status = request.args.get('lifeStatus', default=None)
    chipper_id = request.args.get('chipperId', default=None)
    chipping_location_id = request.args.get('chippingLocationId', default=None)

    query = {}

    if from_index < 0 or size <= 0:
        return jsonify({'message': 'Invalid parameters'}), 400
    if start_date_time is not None:
      if start_date_time == 'null':
        start_date_time = None
      else: query['start_date_time'] = start_date_time
    if chipper_id is not None:
      if (chipper_id == 'null'):
        chipper_id = None
      else: query['chipperId'] = int(chipper_id)
    if chipping_location_id is not None:
      if chipping_location_id == 'null':
        chipping_location_id = None
      else: query['chippingLocationId'] = int(chipping_location_id)
    if life_status is not None:
      if life_status == 'null':
        life_status = None
      else: query['lifeStatus'] = life_status
    if end_data_time is not None:
      if end_data_time == 'null':
        end_data_time = None
      else: query['endDataTime'] = end_data_time
    if gender is not None:
      if gender == 'null':
        gender = None
      else: query['gender'] = gender       
        
    if animal_type:
      query['animalTypes'] = animal_type

    if min_weight is not None and max_weight is not None:
        query['weight'] = {'$gte': min_weight, '$lte': max_weight}
    elif min_weight is not None:
        query['weight'] = {'$gte': min_weight}
    elif max_weight is not None:
        query['weight'] = {'$lte': max_weight}

    if min_length is not None and max_length is not None:
        query['length'] = {'$gte': min_length, '$lte': max_length}
    elif min_length is not None:
        query['length'] = {'$gte': min_length}
    elif max_length is not None:
        query['length'] = {'$lte': max_length}

    if min_height is not None and max_height is not None:
        query['height'] = {'$gte': min_height, '$lte': max_height}
    elif min_height is not None:
        query['height'] = {'$gte': min_height}
    elif max_height is not None:
        query['height'] = {'$lte': max_height}
  
    if not any(query):
        animals = db.animals.find()
    else:
        animals = db.animals.find(query)

    animals = animals.skip(from_index).limit(size)
    visited_locations = request.args.get('visitedLocations', [])
    if visited_locations:
      visited_location_ids = list(map(lambda loc: loc['id'], visited_locations))
    else:
      visited_location_ids = []
    response = []
    for animal in animals:
      animal_dict = {
          "id": animal.get('id'),
          "animalTypes": animal.get('animalTypes'),
          "weight": animal.get('weight'),
          "length": animal.get('length'),
          "height": animal.get('height'),
          "gender": animal.get('gender'),
          "lifeStatus": animal.get('lifeStatus'),
          "chippingDateTime": animal.get('chippingDateTime') if animal.get('chippingDateTime') else None,
          "chipperId": animal.get('chipperId'),
          "chippingLocationId": animal.get('chippingLocationId'),
          "visitedLocations": visited_location_ids,
          "deathDateTime": animal.get('deathDateTime') if animal.get('deathDateTime') else None
      }
                   
      if 'visitedLocations' not in animal_dict:
          animal_dict['visitedLocations'] = []
          
      if animal_dict['visitedLocations'] is None:
          del animal_dict['visitedLocations']
      response.append(animal_dict)
    
    if response:
        return jsonify(response), 200 
    else:
        return jsonify({'message': 'No animals found'}), 400 
                                                               
@animals.route('/animals', methods=['POST'])
def create_animal():
    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return abort(401, 'Authorization header is missing or invalid')

    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')

    user = db.accounts.find_one({'email': email, 'password': password})
    if user is None:
        return abort(401, 'Invalid email or password')

    data = request.get_json()
    if data is None:
        return abort(400, 'Invalid JSON data')

    animalTypes = data.get('animalTypes')
    if not animalTypes or not isinstance(animalTypes, list):
        return abort(400, 'Animal type is required and should be a list')

    for animalType in animalTypes:
        if not animalType or not isinstance(animalType, int):
            return abort(400, 'Invalid animal type')
        if animalType < 0:
            return abort(400, 'Invalid animal type')

    weight = data.get('weight')
    if not weight or weight <= 0:
        return abort(400, 'Weight is required and should be a positive number')

    length = data.get('length')
    if not length or length <= 0:
        return abort(400, 'Length is required and should be a positive number')

    height = data.get('height')
    if not height or height <= 0:
        return abort(400, 'Height is required and should be a positive number')

    gender = data.get('gender')
    if gender not in ['MALE', 'FEMALE', 'OTHER']:
        return abort(400, 'Gender should be MALE, FEMALE or OTHER')

    chipperId = data.get('chipperId')

    if chipperId is None or chipperId < 0:
        return abort(400, 'chipper not found')
    if not chipperId or not isinstance(chipperId, int):
        return abort(400, 'Chipper ID is required and should be an integer')

    chipper = db.accounts.find_one({'id': chipperId})
    if chipper is None:
        return abort(404, f"Chipper with ID '{chipperId}' not found")

    chippingLocationId = data.get('chippingLocationId')
    if chippingLocationId is not None and chippingLocationId < 0:
      return abort(400, 'ChippingLocationId is wrong')
    if chippingLocationId is None:
        return abort(400, 'ChippingLocationId wrong')
    if not chippingLocationId or not isinstance(chippingLocationId, int):
        return abort(400, 'Chipping location ID is required and should be an integer')

    chippingLocation = db.locations.find_one({'id': chippingLocationId})
    if chippingLocation is None:
        return abort(404, f"Chipping location with ID '{chippingLocationId}' not found")

    visitedLocations = data.get('visitedLocations')
    if visitedLocations is None:
        visitedLocations = []

    for locationId in visitedLocations:
        location = db.locations.find_one({'id': locationId})
        if location is None:
            return abort(404, f"Location with ID '{locationId}' not found")
          
    timezone = pytz.timezone('UTC')
    date = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(timezone)
    updated_date = date.strftime("%Y-%m-%dT%H:%M:%S.%f%z")      
    new_id = db.animals.count_documents({}) + 1
    animal = {
    'id': new_id,
    'animalTypes': animalTypes,
    'weight': weight,
    'length': length,
    'height': height,
    'gender': gender,
    'chipperId': chipperId,
    'chippingLocationId': chippingLocationId,
    'visitedLocations': visitedLocations,
    'lifeStatus': 'ALIVE',
    'chippingDateTime': updated_date,
    'deathDateTime': None
    }
    db.animals.insert_one(animal)
    new_animal = db.animals.find_one({"id": new_id}, {'_id': 0})
    return jsonify(new_animal), 201

@animals.route('/animals/<animalId>', methods=['PUT'])
def update_animal(animalId):
    animalId = int(animalId)
    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return abort(401, 'Authorization header is missing or invalid')

    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')

    user = db.accounts.find_one({'email': email, 'password': password})
    if user is None:
        return abort(401, 'Invalid email or password')

    if animalId <= 0 or animalId is None:
      return jsonify({"error": "Invalid id"}), 400
    animal = db.animals.find_one({'id': animalId})
    if not animal:
        return jsonify({"error": "Animal not found"}), 404

    chipperId_param = request.json.get('chipperId')
    chipper = db.accounts.find_one({'id': chipperId_param})
    if chipper is None:
      return jsonify({"error": "Invalid chipper"}), 400
    if not chipper:
        return jsonify({"error": "Invalid chipperId"}), 400

    chippingLocationId_param = request.json.get('chippingLocationId')
    if not chippingLocationId_param:
        return jsonify({"error": "Invalid chippingLocationId"}), 404

    weight = request.json.get('weight')
    if weight is None or weight <= 0:
        return jsonify({"error": "Invalid weight"}), 400
    length = request.json.get('length')
    if length is None or length <= 0:
        return jsonify({"error": "Invalid length"}), 400
    height = request.json.get('height')
    if height is None or height <= 0:
        return jsonify({"error": "Invalid height"}), 400
    gender = request.json.get('gender')
    if gender not in ['MALE', 'FEMALE', 'OTHER']:
        return jsonify({"error": "Invalid gender"}), 400
    
    lifeStatus = request.json.get('lifeStatus')
    if lifeStatus not in ['ALIVE', 'DEAD']:
        return jsonify({"error": "Invalid lifeStatus"}), 400
    
    animal = db.animals.find_one({'id': animalId})
    if not animal:
        return jsonify({"error": "Animal not found"}), 404

    weight = request.json.get('weight')
    if weight is None or weight <= 0:
        return jsonify({"error": "Invalid weight"}), 400
    length = request.json.get('length')
    if length is None or length <= 0:
        return jsonify({"error": "Invalid length"}), 400
    height = request.json.get('height')
    if height is None or height <= 0:
        return jsonify({"error": "Invalid height"}), 400
    
    animal['weight'] = weight
    animal['length'] = length
    animal['height'] = height
    animal['gender'] = gender
    
    timezone = pytz.timezone('UTC')
    date = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(timezone)
    updated_date = date.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    
    timezone = pytz.timezone('UTC')
    if lifeStatus == 'DEAD':
        animal['lifeStatus'] = 'DEAD'
        animal['deathDateTime'] = updated_date
    else:
        animal['lifeStatus'] = 'ALIVE'
        animal['deathDateTime'] = None
    
    animal['chippingLocationId'] = chippingLocationId_param
    animal['chippingDateTime'] = updated_date
    animal['chipperId'] = chipperId_param
    
    if chippingLocationId_param not in animal['visitedLocations']:
        animal['visitedLocations'].append(chippingLocationId_param)
    
    db.animals.update_one({'id': animalId}, {'$set': animal})
    
    return jsonify({
        "id": animal['id'],
        "animalTypes": animal['animalTypes'],
        "weight": animal['weight'],
        "length": animal['length'],
        "height": animal['height'],
        "gender": animal['gender'],
        "lifeStatus": animal['lifeStatus'],
        "chippingDateTime": animal['chippingDateTime'],
        "chipperId": animal['chipperId'],
        "chippingLocationId": animal['chippingLocationId'],
        "visitedLocations": animal['visitedLocations'],
        "deathDateTime": animal['deathDateTime']
    }), 200
    
@animals.route('/animals/<animalId>', methods=['DELETE'])
def delete_animal(animalId):
    animalId = int(animalId)
    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return abort(401, 'Authorization header is missing or invalid')

    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')
    
    if animalId <= 0 or animalId is None:
      return jsonify({"message": "Invalid id"}), 400

    user = db.accounts.find_one({'email': email, 'password': password})
    if user is None:
        return abort(401, 'Invalid email or password')

    animal = db.animals.find_one({"id": animalId})
    if not animal:
        return jsonify({"error": "Animal not found"}), 404
    if len(animal.get("locations", [])) > 1:
        return jsonify({"error": "Animal has visited multiple locations"}), 400
    if len(animal.get("animal_types", [])) > 1:
        return jsonify({"error": "Animal has linked to another animals"}), 400  
    db.animals.delete_one({"id": animalId})
    return jsonify({"message:": "animal deleted"}), 200
  
@animals.route('/animals/<animalId>/types/<typeId>', methods=['POST'])
def create_animal_type(animalId, typeId):
    animalId = int(animalId)
    typeId = int(typeId)
    animal = db.animals.find_one({"id": animalId})
    animal_type = db.animals_types.find_one({"id": typeId})

    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return abort(401, 'Authorization header is missing or invalid')
    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')
    
    if animalId <= 0 or animalId is None:
      return jsonify({'message': 'Invalid animalId'}), 400
    if typeId <= 0 or typeId is None:
      return jsonify({'message': 'Invalid typeId'}), 400

    user = db.accounts.find_one({'email': email, 'password': password})
    if user is None:
        return abort(401, 'Invalid email or password')

    if not animal:
        return jsonify({"error": f"Animal with id {animalId} not found"}), 404

    if not animal_type:
        return jsonify({"error": f"Animal type with id {typeId} not found"}), 404

    if animal_type in animal['animals_types']:
        return jsonify({"error": f"Animal with id {animalId} already has type with id {typeId}"}), 409

    db.animals.update_one({"id": animalId}, {"$push": {"animals_types": {"id": animal_type['id']}}})

    return jsonify({
        "id": animal['id'],
        "animalTypes": [t['id'] for t in animal['animals_types']],
        "weight": animal['weight'],
        "length": animal['length'],
        "height": animal['height'],
        "gender": animal['gender'],
        "lifeStatus": animal['lifeStatus'],
        "chippingDateTime": animal['chippingDateTime'],
        "chipperId": animal['chipperId'],
        "chippingLocationId": animal['chippingLocationId'],
        "visitedLocations": [vl['id'] for vl in animal['visitedLocations']],
        "deathDateTime": animal['deathDateTime']
    }), 201


@animals.route('/animals/<animalId>/types', methods=['PUT'])
def update_animal_type(animalId):
    animalId = int(animalId)
    req_data = request.get_json()
    oldTypeId = req_data.get('oldTypeId')
    newTypeId = req_data.get('newTypeId')

    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return abort(401, 'Authorization header is missing or invalid')

    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')

    if animalId <= 0 or animalId is None:
      return jsonify({"error:": "Invalid animalid"}), 400

    user = db.accounts.find_one({'email': email, 'password': password})
    if user is None:
        return abort(401, 'Invalid email or password')
    if not oldTypeId or oldTypeId <= 0:
        return jsonify({"error": "oldTypeId must be a positive integer"}), 400

    if not newTypeId or newTypeId <= 0:
        return jsonify({"error": "newTypeId must be a positive integer"}), 400

    animal = db.animals.find_one({'id': animalId})
    if not animal:
        return jsonify({"error": f"Animal with id {animalId} not found"}), 404

    if newTypeId not in animal['animalTypes']:
        return jsonify({"error": f"Animal with id {animalId} doesn't have type with id {newTypeId}"}), 404

    if oldTypeId not in animal['animalTypes']:
        return jsonify({"error": f"Animal with id {animalId} doesn't have type with id {oldTypeId}"}), 404

    if oldTypeId in animal['animalTypes']:
        return jsonify({"error": f"Animal with id {animalId} already has type with id {oldTypeId}"}), 409

    if newTypeId in animal['animalTypes']:
        return jsonify({"error": f"Animal with id {animalId} already has type with id {newTypeId}"}), 409

    db.animals_types.update_one({'id': animalId}, {'$addToSet': {'animalTypes': newTypeId}, '$pull': {'animalTypes': oldTypeId}})

    return jsonify({
        "id": animal['id'],
        "animalTypes": [t['id'] for t in animal['animalTypes']],
        "weight": animal['weight'],
        "length": animal['length'],
        "height": animal['height'],
        "gender": animal['gender'],
        "lifeStatus": animal['lifeStatus'],
        "chippingDateTime": animal['chippingDateTime'],
        "chipperId": animal['chipperId'],
        "chippingLocationId": animal['chippingLocationId'],
        "visitedLocations": [vl['id'] for vl in animal['visitedLocations']],
        "deathDateTime": animal['deathDateTime']
    }), 200    

@animals.route('/animals/<animalId>/types/<typeId>', methods=['DELETE'])
def delete_animal_type(animalId, typeId):
    animalId = int(animalId)
    typeId = int(typeId)
    animal = db.animals.find_one({'id': animalId})
    animal_type = db.animals_types.find_one({'id': typeId})

    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return abort(401, 'Authorization header is missing or invalid')

    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')

    if animalId <= 0 or animalId is None:
      return jsonify({"message:": "Invalid animalId"}), 400
    if typeId <= 0 or typeId is None:
      return jsonify({"message:": "Invalid animalId"}), 400
    user = db.accounts.find_one({'email': email, 'password': password})
    if user is None:
        return abort(401, 'Invalid email or password')

    if not animal:
        return jsonify({"error": f"Animal with id {animalId} not found"}), 404

    if not animal_type:
        return jsonify({"error": f"Animal type with id {typeId} not found"}), 400

    if typeId not in animal['animalTypes']:
        return jsonify({"error": f"Animal with id {animalId} does not have type with id {typeId}"}), 400

    animal_types_list = [t['id'] for t in db.animals_types.find()]
    if typeId not in animal_types_list:
        return jsonify({"error": f"Invalid typeId: {typeId}"}), 400

    animal['animalTypes'] = list(filter(lambda x: x != typeId, animal['animalTypes']))
    db.animals.update_one({"id": animalId}, {"$set": {"animalTypes": animal['animalTypes']}})

    return jsonify({
        "id": animal['id'],
        "animalTypes": animal['animalTypes'],
        "weight": animal['weight'],
        "length": animal['length'],
        "height": animal['height'],
        "gender": animal['gender'],
        "lifeStatus": animal['lifeStatus'],
        "chippingDateTime": animal['chippingDateTime'],
        "chipperId": animal['chipperId'],
        "chippingLocationId": animal['chippingLocationId'],
        "visitedLocations": [vl['id'] for vl in animal['visitedLocations']],
        "deathDateTime": animal['deathDateTime']
    }), 200   