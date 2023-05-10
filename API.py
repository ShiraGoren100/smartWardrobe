from flask import Flask, jsonify, request

import functions

app = Flask(__name__)


class LoggedInUser:
    def __init__(self, userId, displayName):
        self.userId = userId
        self.displayName = displayName


# define a route for the root endpoint
@app.route('/')
def hello_world():
    return 'Hello, World!'


# define a route for a custom endpoint
@app.route('/api/users', methods=['GET'])
def get_users():
    users = [
        {'userId': '123', 'displayName': 'alice'},
        {'userId': '124', 'displayName': 'bob'},
        {'userId': '125', 'displayName': 'charlie'}

    ]
    return jsonify(users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    username = request.json.get('username')
    uid, uname = functions.insert_new_user(username, password, email)
    user = LoggedInUser(uid, uname)
    return jsonify(user.__dict__)



@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    uid, uname = functions.get_user_id(password, email)
    user = LoggedInUser(uid, uname)
    return jsonify(user.__dict__)


@app.route('/addItem', methods=['POST'])
def addItem():
    data = request.get_json()
    userid = request.args.get('id')
    print(userid)
    print(data)
    return {'result': 'success'}


@app.route('/closet')
def get_closet():
    # Get query parameters from request.args
    userid = request.args.get('id')
    category = request.args.get('category')

    # Perform operations using userid and category

    # Return response as JSON
    # return jsonify(closet_items)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
