from flask import Blueprint, jsonify, request
from database import db
import re

accounts = Blueprint('accounts', __name__)

@accounts.route('/accounts/<int:id>', methods=['GET'])
def get_account(id: int):
    if id is None or id <= 0:
        return jsonify({'messsage': 'Invalid data'}), 400
    elif db.accounts.find_one({'id': id}):
      account = db.accounts.find_one({'id': id})
      result = {
            'id': account['id'],
            'firstName': account['firstName'],
            'lastName': account['lastName'],
            'email': account['email']
      }
      return jsonify(result), 200
    else:
      return jsonify({'message': 'Account not found'}), 404

@accounts.route('/accounts/search', methods=['GET'])
def search_accounts():
    first_name = request.args.get('firstName')
    last_name = request.args.get('lastName')
    email = request.args.get('email')
    from_index = request.args.get('from', default=0, type=int)
    size = request.args.get('size', default=10, type=int)

    if from_index < 0 or size <= 0:
        return jsonify({'message': 'Invalid parameters'}), 400
    query = {}
    if first_name:
        query['firstName'] = {'$regex': '^'+first_name, '$options': 'i'}
    if last_name:
        query['lastName'] = {'$regex': '^'+last_name, '$options': 'i'}
    if email:
        query['email'] = {'$regex': '^'+email, '$options': 'i'}
    
    accounts = db.accounts.find(query, {'_id': 0}).sort('id', 1).skip(from_index).limit(size)
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
      return jsonify({'message': 'Invalid email format'}), 400
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





