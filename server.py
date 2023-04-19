from flask import Flask
import pymongo

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        severSelectionTimeoutMS=1000)
    db = mongo.smartWardrobe
    mongo.server_info()
except:
    print("ERROR- cannot connect to db")


@app.route('/register', methods=['POST'])
def create_user():
    try:
        user = {"name": "A", "lastName": "AA"}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
    except Exception as ex:
        print("********")
        print(ex)
        print("********")


if __name__ == '__main__':
    app.run(port=80, debug=True)
