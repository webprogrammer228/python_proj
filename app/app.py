import os
from flask import Flask
from endpoints.accounts import accounts
from endpoints.animals import animals
from endpoints.locations import locations
from database import db

application = Flask(__name__)

application.register_blueprint(accounts)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)