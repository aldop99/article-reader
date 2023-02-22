from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
import time  
from datetime import datetime
from dotenv import load_dotenv
import os
from graph import *

load_dotenv()

app = Flask(__name__)

db_name = os.environ.get("DB_NAME")
client = MongoClient('mongodb://localhost:27017')
db = client[db_name]
collections = db["users"]


@app.route('/add-user', methods=['POST'])
def add_user():
    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")

    user = {'city': request.json['city'],
            'email': request.json['email'],
            'topic1': request.json['topic1'],
            'topic2': request.json['topic2'],
            'topic3': request.json['topic3'],
            'topic4': request.json['topic4'],
            'topic5': request.json['topic5'],
            'topic6': request.json['topic6'],
            'topic7': request.json['topic7'],
            'topic8': request.json['topic8'],
            'timestamp': str_date_time
            }
    # Insert the new user into the users collection
    user_id = collections.insert_one(user).inserted_id
    # Find the new user in the collection
    new_user = collections.find_one({'_id': user_id})
    # Convert the new user's ObjectId to a string
    new_user['_id'] = str(new_user['_id'])
    # Return a success message and the new user
    return jsonify({'success': True, 'user': new_user})

@app.route('/', methods=['GET'])
def get_users():
    # Find all users in the collection
    users = list(collections.find())
    # Convert the ObjectIds to strings
    for user in users:
        user['_id'] = str(user['_id'])
    # Return a success message and the list of users
    return jsonify({'success': True, 'users': users})

@app.route('/user-articles/<user_id>/<topic>', methods=['GET'])
def get_user_article(user_id, topic):
    article = []
    # Convert the ObjectIds to strings
    user = collections.find_one({'user': ObjectId(user_id), 'topic': topic})
    my_collection = db[topic]
    # x = my_collection.find_one()
    
    for x in my_collection.find():
       article.append(x['value'])
        
    # print(x)    
    return jsonify({'success': True, 'user': user_id, 'topic': topic , "articles": article})

@app.route('/user-articles/<article_id>', methods=['GET'])
def get_article_recomendation(article_id):
    recomended_article = search_node(article_id)
    return jsonify({'success': True, 'given_article_id': article_id, 'recomended_article': recomended_article})
    # http://localhost:5000/user-articles/63dd801da0af182eb96581e1

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
