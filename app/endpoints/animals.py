from flask import Blueprint, jsonify, request, abort
from database import db
from datetime import datetime

animals = Blueprint('animals', __name__)

@animals.route('/animals/<int:animalId>', methods=['GET'])
def get_animal(animalId):
    auth = request.authorization
    if not auth or not (auth.username == 'admin' and auth.password == 'password'):
        abort(401)

    if not animalId or animalId <= 0:
        abort(400)

    animal = db.animals.find_one({'id': animalId})
    if not animal:
        abort(404, f"Животное с animalId {animalId} не найдено")

    response = {
        "id": animal.id,
        "animalTypes": animal.animalTypes,
        "weight": animal.weight,
        "length": animal.length,
        "height": animal.height,
        "gender": animal.gender,
        "lifeStatus": animal.lifeStatus,
        "chippingDateTime": animal.chippingDateTime.isoformat(),
        "chipperId": animal.chipperId,
        "chippingLocationId": animal.chippingLocationId,
        "visitedLocations": animal.visitedLocations,
        "deathDateTime": animal.deathDateTime.isoformat() if animal.deathDateTime else None
    }

    return jsonify(response), 200

@animals.route('/animals/search', methods=['GET'])
def search_animals():
    auth = request.authorization
    if not auth or not (auth.username == 'admin' and auth.password == 'password'):
        abort(401)

    animal_type = request.args.get('animal_type', default=None)
    min_weight = request.args.get('min_weight', default=None, type=float)
    max_weight = request.args.get('max_weight', default=None, type=float)
    min_length = request.args.get('min_length', default=None, type=float)
    max_length = request.args.get('max_length', default=None, type=float)
    min_height = request.args.get('min_height', default=None, type=float)
    max_height = request.args.get('max_height', default=None, type=float)
    gender = request.args.get('gender', default=None)
    life_status = request.args.get('life_status', default=None)
    chipper_id = request.args.get('chipper_id', default=None)
    chipping_location_id = request.args.get('chipping_location_id', default=None)
    
    query = {}
    
    if animal_type:
        query['animalTypes'] = animal_type
    
    if min_weight and max_weight:
        query['weight'] = {'$gte': min_weight, '$lte': max_weight}
    elif min_weight:
        query['weight'] = {'$gte': min_weight}
    elif max_weight:
        query['weight'] = {'$lte': max_weight}
        
    if min_length and max_length:
        query['length'] = {'$gte': min_length, '$lte': max_length}
    elif min_length:
        query['length'] = {'$gte': min_length}
    elif max_length:
        query['length'] = {'$lte': max_length}
        
    if min_height and max_height:
        query['height'] = {'$gte': min_height, '$lte': max_height}
    elif min_height:
        query['height'] = {'$gte': min_height}
    elif max_height:
        query['height'] = {'$lte': max_height}
        
    if gender:
        query['gender'] = gender
        
    if life_status:
        query['lifeStatus'] = life_status
        
    if chipper_id:
        query['chipperId'] = chipper_id
        
    if chipping_location_id:
        query['chippingLocationId'] = chipping_location_id
    
    animals = db.animals.find(query)
    
    response = []
    for animal in animals:
        animal_dict = {
            "id": animal.id,
            "animalTypes": animal.animalTypes,
            "weight": animal.weight,
            "length": animal.length,
            "height": animal.height,
            "gender": animal.gender,
            "lifeStatus": animal.lifeStatus,
            "chippingDateTime": animal.chippingDateTime.isoformat(),
            "chipperId": animal.chipperId,
            "chippingLocationId": animal.chippingLocationId,
            "visitedLocations": animal.visitedLocations,
            "deathDateTime": animal.deathDateTime.isoformat() if animal.deathDateTime else None
        }
        response.append(animal_dict)
    
    return jsonify(response), 200

@animals.route('/animals/types/<string:typeId>', methods=['GET'])
def get_animal_type(typeId):
    auth = request.authorization
    if not auth or not (auth.username == 'admin' and auth.password == 'password'):
        abort(401)

    if not typeId or typeId.strip() == "":
        abort(400)

    animal_type = db.animal_types.find_one({'id': typeId})
    if not animal_type:
        abort(404, f"Тип животного с typeId {typeId} не найден")

    response = {
        "id": animal_type.id,
        "type": animal_type.type
    }

    return jsonify(response), 200

@animals.route('/animals/<int:animalId>/locations', methods=['GET'])
def get_animal_locations(animalId):
    auth = request.authorization
    if not auth or not (auth.username == 'admin' and auth.password == 'password'):
        abort(401)

    if not animalId or animalId <= 0:
        abort(400)

    startDateTime = request.args.get('startDateTime', None)
    endDateTime = request.args.get('endDateTime', None)
    from_val = int(request.args.get('from', 0))
    size = int(request.args.get('size', 10))

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
    if startDateTime:
        visited_locations = [loc for loc in visited_locations if loc.get('dateTimeOfVisitLocationPoint', None) >= startDateTime]
    if endDateTime:
        visited_locations = [loc for loc in visited_locations if loc.get('dateTimeOfVisitLocationPoint', None) <= endDateTime]

    visited_locations = visited_locations[from_val:from_val+size]

    response = []
    for loc in visited_locations:
        loc_point = db.locationPoints.find_one({'id': loc.get('locationPointId', None)})
        if loc_point:
            response.append({
                "id": loc.get('id', None),
                "dateTimeOfVisitLocationPoint": loc.get('dateTimeOfVisitLocationPoint', None).isoformat(),
                "locationPointId": loc.get('locationPointId', None)
            })

    return jsonify(response), 200



