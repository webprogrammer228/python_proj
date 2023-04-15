from flask import Blueprint, jsonify, request, abort
from database import db
import base64
from datetime import datetime
import pytz

animal_location = Blueprint('animal_location', __name__)

@animal_location.route('/animals/<animalId>/locations', methods=['GET'])
def get_animal_locations(animalId):
    animalId = int(animalId)
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
      encoded_credentials = auth_header.split(' ')[1]
      credentials = base64.b64decode(encoded_credentials).decode('utf-8')
      email, password = credentials.split(':')

      user = db.accounts.find_one({'email': email, 'password': password})
      if user is None:
        abort(401, 'Invalid email or password')


    if animalId <= 0 or animalId is None:
      return jsonify({"message:": "Invalid animalId"}), 400
    startDateTime = request.args.get('startDateTime', None)
    endDateTime = request.args.get('endDateTime', None)

    if startDateTime:
        try:
            startDateTime = datetime.fromisoformat(startDateTime)
        except ValueError:
            abort(400, "Некорректный формат startDateTime. Ожидается формат ISO-8601.")

    if endDateTime:
        try:
            endDateTime = datetime.fromisoformat(endDateTime)
        except ValueError:
            abort(400, "Некорректный формат endDateTime. Ожидается формат ISO-8601.")

    animal = db.animals.find_one({'id': animalId})
    if not animal:
        abort(404, f"Животное с animalId {animalId} не найдено")


    visited_locations = animal.get('visitedLocations', [])

    response_list = []
    for loc in visited_locations:
        loc_point = db.locations.find_one({'id': int(loc.get('locationPointId', None))})
        if loc_point:
            location_id = loc.get('id', None)
            datetime_of_visit = loc.get('dateTimeOfVisitLocationPoint', None)
            response_list.append({
                'id': location_id,
                'dateTimeOfVisitLocationPoint': datetime_of_visit,
                'locationPointId': int(loc.get('locationPointId', None))
            })
    response_list = sorted(response_list, key=lambda x: x['dateTimeOfVisitLocationPoint'])
    return jsonify(response_list), 200   

@animal_location.route('/animals/<animalId>/locations/<pointId>', methods=['POST'])
def add_new_animal_location(animalId, pointId):
    animalId = int(animalId)
    pointId = int(pointId)
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        abort(401, 'Authorization header is missing')

    if not animalId or animalId <= 0 or not pointId or pointId <= 0:
        abort(400)

    if auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')

        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
            abort(401, 'Invalid email or password')

    animal = db.animals.find_one({'id': animalId})
    if animal is None:
        abort(404, f"Животное с animalId {animalId} не найдено")

    if animal.get('lifeStatus', '') == "DEAD":
        abort(400)

    location = db.locations.find_one({"id": pointId})
    if location is None:
        abort(404, f"Точка локации с pointId {pointId} не найдена")

    visited_location_ids = animal.get('visitedLocations', [])
    if pointId in visited_location_ids:
        abort(400, f"Животное уже посетило точку локации с id {pointId}")

    timezone = pytz.timezone('UTC')
    visited_locations_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(timezone)
    updated_date = visited_locations_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    new_location_id = db.animals.count_documents({'visitedLocations': {'$exists': True}}) + 1
    new_location = {
        "id": new_location_id,
        "locationPointId": pointId,
        "dateTimeOfVisitLocationPoint": updated_date
    }
    db.animals.update_one({'id': animalId}, {'$push': {'visitedLocations': pointId }})
      
    return jsonify(new_location), 201

@animal_location.route('/animals/<animalId>/locations', methods=['PUT'])
def update_animal_location(animalId):
    animalId = int(animalId)
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')

        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
            abort(401, 'Invalid email or password')

    if not auth_header:
      return jsonify({"message": "Can't delete not auth user"}), 401

    if animalId <= 0 or animalId is None:
      return jsonify({"message:": "Invalid animalId"}), 400
    
    data = request.get_json()
    if not data or 'visitedLocationPointId' not in data or 'locationPointId' not in data:
      abort(400)
    visited_location_point_id = data['visitedLocationPointId']
    location_point_id = data['locationPointId']

    if animalId is None or animalId <= 0 or visited_location_point_id is None or visited_location_point_id <= 0 or location_point_id is None or location_point_id <= 0:
        abort(400)

    animal = db.animals.find_one({'id': animalId})
    if not animal:
        abort(404, f"Животное с animalId {animalId} не найдено")

    if animal.get('lifeStatus', '') == "DEAD":
        abort(400)
    
    visited_locations = animal.get('visitedLocations')
    if visited_locations is None:
      return jsonify({"message:": "This animal haven't visited locations"}), 404
    if location_point_id in visited_locations:
      return jsonify({"message:": "This point is already used"}), 400 
    
    duplicatedValues = db.animals.find({'id': animalId}, {'visitedLocations': location_point_id})
    if duplicatedValues is not None:
      return jsonify({"message:": "This point is already have!"}), 400
    
    timezone = pytz.timezone('UTC')
    visited_locations_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(timezone)
    updated_date = visited_locations_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    new_location = {
        "id": db.animals.count_documents({}) + 1,
        "locationPointId": location_point_id,
        "dateTimeOfVisitLocationPoint": updated_date
    }
    db.animals.update_one({'id': animalId}, {'$push': {'visitedLocations': location_point_id}}) 
    
    return jsonify(new_location), 200

@animal_location.route('/animals/<animalId>/locations/<visitedPointId>', methods=['DELETE'])
def delete_animal_location(animalId, visitedPointId):
    animalId = int(animalId)
    visitedPointId = int(visitedPointId)
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

    if animalId <= 0 or animalId is None:
      return jsonify({"message:": "Invalid animalId"}), 400
    if visitedPointId <= 0 or visitedPointId is None:
      return jsonify({"message:": "Invalid visitedPointId"}), 400

    animal = db.animals.find_one({'id': animalId})
    if not animal:
        abort(404, f"Животное с animalId {animalId} не найдено")

    visited_locations = animal.get('visitedLocations', [])
    visited_location_ids = [loc.get('locationPointId') for loc in visited_locations]

    if visitedPointId not in visited_location_ids:
        abort(404, f"Объект с информацией о посещенной точке локации с visitedPointId {visitedPointId} не найден.")
    elif len(visited_locations) == 1:
        if visited_locations[0]['locationPointId'] == animal.get('chipLocation', ''):
            db.animals.update_one({'id': animalId}, {'$unset': {'visitedLocations': '', 'chipLocation': ''}})
            return '', 200
        else:
            db.animals.update_one({'id': animalId}, {'$unset': {'visitedLocations': ''}})
            return '', 200
    else:
        visited_locations = [loc for loc in visited_locations if loc.get('locationPointId') != visitedPointId]
        db.animals.update_one({'id': animalId}, {'$set': {'visitedLocations': visited_locations}})

    return jsonify({'message:': 'Successfully delete'}), 200