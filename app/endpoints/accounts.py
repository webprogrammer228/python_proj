from flask import Blueprint, jsonify, request, abort
from database import db
import re
import base64
from flask_cors import CORS


accounts = Blueprint('accounts', __name__)
CORS(accounts)

@accounts.route('/accounts/<accountId>', methods=['GET'])
def get_account(accountId):
    accountId = int(accountId)
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')

        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
            abort(401, 'Invalid email or password')

    if accountId is None or accountId <= 0:
      return jsonify({'messsage': 'Ivalid id value'}), 400
    account = db.accounts.find_one({'id': accountId})
    if account:
        result = {
            'id': account['id'],
            'firstName': account['firstName'],
            'lastName': account['lastName'],
            'email': account['email']
        }
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Account not found'}), 404
      
@accounts.route('/accounts/signIn', methods=['POST'])
def auth_account():
    data = request.json
    if data is None:
      return jsonify({'message': 'Invalid data'}), 404
    user = db.accounts.find_one({'email': data.get("email"), 'password': data.get("password")})
    if user:
        result = {
            'id': user['id'],
            'firstName': user['firstName'],
            'lastName': user['lastName'],
            'email': user['email']
        }
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
    else:
        return jsonify({'message': 'Account not found'}), 404      
    
@accounts.route('/accounts/search', methods=['GET'])
def search_animals():
    first_name = request.args.get('firstName')
    last_name = request.args.get('lastName')
    search_email = request.args.get('email')
    from_index = request.args.get('from', default=0, type=int)
    size = request.args.get('size', default=10, type=int)

    if from_index < 0 or size <= 0:
        return jsonify({'message': 'Invalid parameters'}), 400

    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = credentials.split(':')
        user = db.accounts.find_one({'email': email, 'password': password})
        if user is None:
            abort(401, 'Invalid email or password')

    query = {}
    if first_name and ' ' not in first_name:
      regex_pattern = '-'.join(['[0-9a-f]{4}']*4)
      query = {'firstName': {'$regex': regex_pattern}}
    if last_name and ' ' not in last_name:
      regex_pattern = '-'.join(['[0-9a-f]{4}']*4)
      query = {'lastName': {'$regex': regex_pattern}}
    if search_email is not None:
      regex_pattern = '^.*-([0-9a-fA-F]+[A-Z0-9]+).*$'
      query = {'email': {'$regex': regex_pattern}}
         
    if not query:
        accounts = db.accounts.find({}, {'_id': 0}).sort('id', 1).skip(from_index).limit(size)
    else:
        accounts = db.accounts.find(query, {'_id': 0}).sort('id', 1).skip(from_index).limit(size)
        
    results = []
    for account in accounts:
        result = {
            'id': account['id'],
            'firstName': account['firstName'],
            'lastName': account['lastName'],
            'email': account['email']
        }
        results.append(result)
    return jsonify(results), 200

@accounts.route('/accounts/<account_id>', methods=['PUT'])
def update_account(account_id):
    account_id = int(account_id)
    data = request.json
    if not data:
        return jsonify({'message': 'Request body is empty'}), 400

    firstName = data.get('firstName', '')
    lastName = data.get('lastName', '')
    email = data.get('email', '')
    password = data.get('password', '')

    if account_id <= 0 or account_id is None:
      return jsonify({"message:": "Invalid account"}), 400
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

    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return jsonify({'message': 'Invalid email address'}), 400

    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        return jsonify({'message': 'Invalid authorization header'}), 401

    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    auth_email, auth_password = credentials.split(':')

    if not auth_email or not auth_password:
        return jsonify({'message': 'Invalid email or password'}), 401

    account = db.accounts.find_one({'id': account_id})
    if account is None:
        return jsonify({'message': 'Account not found'}), 403

    if account['email'] != auth_email or account['password'] != auth_password:
        return jsonify({'message': 'Not authorized to update this account'}), 401

    if email != account['email'] and db.accounts.find_one({'email': email}):
        return jsonify({'message': 'Account with email already exists'}), 409
    updated_account = {
        'id': account_id,
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'password': password
    }
    db.accounts.replace_one({'id': account_id}, updated_account)
    result = {
        'id': account_id,
        'firstName': firstName,
        'lastName': lastName,
        'email': email
    }
    return jsonify(result), 200

@accounts.route('/accounts/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    account_id = int(account_id)
    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Basic '):
        abort(401, 'Invalid or missing authorization header')

    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    email, password = credentials.split(':')

    current_account = db.accounts.find_one({'id': account_id})
    
    print(current_account, 'current_account')
    
    if account_id is None or account_id <= 0:
      return jsonify({"message:": "Error account"}), 400
    
    if not auth_header:
      return jsonify({"message": "Not auth header"}), 401
    
    find_account = db.accounts.find_one({'email': email})
    if find_account is None:
      return jsonify({"message": "Not auth account"}), 401
    
    if current_account is None or current_account['email'] != email and current_account['password'] != password:
     abort(403, 'Unauthorized to delete this account') 
    
    account = db.accounts.find_one({'id': account_id})
        
    animal = db.animals.find_one({"id": account_id})
    if animal:
      chipper = animal.get("chipperId")     
      if chipper == account_id:
        return jsonify({"error:": "Account linked with animal"}), 400

    if account is None:
      abort(403, 'Unauthorized to delete this account')

    if account['email'] != email and account['password'] != password:
        abort(401, 'Unauthorized to delete this account')

    if db.animals.find_one({'сhipperId': account_id}) is not None:
        abort(400, 'Account is associated with an animal')

    db.accounts.delete_one({'id': account_id})

    return jsonify({"message: Successfull delete account"}), 200