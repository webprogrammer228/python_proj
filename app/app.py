import os
from flask import Flask
from endpoints.accounts import accounts
from endpoints.animals import animals
from endpoints.locations import locations
from endpoints.registration import registration
from endpoints.animalLocation import animal_location
from endpoints.animalType import animal_type
from database import db

application = Flask(__name__)
#точка входа в приложение

application.register_blueprint(accounts)
application.register_blueprint(animals)
application.register_blueprint(locations)
application.register_blueprint(registration)
application.register_blueprint(animal_location)
application.register_blueprint(animal_type)

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)