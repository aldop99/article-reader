from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client["news_database"]
collections = db["users"]

@app.route('/')
def start():
    return jsonify({'message': 'Welcome from Flask.'})

@app.route('/add-user', methods=['POST'])
def add_user():
    user = {'city': request.json['city'],
            'email': request.json['email'],
            'topic1': request.json['topic1'],
            'topic2': request.json['topic2'],
            'topic3': request.json['topic3'],
            'topic4': request.json['topic4'],
            'topic5': request.json['topic5'],
            'topic6': request.json['topic6'],
            'topic7': request.json['topic7'],
            'topic8': request.json['topic8']
            }
    # Insert the new user into the users collection
    user_id = collections.insert_one(user).inserted_id
    # Find the new user in the collection
    new_user = collections.find_one({'_id': user_id})
    # Convert the new user's ObjectId to a string
    new_user['_id'] = str(new_user['_id'])
    # Return a success message and the new user
    return jsonify({'success': True, 'user': new_user})

@app.route('/users', methods=['GET'])
def get_users():
    # Find all users in the collection
    users = list(collections.find())
    # Convert the ObjectIds to strings
    for user in users:
        user['_id'] = str(user['_id'])
    # Return a success message and the list of users
    return jsonify({'success': True, 'users': users})

@app.route('/update-user/<user_id>', methods=['PUT'])
def update_user(user_id):
    # Get the request data as a json object
    data = request.get_json()
    # Find the user in the collection
    user = collections.find_one({'_id': ObjectId(user_id)})
    # Check if the user exists
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    # Update the user with the new data
    collections.update_one({'_id': ObjectId(user_id)}, {'$set': data})
    # Find the updated user in the collection
    updated_user = collections.find_one({'_id': ObjectId(user_id)})
    # Convert the updated user's ObjectId to a string
    updated_user['_id'] = str(updated_user['_id'])
    # Return a success message and the updated user
    return jsonify({'success': True, 'user': updated_user})

@app.route('/delete-user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
  # Find the user in the collection
  user = collections.find_one({'_id': ObjectId(user_id)})
  # Check if the user exists
  if not user:
    return jsonify({'success': False, 'error': 'User not found'}), 404
  # Delete the user from the collection
  collections.delete_one({'_id': ObjectId(user_id)})
  # Convert the user's ObjectId to a string
  user['_id'] = str(user['_id'])
  # Return a success message and the deleted user
  return jsonify({'success': True, 'user': user})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
