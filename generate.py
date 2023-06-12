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

# todo: to make life easier: change whether tags to only 4 options: summer, winter, cool_day(autumn), warm_day(spring)


import mysql.connector
import random
from datetime import datetime

from functions import get_category_id

# Establish a connection to the MySQL server
db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
# db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
cursordb = db.cursor()

need_jacket = 0
need_coat = 0
closed_Shoes = 0
rain = 0
cover_up = 0

cool_threshold = 18
warm_threshold = 24
cold_threshold = 14
wear_again_range = 14


def chooseOutfitType(options):
    """
    choose outfit type
    :param options: lost of options of outfit types-dress\skirt\pants ect.
    :return:randomly chosen option
    """
    options = ["skirts", "pants", "Dresses"]
    random_choice = random.choice(options)  # need to change based on answer from db based on how many options we have.
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
        need_coat = 1
        closed_shoes = 1
        cover_up = 1
    if cool_threshold < temp_c < warm_threshold:
        need_jacket = 1
        cover_up = 1
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

def get_top(type, weather, thickness, sleeves):
    """
       returns random clothing item that is of 'type'
        category  that is a top (shirt)
        and of requested weather, thickness and length
       :param type:
       :param weather:
       :return:
       """
    random_weather = random.choice(weather)
    random_thickness = random.choice(thickness)
    random_sleeves = random.choice(sleeves)

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
            "AND tci.tag_value = %s"
            "AND t.tag_name = 'thickness'  "
            "AND tci.tag_value = %s"
            "AND t.tag_name = 'sleeves'  "
            "AND tci.tag_value = %s"
            , [type, random_weather, random_thickness, random_sleeves])
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        if data == []:
            return data
        random_choice = random.choice(data)
        return random_choice
    except Exception as e:
        print(f"An error occurred: {e}")

def get_bottom(type, weather, thickness, length):
    """
    returns random clothing item that is of 'type'
     category  that is a bottom (pants or skirt)
     and of requested weather, thickness and length
    :param type:
    :param weather:
    :return:
    """

    random_weather = random.choice(weather)
    random_thickness = random.choice(thickness)
    random_length = random.choice(length)
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
            "AND tci.tag_value = %s"
            "AND t.tag_name = 'thickness'  "
            "AND tci.tag_value = %s"
            "AND t.tag_name = 'length'  "
            "AND tci.tag_value = %s"
            , [type, random_weather, random_thickness, random_length])
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        if data == []:
            return data
        random_choice = random.choice(data)
        return random_choice
    except Exception as e:
        print(f"An error occurred: {e}")


def get_dress(type, weather, thickness, sleeves, length):
    """
    returns random clothing item that is of 'type'
     category  that is a dress
     and of requested weather, thickness sleeves and length
    :param type:
    :param weather:
    :return:
    """
    random_weather = random.choice(weather)
    random_thickness = random.choice(thickness)
    random_sleeves = random.choice(sleeves)
    random_length = random.choice(length)
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
            "AND tci.tag_value = %s"
            "AND t.tag_name = 'thickness'  "
            "AND tci.tag_value = %s"
            "AND t.tag_name = 'sleeves'  "
            "AND tci.tag_value = %s"
            "AND t.tag_name = 'length'  "
            "AND tci.tag_value = %s"
            , [type, random_weather, random_thickness, random_sleeves, random_length])
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        if data == []:
            return data
        random_choice = random.choice(data)
        return random_choice
    except Exception as e:
        print(f"An error occurred: {e}")

def get_random_item(type, weather):
    """
    returns random clothing item that is of 'type'
     category and of requested weather
    :param type:
    :param weather:
    :return:
    """
    random_weather = random.choice(weather)
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
            "AND t.tag_name = 'weather'"
            "AND tci.tag_value = %s", [type, random_weather])
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        if data == []:
            return data
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
    date_string = date.strftime("%Y-%m-%d")
    try:

        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()
        sql = "INSERT INTO outfits (top, bottom, outwear, shoes, last_used, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (top, bottom, outwear, shoes, date_string, user_id)
        cursordb.execute(sql, val)
        db.commit()
        cursordb.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_outfit_by_id(id):
    """
    returns outfit based on outfit id    :param id:
    :return: all outfit info
    """
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute("SELECT * "
                         "FROM outfits WHERE id = %s;", ([id]))
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


def checkOutfit(user_id, top, bottom, shoes):
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute("SELECT last_used, id "
                         "FROM outfits WHERE user_id = %s  "
                         "AND top = %s  AND bottom = %s  "
                         "AND shoes = %s;", (user_id, top, bottom, shoes))
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


def summer_outfit(json_obj, user_id):
    """

    :return: outfit id
    """

    date = datetime.now().date()
    again = 1
    while again == 1:
        top = []
        bottom = []
        while top == [] or bottom == []:
            clothing_type = chooseOutfitType(json_obj)
            if clothing_type != "dress":
                top = get_top("shirt", ["hot"], ["light"], ["sleeveless", "short sleeves"])
                bottom = get_bottom(clothing_type, ["hot"], ["light"], ["short", "knee length"])

            else:
                top = get_dress(clothing_type, ["hot"], ["light"], ["sort", "sleeveless"], ["short", "knee length"])
                bottom = [None]
        shoes = get_random_item("Footwear", ["hot"])
        outwear = None
        check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
        if check == []:
            add_outfit(user_id, top[0], bottom[0], outwear, shoes[0])
            check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
            return check[0][1]

        elif (check[0][0] - date).days < wear_again_range:
            again = 1
        else:
            return check[1]


# todo:
def cool_outfit(json_obj):
    """
    either summer outfit with long sleeves- or short sleeves and a jacket
    :return: outfit id
    """

    pass


# todo:
def colder_outfit():
    pass


# todo:
def winter_outfit():
    pass


# todo:
def getOutfit(json_obj, user_id):
    """
    gets weahter and decides what kind of outfit to generate
    :param json_obj:
    :param user_id:
    :return:
    """
    temperature = getWeather(json_obj)

    if temperature >= warm_threshold:
        outfit_id = summer_outfit(json_obj, user_id)

    elif cool_threshold <= temperature <= warm_threshold:
        outfit_id = cool_outfit()
    elif cold_threshold <= temperature <= cool_threshold:
        outfit_id = colder_outfit()
    else:
        outfit_id = winter_outfit()
    return get_outfit_by_id(outfit_id)


from flask import Flask, jsonify, request, render_template
import requests
import functions


def temperature():
    longitude = "34"
    latitude = "32"
    r = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?lat=' + latitude + '.34&lon=' + longitude + '.99&appid=8f3241a0140c7cbf04fd85bcb7b1cef9')
    json_obj = r.json()
    # generate outfit
    outfit = getOutfit(json_obj, 1)
    print(outfit)
    temp_k = float(json_obj['main']['temp'])
    temp_c = temp_k - 273.15  # convert to celsius
    return temp_c


if __name__ == '__main__':
    temperature()
