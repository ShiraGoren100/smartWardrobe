import json
from flask import Flask, jsonify, request
import user_file
import generate
from closet import insert_new_item, get_item_property, get_item_by_id, delete_item, get_items_from_closet
from generate import regenerate
from weather_file import temperature

app = Flask(__name__)


class LoggedInUser:
    """
    user object
    """

    def __init__(self, userId, displayName, days_interval):
        self.userId = userId
        self.displayName = displayName
        self.interval = days_interval


class clothingList:
    """
    each user has a list of items that belong to the same category.
    The list consists of all data on item.
    """

    def __init__(self, list):
        # self.userId = userId
        # self.category = category
        self.list = list


class clothing_item:
    def __int__(self, id, picture, list):
        self.id = id
        self.picture = picture
        self.list = list


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
    uid, uname, days_interval = user_file.insert_new_user(username, password, email)
    user = LoggedInUser(uid, uname, days_interval)
    return jsonify(user.__dict__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    uid, uname, days_interval = user_file.get_user_id(password, email)
    user = LoggedInUser(uid, uname, days_interval)
    return jsonify(user.__dict__)


@app.route('/addItem', methods=['POST'])
def addItem():
    data = request.get_json()
    userid = request.args.get('id')
    print(userid)
    print(data)
    insert_new_item(data, userid)
    return {'result': 'success'}

def get_item_as_clist(i, list1):
    properties = get_item_property(i[0])
    if properties is None:
        return
    title_value_list = []
    # tup = property['properties']
    for prop in properties:
        title = prop[0]
        value = prop[1]
        title_value_list.append({'title': title, 'value': value})
    item = {"id": i[0], "img": i[1], "properties": title_value_list}
    # item={"id":i[0], "img":i[1]}
    list1.append(item)

@app.route('/closet')
def get_closet():
    # Get query parameters from request.args
    userid = request.args.get('id')
    category = request.args.get('category')
    print(userid + "," + category)
    # Perform operations using userid and category
    data = get_items_from_closet(userid, category)
    list1 = []
    for i in data:
       get_item_as_clist(i, list1)
    # Return response as JSON
    cList = clothingList(list1)
    # return jsonify(closet_items)
    # ret={'list':list}
    return jsonify(list1)


@app.route('/outfit')
def get_outfit():
    # Get query parameters from request.args
    userid = request.args.get('id')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    tempJson = temperature(latitude, longitude)
    outfit_info = get_outfit(tempJson, userid)
    if outfit_info == "not enough items for outfit interval":
        error_response = {"error": outfit_info}
        json_response = json.dumps(error_response)
        return json_response, 500

    list1 = []
    for i in range(1, 5):
        if outfit_info[0][i] is not None:
                item = get_item_by_id(outfit_info[0][i])[0]
                get_item_as_clist(item, list1)
        # Return response as JSON
    cList = clothingList(list1)
    outfit = {"outfitId": outfit_info[0][0], "date": outfit_info[0][5].strftime("%d/%m/%y"), "list": list1, "userId": outfit_info[0][6]}
    print(request.args)
    return jsonify(outfit)
@app.route('/regenerate')
def regenerate_outfit():
    # Get query parameters from request.args
    userid = request.args.get('id')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    outfitid = request.args.get('outfitid')
    tempJson = temperature(latitude, longitude)
    outfit_info = regenerate(tempJson, userid, outfitid)
    if outfit_info == "not enough items for outfit interval":
        error_response = {"error": outfit_info}
        json_response = json.dumps(error_response)
        return json_response, 500
    list1 = []
    for i in range(1, 5):
        if outfit_info[0][i] is not None:
                item = get_item_by_id(outfit_info[0][i])[0]
                get_item_as_clist(item, list1)
        # Return response as JSON
    cList = clothingList(list1)
    outfit = {"outfitId": outfit_info[0][0], "date": outfit_info[0][5].strftime("%d/%m/%y"), "list": list1, "userId": outfit_info[0][6]}
    print(request.args)
    return jsonify(outfit)


@app.route('/deleteItem', methods=['DELETE'])
def deleteItem():
    item_id = request.args.get('id')
    delete_item(item_id)
    return {'result': 'success'}


@app.route('/rateOutfit', methods=['POST'])
def rateOutfit():
    # todo:add rating to outfit
    userid = request.args.get('id')
    outfitid = request.args.get('outfitID')
    option = request.args.get('option')
    print(userid)
    generate.change_temp_thresholds(userid, outfitid,  option)
    return {'result': 'success'}

@app.route('/interval', methods=['POST'])
def updateInterval():
    # todo:add rating to outfit
    userid = request.args.get('id')
    interval=request.args.get('interval')
    print(userid)
    user_file.set_days_interval(userid, interval)
    return {'result': 'success'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
