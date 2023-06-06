"""
work flow:
get weather.
look at oufits- if there is an outiit that works with a good date-send to user and update last worn
otherwise-get dress\shirt+pants\shirt+skirt, that work with the weather report
decide if outwear is needed
if needed-choose.
choose footwear
add outfit to table?
sent outfit to user
add the date as 'last worn' for this outfit
"""

import mysql.connector
import random
from datetime import datetime

from functions import get_category_id

# Establish a connection to the MySQL server
db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
#db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
cursordb = db.cursor()

need_jacket = 0
need_coat=0
closed_Shoes=0
rain=0
cover_up = 0

cool_threshold=18
warm_threshold=24
cold_threshold=14

def chooseOutfitType(options):
    """
    choose outfit type
    :param options: lost of options of outfit types-dress\skirt\pants ect.
    :return:randomly chosen option
    """
    # try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
        #                              port=3307)
        # cursordb = db.cursor()
        # cursordb.execute(
        #     "SELECT c.type AS category, COUNT(ci.id) AS count FROM"
        #     " categories c LEFT JOIN clothing_item ci ON ci.category_id = c.id WHERE c.type IN"
        #     " ('skirt', 'dress', 'pants') GROUP BY c.type;")
        # # Fetch the result
        # options = cursordb.fetchall()
        # cursordb.close()
        # db.close()
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    options = ["skirt", "pants", "dress"]
    random_choice = random.choice(options)#need to change based on answer from db based on how many options we have.
    return random_choice


def getWeather(json_obj):
    """
    define weather related needs for outfit
    :param json_obj:
    :return:
    """
    temp_k = float(json_obj['main']['temp'])
    temp_c = temp_k - 273.15  # convert to celsius
    if temp_c < 0:
        need_coat=1
        closed_shoes=1
        cover_up=1
    if cool_threshold < temp_c < warm_threshold:
        need_jacket=1
        cover_up=1
        closed_shoes = 0
    else:
        need_coat = 0
        closed_shoes = 0
        cover_up = 0
    return temp_c


"""
start with summer:
if it is hot, we want to select all pants, skirts, shirts that are short sleeves and fit for summer.
then out of the categories possible we want to choose one(skirt\pants\dress)
then we want to add foot ware.

if it is cool:
we want to select all summer things and add a jacket
or- we want to select longer sleeves with no jacket.

if it is colder:
we want to select everything that is longer
= jacket

if it is even colder we want to select a sweater and a jacket

if it is very cold- sweate, coat.

"""

def get_random_item(type, weather):
    """
    returns random clothing item that is of 'type'
     category and of requested weather
    :param type:
    :param weather:
    :return:
    """
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category "
            "FROM clothing_item ci JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci ON tci.clothing_item_id = ci.id "
            "JOIN tags t ON t.id = tci.tag_id WHERE c.type= %s"
            "AND t.tag_name = 'weather'  "
            "AND tci.tag_value = 'summer'", type)
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        random_choice = random.choice(data)
        return random_choice
    except Exception as e:
        print(f"An error occurred: {e}")

def add_outfit(user_id, top, bottom, outwear, shoes):
    """
    add outfit to db
    :param user_id:
    :param top:
    :param bottom:
    :param outwear:
    :param shoes:
    :return:
    """
    date = datetime.now()
    try:

        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()
        sql = "INSERT INTO outfits (top, bottom, outwear, shoes, last_used, user_id) VALUES (%d, %d, %d, %d, %s, %d)"
        val = (top, bottom, outwear,shoes,date,user_id)
        cursordb.execute(sql, val)
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")


#todo: to make life easier: change whether tags to only 4 options: summer, winter, cool_day(autumn), warm_day(spring)


#todo:
def summer_outfit(json_obj, user_id):
    """

    :return:
    """
    type = chooseOutfitType(json_obj)
    if type is not "dress":
        top = get_random_item("shirt", "summer")
        bottom = get_random_item(type, "summer")
    else:
        top = get_random_item(type, "summer")
        bottom = None
    shoes = get_random_item("footware", "summer")

    outwear = None
    accessories = None
    # todo: get the id of each item and give to this function
    add_outfit(user_id, top[0], bottom[0], outwear, shoes[0])

    #todo: return the outfit pictures to client
    outfit = []
    outfit.append(top)
    outfit.append(bottom)
    outfit.append(shoes)
    return outfit


#todo:
def cool_outfit():
    pass

#todo:
def colder_outfit():
    pass

#todo:
def winter_outfit():
    pass


#todo:
def getOutfit(json_obj, user_id):
    """
    gets weahter and decides what kind of outfit to generate
    :param json_obj:
    :param user_id:
    :return:
    """
    temperature = getWeather(json_obj)

    if temperature >= warm_threshold:
       summer_outfit()

    elif cool_threshold <= temperature <= warm_threshold:
        cool_outfit()
    elif cold_threshold <= temperature <= cool_threshold:
        colder_outfit()
    else:
        winter_outfit()


