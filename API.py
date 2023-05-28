from flask import Flask, jsonify, request, render_template
import requests
import functions

app = Flask(__name__)


class LoggedInUser:
    """
    user object
    """
    def __init__(self, userId, displayName):
        self.userId = userId
        self.displayName = displayName

class clothingList:
    """
    each user has a list of items that belong to the same category.
    The list consists of all data on item.
    """
    def __init__(self,userId, category, list):
        self.userId = userId
        self.category = category
        self.list = list


# define a route for the root endpoint
@app.route('/')
def hello_world():
    return 'Hello, World!'


# get weather report.
# @app.route('/temperature')
# def temperature():
#     longitude = request.json.get('longitude')
#     latitude = request.json.get('latitude')
#     r = requests.get('https://api.openweathermap.org/data/2.5/weather?lat='+latitude+'.34&lon='+longitude+'.99&appid=8f3241a0140c7cbf04fd85bcb7b1cef9')
#     json_obj = r.json()
#     #generate outfit
#     outfit = generate(json_obj)
#     temp_k = float(json_obj['main']['temp'])
#     temp_c = temp_k-273.15 # convert to celsius
#     return temp_c

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
    functions.insert_new_item(data, userid)
    return {'result': 'success'}


@app.route('/closet')
def get_closet():
    # Get query parameters from request.args
    userid = request.args.get('id')
    category = request.args.get('category')
    print(userid+","+category)
    # Perform operations using userid and category
    data = functions.get_closet(userid, category)

    # Return response as JSON
    cList = clothingList(userid,category,data)
    # return jsonify(closet_items)
    return jsonify(cList.__dict__)

@app.route('/outfit')
def get_outfit():
    # Get query parameters from request.args
    userid = request.args.get('id')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    print(request.args)
    return jsonify(None)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
