import pymongo
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
# mongo = pymongo(app)
client = pymongo.MongoClient("")
db = client.test

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users

    username = request.json['username']
    password = request.json['password']

    user = users.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful'}), 200


if __name__ == '__main__':
    app.run(debug=True)
