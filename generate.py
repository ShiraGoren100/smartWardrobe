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
# db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
cursordb = db.cursor()

need_jacket = 0
need_coat = 0
closed_Shoes = 0
rain = 0
cover_up = 0

# cool_threshold = 18
# warm_threshold = 24
# cold_threshold = 14
wear_again_range = 14

def get_users_thresholds(user_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()


        cursordb.execute("SELECT hot,warm,cool FROM user WHERE id = %s;", [user_id])
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


def chooseOutfitType(options):
    """
    choose outfit type
    :param options: lost of options of outfit types-dress\skirt\pants ect.
    :return:randomly chosen option
    """
    # options = ["skirts", "pants", "Dresses"]
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
    # if temp_c < 0:
    #     need_coat = 1
    #     closed_shoes = 1
    #     cover_up = 1
    # if cool_threshold < temp_c < warm_threshold:
    #     need_jacket = 1
    #     cover_up = 1
    #     closed_shoes = 0
    # else:
    #     need_coat = 0
    #     closed_shoes = 0
    #     cover_up = 0
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
with jacket or warm without jacket



if it is very cold- warm and coat

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
    random_type = random.choice(type)
    random_weather = random.choice(weather)
    random_thickness = random.choice(thickness)
    random_sleeves = random.choice(sleeves)

    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category "
            "FROM clothing_item ci "
            "JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_sleeves ON tci_sleeves.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_thickness ON tci_thickness.clothing_item_id = ci.id "
            "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
            "JOIN tags t_sleeves ON t_sleeves.id = tci_sleeves.tag_id "
            "JOIN tags t_thickness ON t_thickness.id = tci_thickness.tag_id "
            "WHERE c.type = %s "
            "AND t_weather.tag_name = 'weather' AND tci_weather.tag_value = %s "
            "AND t_sleeves.tag_name = 'sleeves' AND tci_sleeves.tag_value = %s "
            "AND t_thickness.tag_name = 'thickness' AND tci_thickness.tag_value = %s;"
   ,
            [random_type, random_weather, random_sleeves, random_thickness]
        )



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
    random_type = random.choice(type)
    random_weather = random.choice(weather)
    random_thickness = random.choice(thickness)
    random_length = random.choice(length)
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category "
            "FROM clothing_item ci "
            "JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_length ON tci_length.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_thickness ON tci_thickness.clothing_item_id = ci.id "
            "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
            "JOIN tags t_length ON t_length.id = tci_length.tag_id "
            "JOIN tags t_thickness ON t_thickness.id = tci_thickness.tag_id "
            "WHERE c.type = %s "
            "AND t_weather.tag_name = 'weather' AND tci_weather.tag_value = %s "
            "AND t_length.tag_name = 'length' AND tci_length.tag_value = %s "
            "AND t_thickness.tag_name = 'thickness' AND tci_thickness.tag_value = %s;"
            , [random_type, random_weather, random_length, random_thickness])
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
    random_type = random.choice(type)
    random_weather = random.choice(weather)
    random_thickness = random.choice(thickness)
    random_sleeves = random.choice(sleeves)
    random_length = random.choice(length)
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category "
            "FROM clothing_item ci "
            "JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_sleeves ON tci_sleeves.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_length ON tci_length.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_thickness ON tci_thickness.clothing_item_id = ci.id "
            "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
            "JOIN tags t_sleeves ON t_sleeves.id = tci_sleeves.tag_id "
            "JOIN tags t_length ON t_length.id = tci_length.tag_id "
            "JOIN tags t_thickness ON t_thickness.id = tci_thickness.tag_id "
            "WHERE c.type = %s "
            "AND t_weather.tag_name = 'weather' AND tci_weather.tag_value = %s "
            "AND t_length.tag_name = 'length' AND tci_length.tag_value = %s "
            "AND t_sleeves.tag_name = 'sleeves' AND tci_sleeves.tag_value = %s "
            "AND t_thickness.tag_name = 'thickness' AND tci_thickness.tag_value = %s;"
            , [random_type, random_weather, random_length, random_sleeves, random_thickness])
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
    random_type = random.choice(type)
    random_weather = random.choice(weather)
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category "
            "FROM clothing_item ci JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci ON tci.clothing_item_id = ci.id "
            "JOIN tags t ON t.id = tci.tag_id WHERE c.type= %s"
            "AND t.tag_name = 'weather'"
            "AND tci.tag_value = %s", [random_type, random_weather])
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

        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
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
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
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
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
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
    options = ["skirts", "pants", "Dresses"]
    while again == 1:
        top = []
        bottom = []
        while top == [] or bottom == []:
            clothing_type = chooseOutfitType(options)
            if clothing_type != "Dresses":
                top = get_top(["shirts"], ["hot"], ["light"], ["sleeveless", "short sleeves"])
                bottom = get_bottom([clothing_type], ["hot"], ["light"], ["short", "knee length"])
                if bottom == []:
                    options.remove(clothing_type)

            else:
                top = get_dress([clothing_type], ["hot"], ["light"], ["short sleeves", "sleeveless"], ["short", "knee length"])
                bottom = [None]
                if top == []:
                    options.remove(clothing_type)
        shoes = get_random_item(["Footwear"], ["hot"])
        if shoes == []:
            shoes = [None]
        outwear = None
        check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
        if check == []:
            add_outfit(user_id, top[0], bottom[0], outwear, shoes[0])
            check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
            return check[0][1]

        elif (date - check[0][0]).days < wear_again_range:
            again = 1
        else:
            return check[1]

def is_type_sleeves(top_id, sleeve_type):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()

        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category "
            "FROM clothing_item ci JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci ON tci.clothing_item_id = ci.id "
            "JOIN tags t ON t.id = tci.tag_id WHERE ci.id = %s"
            "AND t.tag_name ='sleeves'"
            "AND tci.tag_value = %s", [top_id, sleeve_type])
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        if data == []:
            return False
        return True
    except Exception as e:
        print(f"An error occurred: {e}")

def is_type_weather(clothing_id, weather_type):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
        cursordb = db.cursor()

        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category "
            "FROM clothing_item ci JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci ON tci.clothing_item_id = ci.id "
            "JOIN tags t ON t.id = tci.tag_id WHERE ci.id = %s"
            "AND t.tag_name ='sleeves'"
            "AND tci.tag_value = %s", [clothing_id, weather_type])
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        if data == []:
            return False
        return True
    except Exception as e:
        print(f"An error occurred: {e}")


def cool_outfit(json_obj, user_id):
    """
    either summer outfit with long sleeves- or short sleeves and a jacket
    :return: outfit id
    """
    date = datetime.now().date()
    again = 1
    options = ["skirts", "pants", "Dresses"]
    while again == 1:
        top = []
        bottom = []
        while top == [] or bottom == []:
            clothing_type = chooseOutfitType(options)
            if clothing_type != "Dresses":
                top = get_top(["shirts"], ["hot", "warm"], ["light", "medium"], ["short sleeves"])
                bottom = get_bottom([clothing_type], ["hot", "warm"], ["light", "medium"], ["knee length", "long"])
                # if bottom == []:
                #     options.remove(clothing_type)
            else:
                top = get_dress([clothing_type], ["hot", "warm"], ["light", "medium"], ["short sleeves", "long"], ["knee length", "long"])
                bottom = [None]
                # if top == []:
                #     options.remove(clothing_type)
        shoes = get_random_item("Footwear", ["hot", "warm"])
        if shoes == []:
            shoes = [None]
        if is_type_sleeves(top[0], "short sleeves"):
            outwear = get_random_item("outwear", "warm")
            if outwear == []:
                outwear = [None]
        else:
            outwear = [None]
        check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
        if check == []:
            add_outfit(user_id, top[0], bottom[0], outwear[0], shoes[0])
            check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
            return check[0][1]

        elif (check[0][0] - date).days < wear_again_range:
            again = 1
        else:
            return check[1]


def colder_outfit(json_obj, user_id):
    """
       either cool weather with long sleeves or  for warm weather with a jacket
       :return: outfit id
       """
    date = datetime.now().date()
    again = 1
    options = ["skirts", "pants", "Dresses"]
    while again == 1:
        top = []
        bottom = []
        while top == [] or bottom == []:
            clothing_type = chooseOutfitType(options)
            if clothing_type != "Dresses":
                top = get_top(["shirts"], ["warm", "cool"], ["medium", "heavy"], ["long sleeves"])
                bottom = get_bottom([clothing_type], ["warm", "cool"], ["medium", "heavy"], ["long"])
                if bottom == []:
                    options.remove(clothing_type)
            else:
                top = get_dress([clothing_type], ["warm", "cool"], ["medium", "heavy"], ["long sleeves"],
                                ["long"])
                bottom = [None]
                if top == []:
                    options.remove(clothing_type)
        shoes = get_random_item(["Footwear"], ["warm", "cool"])
        if shoes == []:
            shoes = [None]
        if is_type_weather(top[0], "warm"):
            outwear = get_random_item(["outwear"], ["cool"])
            if outwear == []:
                outwear = [None]
        else:
            outwear = [None]
        check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
        if check == []:
            add_outfit(user_id, top[0], bottom[0], outwear[0], shoes[0])
            check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
            return check[0][1]

        elif (check[0][0] - date).days < wear_again_range:
            again = 1
        else:
            return check[1]


# todo:
def winter_outfit(json_obj, user_id):
    """
       get cold weather outfit and coat
       :return: outfit id
       """
    date = datetime.now().date()
    again = 1
    options = ["skirts", "pants", "Dresses"]
    while again == 1:
        top = []
        bottom = []
        while top == [] or bottom == []:
            clothing_type = chooseOutfitType(options)
            if clothing_type != "Dresses":
                top = get_top(["shirts"], ["cold"], ["heavy"], ["long sleeves"])
                bottom = get_bottom([clothing_type], ["cold"], ["heavy"], ["long"])
                if bottom == []:
                    options.remove(clothing_type)
            else:
                top = get_dress([clothing_type], ["cold"], ["heavy"], ["long sleeves"], ["long"])
                bottom = [None]
                if top == []:
                    options.remove(clothing_type)
        shoes = get_random_item(["Footwear"], ["cold"])
        if shoes == []:
            shoes = [None]
        outwear = get_random_item(["outwear"], ["cold"])
        check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
        if check == []:
            add_outfit(user_id, top[0], bottom[0], outwear[0], shoes[0])
            check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
            return check[0][1]

        elif (check[0][0] - date).days < wear_again_range:
            again = 1
        else:
            return check[1]


# todo:
def getOutfit(json_obj, user_id):
    """
    gets weahter and decides what kind of outfit to generate
    :param json_obj:
    :param user_id:
    :return:
    """
    temperature = getWeather(json_obj)
    user_thresholds = get_users_thresholds(user_id)
    hot_threshold = int(user_thresholds[0][0])
    warm_threshold = int(user_thresholds[0][1])
    cool_threshold = int(user_thresholds[0][2])
    if temperature >= hot_threshold:
        outfit_id = summer_outfit(json_obj, user_id)

    elif warm_threshold <= temperature <= hot_threshold:
        outfit_id = cool_outfit(json_obj, user_id)
    elif warm_threshold <= temperature <= cool_threshold:
        outfit_id = colder_outfit(json_obj, user_id)
    else:
        outfit_id = winter_outfit(json_obj, user_id)
    return get_outfit_by_id(outfit_id)


def change_threshold(threshold_to_change, val, user_id):
    # UPDATE user
    # SET threshold = <new_threshold_value>
    # WHERE user_id = <your_user_id>;
    try:

        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()
        sql = "UPDATE user SET %s = %s WHERE user_id = %s"
        val = (threshold_to_change, val, user_id)
        cursordb.execute(sql, val)
        db.commit()
        cursordb.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")


def too_hot(hot_threshold, warm_threshold, cool_threshold, temperature, user_id):
    if temperature >= hot_threshold:
        pass
    elif warm_threshold <= temperature < hot_threshold:
        change_threshold("hot_threshold", hot_threshold - 2, user_id)
    elif cool_threshold <= temperature < warm_threshold:
        change_threshold("warm_threshold", warm_threshold - 2, user_id)
    elif temperature < cool_threshold:
        change_threshold("cool_threshold", cool_threshold - 2, user_id)


def too_cold(hot_threshold, warm_threshold, cool_threshold, user_id):
    if temperature >= hot_threshold:
        change_threshold("hot_threshold", hot_threshold + 2, user_id)
    elif warm_threshold <= temperature < hot_threshold:
        change_threshold("warm_threshold", warm_threshold + 2, user_id)
    elif cool_threshold <= temperature < warm_threshold:
        change_threshold("cool_threshold", cool_threshold + 2, user_id)
    elif temperature < cool_threshold:
        pass


def change_temp_thresholds(json_obj, user_id, stars, feedback):
    temperature = getWeather(json_obj)
    hot_threshold, warm_threshold, cool_threshold = get_users_thresholds(user_id)
    if feedback == "too hot":
        too_hot(hot_threshold, warm_threshold, cool_threshold,temperature, user_id)
    elif feedback == "too cold":
        too_cold(hot_threshold, warm_threshold, cool_threshold, temperature, user_id)

from flask import Flask, jsonify, request, render_template
import requests
import functions


# def temperature():
#     longitude = "34"
#     latitude = "32"
#     r = requests.get(
#         'https://api.openweathermap.org/data/2.5/weather?lat=' + latitude + '.34&lon=' + longitude + '.99&appid=8f3241a0140c7cbf04fd85bcb7b1cef9')
#     json_obj = r.json()
#     # generate outfit
#     outfit = getOutfit(json_obj, 1)
#     print(outfit)
#     temp_k = float(json_obj['main']['temp'])
#     temp_c = temp_k - 273.15  # convert to celsius
#     return temp_c
#
#
# if __name__ == '__main__':
#     temperature()
#     #print(get_outfit_by_id(26))

def temperature():
    longitude = request.json.get('longitude')
    latitude = request.json.get('latitude')
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?lat='+latitude+'.34&lon='+longitude+'.99&appid=8f3241a0140c7cbf04fd85bcb7b1cef9')
    json_obj = r.json()
    # temp_k = float(json_obj['main']['temp'])
    # temp_c = temp_k-273.15 # convert to celsius
    return json_obj
# def temperature(latitude, longitude):
#     longitude1 = str(int(round(float(longitude))))
#     latitude1 = str(int(round(float(latitude))))
#     r = requests.get(
#         'https://api.openweathermap.org/data/2.5/weather?lat=' + latitude1 + '&lon=' + longitude1 + '&appid=8f3241a0140c7cbf04fd85bcb7b1cef9')
#     json_obj = r.json()
#     # generate outfit
#     outfit = getOutfit(json_obj,1 )
#     print(outfit)
#     temp_k = float(json_obj['main']['temp'])
#     temp_c = temp_k - 273.15  # convert to celsius
#     return temp_c
#
#
# if __name__ == '__main__':
#     # temperature()
#     print(get_outfit_by_id(26))

def temperature(latitude, longitude):
    longitude1 = str(int(round(float(longitude))))
    latitude1 = str(int(round(float(latitude))))
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + latitude1 + '&lon=' + longitude1 + '&appid=8f3241a0140c7cbf04fd85bcb7b1cef9')
    json_obj = r.json()
    # temp_k = float(json_obj['main']['temp'])
    # temp_c = temp_k-273.15 # convert to celsius
    return json_obj
