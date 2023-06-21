import mysql.connector
import random
from datetime import datetime
from flask import Flask, jsonify, request, render_template
import requests
import functions

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
#
# cool_threshold = 18
# warm_threshold = 24
# cold_threshold = 14
wear_again_range = 2


def get_users_thresholds(user_id):
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute("SELECT hot, warm, cool FROM user WHERE id = %s;", [user_id])
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
    return temp_c


def is_item_for_hot(data):
    if data[4] == 'cool' or data[4] == 'cold' or data[5] == 'long sleeves' or data[6] == 'heavy':
        return False
    else:
        return True


def is_item_for_warm(data):
    if data[6] == 'heavy':
        return False
    else:
        return True


def is_item_for_cool(data):
    if data[6] == 'short':
        return False
    else:
        return True


def is_item_for_cold(data):
    if data[6] == 'knee length' or data[6] == 'short':
        return False
    else:
        return True


def check_if_fits_weather(weather, data):
    if weather == 'hot':
        return is_item_for_hot(data)
    if weather == 'warm':
        return is_item_for_warm(data)
    if weather == 'cool':
        return is_item_for_cool(data)
    if weather == 'cold':
        return is_item_for_cold(data)


def get_shoes_item(type, weather):
    """
       returns random clothing item that is of 'type' footwear
        and of requested weather
       :return: a list of an item tas requested
       """
    valid = False
    random_choice = []
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category, "
            "tci_weather.tag_value AS weather "
            "FROM clothing_item ci "
            "JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
            "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
            "WHERE c.type = %s "
            "AND t_weather.tag_name = 'weather';",
            [type]
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


def get_top_item(type, weather):
    """
       returns random clothing item that is of 'type'
        category  that is a top (shirt)
        and check if fits weather
       :param type:
       :param weather:
       :return:
       """
    valid = False
    random_choice = []
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category, "
            "tci_weather.tag_value AS weather, "
            "tci_sleeves.tag_value AS sleeves, "
            "tci_thickness.tag_value AS thickness "
            "FROM clothing_item ci "
            "JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_sleeves ON tci_sleeves.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_thickness ON tci_thickness.clothing_item_id = ci.id "
            "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
            "JOIN tags t_sleeves ON t_sleeves.id = tci_sleeves.tag_id "
            "JOIN tags t_thickness ON t_thickness.id = tci_thickness.tag_id "
            "WHERE c.type = %s "
            "AND t_weather.tag_name = 'weather' "
            "AND t_sleeves.tag_name = 'sleeves' "
            "AND t_thickness.tag_name = 'thickness';",
            [type]
        )
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        # check if top fits weather
        while not valid:
            if data == []:
                return data
            random_choice = random.choice(data)
            valid = check_if_fits_weather(weather, random_choice)
            if not valid:
                data.remove(random_choice)
                random_choice = random.choice(data)
        return random_choice
    except Exception as e:
        print(f"An error occurred: {e}")


def get_bottom_item(type, weather):
    """
       returns random clothing item that is of 'type'
        category  that is a bottom (skirt or pants)
        and fits weather
       """
    valid = False
    random_choice = []
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category, "
            "tci_weather.tag_value AS weather, "
            "tci_length.tag_value AS length, "
            "tci_thickness.tag_value AS thickness "
            "FROM clothing_item ci "
            "JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_length ON tci_length.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_thickness ON tci_thickness.clothing_item_id = ci.id "
            "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
            "JOIN tags t_length ON t_length.id = tci_length.tag_id "
            "JOIN tags t_thickness ON t_thickness.id = tci_thickness.tag_id "
            "WHERE c.type = %s "
            "AND t_weather.tag_name = 'weather' "
            "AND t_length.tag_name = 'length' "
            "AND t_thickness.tag_name = 'thickness';",
            [type]
        )
        data = cursordb.fetchall()
        cursordb.close()
        db.close()

        while not valid:
            if data == []:
                return data
            random_choice = random.choice(data)
            valid = check_if_fits_weather(weather, random_choice)
            if not valid:
                data.remove(random_choice)
                random_choice = random.choice(data)
        return random_choice
    except Exception as e:
        print(f"An error occurred: {e}")


def get_dress_item(type, weather):
    """
       returns random clothing item that is of 'type'
        category  that is a dress
       """
    valid = False
    random_choice = []
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category, "
            "tci_weather.tag_value AS weather, "
            "tci_sleeves.tag_value AS sleeves, "
            "tci_thickness.tag_value AS thickness "
            "tci_length.tag_value AS length, "
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
            "AND t_weather.tag_name = 'weather' "
            "AND t_length.tag_name = 'length' "
            "AND t_sleeves.tag_name = 'sleeves' "
            "AND t_thickness.tag_name = 'thickness';",
            [type]
        )
        data = cursordb.fetchall()
        cursordb.close()
        db.close()

        while not valid:
            if data == []:
                return data
            random_choice = random.choice(data)
            valid = check_if_fits_weather(weather, random_choice)
            if not valid:
                data.remove(random_choice)
                random_choice = random.choice(data)
        return random_choice
    except Exception as e:
        print(f"An error occurred: {e}")


# def get_top(type, weather, thickness, sleeves):
#     """
#        returns random clothing item that is of 'type'
#         category  that is a top (shirt)
#         and of requested weather, thickness and length
#        :param type:
#        :param weather:
#        :return:
#        """
#     random_type = random.choice(type)
#     random_weather = random.choice(weather)
#     random_thickness = random.choice(thickness)
#     random_sleeves = random.choice(sleeves)
#
#     try:
#         # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
#         db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
#                                      port=3307)
#         cursordb = db.cursor()
#         cursordb.execute(
#             "SELECT ci.id, ci.picture, ci.user_id, ci.category "
#             "FROM clothing_item ci "
#             "JOIN categories c ON ci.category = c.id "
#             "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
#             "JOIN tags_clothing_item tci_sleeves ON tci_sleeves.clothing_item_id = ci.id "
#             "JOIN tags_clothing_item tci_thickness ON tci_thickness.clothing_item_id = ci.id "
#             "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
#             "JOIN tags t_sleeves ON t_sleeves.id = tci_sleeves.tag_id "
#             "JOIN tags t_thickness ON t_thickness.id = tci_thickness.tag_id "
#             "WHERE c.type = %s "
#             "AND t_weather.tag_name = 'weather' AND tci_weather.tag_value = %s "
#             "AND t_sleeves.tag_name = 'sleeves' AND tci_sleeves.tag_value = %s "
#             "AND t_thickness.tag_name = 'thickness' AND tci_thickness.tag_value = %s;",
#             [random_type, random_weather, random_sleeves, random_thickness]
#         )
#         data = cursordb.fetchall()
#         cursordb.close()
#         db.close()
#         if data == []:
#             return data
#         random_choice = random.choice(data)
#         return random_choice
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#
# def get_bottom(type, weather, thickness, length):
#     """
#     returns random clothing item that is of 'type'
#      category  that is a bottom (pants or skirt)
#      and of requested weather, thickness and length
#     :param type:
#     :param weather:
#     :return:
#     """
#     random_type = random.choice(type)
#     random_weather = random.choice(weather)
#     random_thickness = random.choice(thickness)
#     random_length = random.choice(length)
#     try:
#         # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
#         db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
#                                      port=3307)
#         cursordb = db.cursor()
#
#         # get all clothing items that are classified as summer.
#         cursordb.execute(
#             "SELECT ci.id, ci.picture, ci.user_id, ci.category "
#             "FROM clothing_item ci "
#             "JOIN categories c ON ci.category = c.id "
#             "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
#             "JOIN tags_clothing_item tci_length ON tci_length.clothing_item_id = ci.id "
#             "JOIN tags_clothing_item tci_thickness ON tci_thickness.clothing_item_id = ci.id "
#             "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
#             "JOIN tags t_length ON t_length.id = tci_length.tag_id "
#             "JOIN tags t_thickness ON t_thickness.id = tci_thickness.tag_id "
#             "WHERE c.type = %s "
#             "AND t_weather.tag_name = 'weather' AND tci_weather.tag_value = %s "
#             "AND t_length.tag_name = 'length' AND tci_length.tag_value = %s "
#             "AND t_thickness.tag_name = 'thickness' AND tci_thickness.tag_value = %s;"
#             , [random_type, random_weather, random_length, random_thickness])
#         data = cursordb.fetchall()
#         cursordb.close()
#         db.close()
#         if data == []:
#             return data
#         random_choice = random.choice(data)
#         return random_choice
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#
# def get_dress(type, weather, thickness, sleeves, length):
#     """
#     returns random clothing item that is of 'type'
#      category  that is a dress
#      and of requested weather, thickness sleeves and length
#     :param type:
#     :param weather:
#     :return:
#     """
#     random_type = random.choice(type)
#     random_weather = random.choice(weather)
#     random_thickness = random.choice(thickness)
#     random_sleeves = random.choice(sleeves)
#     random_length = random.choice(length)
#     try:
#         # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
#         db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
#                                      port=3307)
#         cursordb = db.cursor()
#
#         # get all clothing items that are classified as summer.
#         cursordb.execute(
#             "SELECT ci.id, ci.picture, ci.user_id, ci.category "
#             "FROM clothing_item ci "
#             "JOIN categories c ON ci.category = c.id "
#             "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
#             "JOIN tags_clothing_item tci_sleeves ON tci_sleeves.clothing_item_id = ci.id "
#             "JOIN tags_clothing_item tci_length ON tci_length.clothing_item_id = ci.id "
#             "JOIN tags_clothing_item tci_thickness ON tci_thickness.clothing_item_id = ci.id "
#             "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
#             "JOIN tags t_sleeves ON t_sleeves.id = tci_sleeves.tag_id "
#             "JOIN tags t_length ON t_length.id = tci_length.tag_id "
#             "JOIN tags t_thickness ON t_thickness.id = tci_thickness.tag_id "
#             "WHERE c.type = %s "
#             "AND t_weather.tag_name = 'weather' AND tci_weather.tag_value = %s "
#             "AND t_length.tag_name = 'length' AND tci_length.tag_value = %s "
#             "AND t_sleeves.tag_name = 'sleeves' AND tci_sleeves.tag_value = %s "
#             "AND t_thickness.tag_name = 'thickness' AND tci_thickness.tag_value = %s;"
#             , [random_type, random_weather, random_length, random_sleeves, random_thickness])
#         data = cursordb.fetchall()
#         cursordb.close()
#         db.close()
#         if data == []:
#             return data
#         random_choice = random.choice(data)
#         return random_choice
#     except Exception as e:
#         print(f"An error occurred: {e}")

# def get_random_item(type, weather):
#     """
#     returns random clothing item that is of 'type'
#      category and of requested weather
#     :param type:
#     :param weather:
#     :return:
#     """
#     random_type = random.choice(type)
#     random_weather = random.choice(weather)
#     try:
#         # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
#         db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
#                                      port=3307)
#         cursordb = db.cursor()
#
#         # get all clothing items that are classified as summer.
#         cursordb.execute(
#             "SELECT ci.id, ci.picture, ci.user_id, ci.category "
#             "FROM clothing_item ci JOIN categories c ON ci.category = c.id "
#             "JOIN tags_clothing_item tci ON tci.clothing_item_id = ci.id "
#             "JOIN tags t ON t.id = tci.tag_id WHERE c.type= %s"
#             "AND t.tag_name = 'weather'"
#             "AND tci.tag_value = %s", [random_type, random_weather])
#         data = cursordb.fetchall()
#         cursordb.close()
#         db.close()
#         if data == []:
#             return data
#         random_choice = random.choice(data)
#         return random_choice
#     except Exception as e:
#         print(f"An error occurred: {e}")


def add_outfit(user_id, top, bottom, outwear, shoes):
    """
    add outfit to db
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


def check_outfit(user_id, top, bottom, shoes):
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


def get_jacket(thickness):
    """
     returns jacket based on weather and top chosen
     """
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1",
                                     database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category, "
            "tci_weather.tag_value AS weather, "
            "tci_sleeves.tag_value AS sleeves, "
            "tci_thickness.tag_value AS thickness "
            "tci_length.tag_value AS length, "
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
            "WHERE c.type = 'outwear' "
            "AND t_weather.tag_name = 'weather' "
            "AND t_thickness.tag_name = 'thickness'"
            " AND tci_thickness.tag_value = %s;"
            ";",
            [thickness]
        )
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        if data == []:
            return [None]
        random_choice = random.choice(data)
        return random_choice
    except Exception as e:
        print(f"An error occurred: {e}")


def get_outwear(top, weather):
    """
    returns outwear for outfit
    :param top:
    :param weather:
    :return:
    """
    if weather == 'hot':
        return [None]
    if weather == 'warm':
        if top[6] == 'light':
            # get a light jacket
            return get_jacket('light')
        else:
            return [None]
    if weather == 'cool':
        if top[6] == 'light':
            return get_jacket('heavy')
        if top[6] == 'medium':
            return get_jacket('medium')
        if top[6] == 'heavy':
            return [None]
    if weather == 'cold':
        return get_jacket('heavy')


def get_outfit_by_weather(user_id, weather):
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
                top = get_top_item("shirts", weather)
                bottom = get_bottom_item(clothing_type, weather)
                if bottom == [] or top== []:
                    options.remove(clothing_type)
            else:
                top = get_dress_item(clothing_type, weather)
                bottom = [None]
                if top == [] or top == None:
                    options.remove(clothing_type)
                    top = []
        shoes = get_shoes_item("Footwear", weather)
        if shoes == []:
            shoes = [None]
        outwear = get_outwear(top, weather)
        check = check_outfit(user_id, top[0], bottom[0], shoes[0])
        if check == []:
            add_outfit(user_id, top[0], bottom[0], outwear[0], shoes[0])
            check = check_outfit(user_id, top[0], bottom[0], shoes[0])
            return check[0][1]

        elif (date - check[0][0]).days < wear_again_range:
            again = 1
        else:
            return check[0][1]


def is_type_sleeves(top_id, sleeve_type):
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
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
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
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


# def cool_outfit(json_obj, user_id):
#     """
#     either summer outfit with long sleeves- or short sleeves and a jacket
#     :return: outfit id
#     """
#     date = datetime.now().date()
#     again = 1
#     while again == 1:
#         top = []
#         bottom = []
#         while top == [] or bottom == []:
#             clothing_type = chooseOutfitType(json_obj)
#             if clothing_type != "dress":
#                 top = get_top(["shirts"], ["hot", "warm"], ["light", "medium"], ["short sleeves"])
#                 bottom = get_bottom([clothing_type], ["hot", "warm"], ["light", "medium"], ["knee length", "long"])
#
#             else:
#                 top = get_dress([clothing_type], ["hot", "warm"], ["light", "medium"], ["short sleeves", "long"], ["knee length", "long"])
#                 bottom = [None]
#         shoes = get_random_item("Footwear", ["hot", "warm"])
#         if is_type_sleeves(top[0], "short sleeves"):
#             outwear = get_random_item("outwear", "warm")
#             if outwear == []:
#                 outwear = [None]
#         else:
#             outwear = [None]
#         check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
#         if check == []:
#             add_outfit(user_id, top[0], bottom[0], outwear[0], shoes[0])
#             check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
#             return check[0][1]
#
#         elif (check[0][0] - date).days < wear_again_range:
#             again = 1
#         else:
#             return check[1]
#
#
# def colder_outfit(json_obj, user_id):
#     """
#        either cool weather with long sleeves or  for warm weather with a jacket
#        :return: outfit id
#        """
#     date = datetime.now().date()
#     again = 1
#     while again == 1:
#         top = []
#         bottom = []
#         while top == [] or bottom == []:
#             clothing_type = chooseOutfitType(json_obj)
#             if clothing_type != "dress":
#                 top = get_top(["shirts"], ["warm", "cool"], ["medium", "heavy"], ["long sleeves"])
#                 bottom = get_bottom([clothing_type], ["warm", "cool"], ["medium", "heavy"], ["long"])
#
#             else:
#                 top = get_dress([clothing_type], ["warm", "cool"], ["medium", "heavy"], ["long sleeves"],
#                                 ["long"])
#                 bottom = [None]
#         shoes = get_random_item(["Footwear"], ["warm", "cool"])
#         if is_type_weather(top[0], "warm"):
#             outwear = get_random_item(["outwear"], ["cool"])
#             if outwear == []:
#                 outwear = [None]
#         else:
#             outwear = [None]
#         check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
#         if check == []:
#             add_outfit(user_id, top[0], bottom[0], outwear[0], shoes[0])
#             check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
#             return check[0][1]
#
#         elif (check[0][0] - date).days < wear_again_range:
#             again = 1
#         else:
#             return check[1]
#
#
# # todo:
# def winter_outfit(json_obj, user_id):
#     """
#        get cold weather outfit and coat
#        :return: outfit id
#        """
#     date = datetime.now().date()
#     again = 1
#     while again == 1:
#         top = []
#         bottom = []
#         while top == [] or bottom == []:
#             clothing_type = chooseOutfitType(json_obj)
#             if clothing_type != "dress":
#                 top = get_top(["shirts"], ["cold"], ["heavy"], ["long sleeves"])
#                 bottom = get_bottom([clothing_type], ["cold"], ["heavy"], ["long"])
#
#             else:
#                 top = get_dress([clothing_type], ["cold"], ["heavy"], ["long sleeves"], ["long"])
#                 bottom = [None]
#         shoes = get_random_item(["Footwear"], ["cold"])
#         outwear = get_random_item(["outwear"], ["cold"])
#         check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
#         if check == []:
#             add_outfit(user_id, top[0], bottom[0], outwear[0], shoes[0])
#             check = checkOutfit(user_id, top[0], bottom[0], shoes[0])
#             return check[0][1]
#
#         elif (check[0][0] - date).days < wear_again_range:
#             again = 1
#         else:
#             return check[1]


# todo:
def getOutfit(json_obj, user_id):
    """
    gets weather and decides what kind of outfit to generate
    :return: list with a tuple holding all info of outfit
    """
    temperature = getWeather(json_obj)
    user_thresholds = get_users_thresholds(user_id)
    hot_threshold = int(user_thresholds[0][0])
    warm_threshold = int(user_thresholds[0][1])
    cool_threshold = int(user_thresholds[0][2])
    if temperature >= hot_threshold:
        outfit_id = get_outfit_by_weather(user_id, 'hot')

    elif warm_threshold <= temperature <= hot_threshold:
        outfit_id = get_outfit_by_weather(user_id, 'warm')
    elif warm_threshold <= temperature <= cool_threshold:
        outfit_id = get_outfit_by_weather(user_id, 'cool')
    else:
        outfit_id = get_outfit_by_weather(user_id, 'cold')
    return get_outfit_by_id(outfit_id)


def change_threshold(threshold_to_change, val, user_id):
    # UPDATE user
    # SET threshold = <new_threshold_value>
    # WHERE user_id = <your_user_id>;
    try:

        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
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

def temperature(latitude, longitude):
    longitude1 = str(int(round(float(longitude))))
    latitude1 = str(int(round(float(latitude))))
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + latitude1 + '&lon=' + longitude1 + '&appid=8f3241a0140c7cbf04fd85bcb7b1cef9')
    json_obj = r.json()
    return json_obj