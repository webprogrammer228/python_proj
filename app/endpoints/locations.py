from flask import Blueprint, jsonify, request, abort
from database import db

locations = Blueprint('locations', __name__)

from flask import Blueprint, jsonify, request, abort
from database import db

locations = Blueprint('locations', __name__)

@locations.route('/locations/<int:pointId>', methods=['GET'])
def get_location(pointId):
    auth = request.authorization
    if not auth or not (auth.username == 'admin' and auth.password == 'password'):
        abort(401)

    if not pointId or pointId <= 0:
        abort(400)

    location = db.locationPoints.find_one({'id': pointId})
    if not location:
        abort(404, f"Точка локации с pointId {pointId} не найдена")

    response = {
        "id": location.get('id', None),
        "latitude": location.get('latitude', None),
        "longitude": location.get('longitude', None)
    }

    return jsonify(response), 200
