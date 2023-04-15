from flask import Blueprint, jsonify, request, abort
from database import db
import re
import base64

registration = Blueprint('registration', __name__, url_prefix='/')

@registration.route('/registration', methods=['POST'])
def register_account():
    data = request.json
    if not data:
      return jsonify({'message': 'Request body is empty'}), 400

    firstName = data.get('firstName', '')
    lastName = data.get('lastName', '')
    email = data.get('email', '')
    password = data.get('password', '')

    if firstName is not None:
      firstName = firstName.strip()
    if lastName is not None:  
      lastName = lastName.strip()
    if email is not None:   
      email = email.strip()
    if password is not None:   
      password = password.strip()

    if not firstName or not lastName or not email or not password:
      return jsonify({'message': 'Invalid data'}), 400

    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')

        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
            abort(401, 'Invalid email or password')
        else:
            return jsonify({'message': 'User is already authenticated'}), 403

    if not firstName or not lastName or not email or not password:
        return jsonify({'message': 'Invalid data'}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'message': 'Invalid email format'}), 400

    if db.accounts.find_one({'email': email}):
        return jsonify({'message': 'Account with email already exists'}), 409

    new_id = db.accounts.count_documents({}) + 1
    account = {
        'id': new_id,
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'password': password  
    }
    result = {
        'id': new_id,
        'firstName': firstName,
        'lastName': lastName,
        'email': email
    }
    
    db.accounts.insert_one(account)
    return jsonify(result), 201