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

def chooseOutfitType(options):
    """
    choose outfit type
    :param options: lost of options of outfit types-dress\skirt\pants ect.
    :return:randomly chosen option
    """
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT c.type AS category, COUNT(ci.id) AS count FROM"
            " categories c LEFT JOIN clothing_item ci ON ci.category_id = c.id WHERE c.type IN"
            " ('skirt', 'dress', 'pants') GROUP BY c.type;")
        # Fetch the result
        options = cursordb.fetchall()
        cursordb.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")

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


def getOutfit(json_obj):
   getWeather(json_obj)
   type = chooseOutfitType()
   if cover_up:
       # try:
       #     # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
       #     db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
       #                                  port=3307)
       #     cursordb = db.cursor()
       #     cursordb.execute(
       #         "SELECT * FROM clothing_item WHERE  user_id = %s and category= %s", (user_id, category_id))
       #     # Fetch the result
       #     data = cursordb.fetchall()
       #     cursordb.close()
       #     db.close()
       #     return data
       # except Exception as e:
       #     print(f"An error occurred: {e}")
       return
