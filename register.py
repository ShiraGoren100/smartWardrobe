# import pymongo
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from mongoengine.errors import DoesNotExist
# from flask_pymongo import PyMongo
# from werkzeug.security import generate_password_hash, check_password_hash
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
# client = pymongo.MongoClient("mongodb://localhost:27017/users")
# db = client.test

app = Flask(__name__)
app.config['MONGO_SETTINGS'] = {
    'db': 'smartWardrobe',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine(app)


class User(db.Document):
    name = db.stringField(required=True)
    email = db.EmailField(required=True, uniqe=True)
    password = db.stringField(required=True)



@app.route('/register', methods=['POST'])
def register():

    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    existing_user = users.objects.get({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already taken'}), 409

    existing_email = users.find_one({'email': email})
    if existing_email:
        return jsonify({'message': 'Email already registered'}), 409

    hashed_password = generate_password_hash(password)

    user = {'username': username, 'email': email, 'password': hashed_password}
    users.insert_one(user)

    return jsonify({'message': 'Registration successful'}), 201


if __name__ == '__main__':
    app.run(debug=True)
