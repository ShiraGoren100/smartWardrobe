from random import random
import mysql
import random

import closet
from weather_file import shoes_fit_weather, check_if_fits_weather


def get_shoes_item(type, weather, user_id):
    """
       returns random clothing item that is of 'type' footwear
        and of requested weather
       :return: a list of an item tas requested
       """
    valid = False
    random_choice = []
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category, "
            "tci_weather.tag_value AS weather "
            "FROM clothing_item ci "
            "JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
            "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
            "WHERE c.type = %s "
            "AND t_weather.tag_name = 'weather' "
            "AND ci.user_id = %s;",
            [type, user_id]
        )
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        while not valid:
            if data == []:
                return data
            random_choice = random.choice(data)
            valid = shoes_fit_weather(weather, random_choice)
            if not valid:
                data.remove(random_choice)
                random_choice = random.choice(data)
        return random_choice
    except Exception as e:
        print(f"An error occurred: {e}")



def get_top_item(type, weather, user_id):
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
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
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
            "AND t_thickness.tag_name = 'thickness' "
            "AND ci.user_id = %s;",
            [type, user_id]
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

def get_bottom_item(type, weather, user_id):
    """
       returns random clothing item that is of 'type'
        category  that is a bottom (skirt or pants)
        and fits weather
       """
    valid = False
    random_choice = []
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
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
            "AND t_thickness.tag_name = 'thickness' "
            "AND ci.user_id = %s;",
            [type, user_id]
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


def get_dress_item(type, weather, user_id):
    """
       returns random clothing item that is of 'type'
        category  that is a dress
       """
    valid = False
    random_choice = []
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
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
            "AND t_thickness.tag_name = 'thickness' "
            "AND ci.user_id = %s;",
            [type, user_id]
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


def get_jacket(thickness, user_id, type):
    """
     returns jacket based on weather and top chosen
     """
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

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
            "AND t_thickness.tag_name = 'thickness'"
            " AND tci_thickness.tag_value = %s "
            "AND ci.user_id = %s;"
            ";",
            [type, thickness, user_id]
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
