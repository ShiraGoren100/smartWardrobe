import mysql.connector
import random
from datetime import datetime
import requests

wear_again_range = 2


def get_users_thresholds(user_id):
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",    port=3307)
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
    random_choice = random.choice(options)
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


def shoes_for_hot(data):
    if data[4] == 'cold':
        return False
    else:
        return True


def shoes_for_cool(data):
    if data[4] == 'hot':
        return False
    else:
        return True


def shoes_fit_weather(weather, data):
    if weather == 'hot':
        return shoes_for_hot(data)
    if weather == 'warm':
        return shoes_for_hot(data)
    if weather == 'cool':
        return shoes_for_cool(data)
    if weather == 'cold':
        return shoes_for_cool(data)


def get_shoes_item(type, weather):
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
            "AND t_weather.tag_name = 'weather';",
            [type]
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


def add_outfit(user_id, top, bottom, outwear, shoes, temperature):
    """
    add outfit to db
    """
    date = datetime.now()
    date_string = date.strftime("%Y-%m-%d")
    try:

        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()
        sql = "INSERT INTO outfits (top, bottom, outwear, shoes, last_used, user_id, temperature) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (top, bottom, outwear, shoes, date_string, user_id, temperature)
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
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

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
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

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


def set_days_interval(user_id, val):
    try:

        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()
        sql = "UPDATE user SET days_interval = %s WHERE id = %s"
        val = (val, user_id)
        cursordb.execute(sql, val)
        db.commit()
        cursordb.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def get_days_interval(user_id):
    """
      returns the days user wants between re-wearing outfit
    """
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)

        cursordb = db.cursor()
        cursordb.execute("SELECT days_interval "
                         "FROM user WHERE id = %s;", ([user_id]))
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data[0]
    except Exception as e:
        print(f"An error occurred: {e}")

def get_outfit_by_weather(user_id, weather, temperature):
    """
    :return: outfit id
    """

    date = datetime.now().date()
    again = 0
    options = ["skirts", "pants", "Dresses"]
    while again != 4:
        top = []
        bottom = []
        while top == [] or bottom == []:
            clothing_type = chooseOutfitType(options)
            if clothing_type != "Dresses":
                top = get_top_item("shirts", weather)
                bottom = get_bottom_item(clothing_type, weather)
                if bottom == [] or top == []:
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
            add_outfit(user_id, top[0], bottom[0], outwear[0], shoes[0], temperature)
            check = check_outfit(user_id, top[0], bottom[0], shoes[0])
            return check[0][1]

        elif (date - check[0][0]).days < get_days_interval(user_id):
            again += 1
        else:
            return check[0][1]
    error_message = "not enough items for outfit interval"
    return error_message


def is_type_sleeves(top_id, sleeve_type):
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

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
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()

        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category "
            "FROM clothing_item ci JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci ON tci.clothing_item_id = ci.id "
            "JOIN tags t ON t.id = tci.tag_id WHERE ci.id = %s "
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


# todo:
def getOutfit(json_obj, user_id):
    """
    gets weather and decides what kind of outfit to generate
    :return: list with a tuple holding all info of outfit
    """
    temperature = int(getWeather(json_obj))
    user_thresholds = get_users_thresholds(user_id)
    hot_threshold = int(user_thresholds[0][0])
    warm_threshold = int(user_thresholds[0][1])
    cool_threshold = int(user_thresholds[0][2])
    if temperature >= hot_threshold:
        outfit_id = get_outfit_by_weather(user_id, 'hot', temperature)

    elif warm_threshold <= temperature <= hot_threshold:
        outfit_id = get_outfit_by_weather(user_id, 'warm', temperature)
    elif warm_threshold <= temperature <= cool_threshold:
        outfit_id = get_outfit_by_weather(user_id, 'cool', temperature)
    else:
        outfit_id = get_outfit_by_weather(user_id, 'cold', temperature)
    if not isinstance(outfit_id, int):
        return outfit_id
    return get_outfit_by_id(outfit_id)


def change_threshold(threshold_to_change, val, user_id):
    try:

        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()
        if threshold_to_change == 'hot':
            sql = "UPDATE user SET hot = %s WHERE id = %s"
        elif threshold_to_change == 'warm':
            sql = "UPDATE user SET warm = %s WHERE id = %s"
        else:
            sql = "UPDATE user SET cool = %s WHERE id = %s"
        val = (val, user_id)
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
        change_threshold('hot', hot_threshold - 2, user_id)
    elif cool_threshold <= temperature < warm_threshold:
        change_threshold('warm', warm_threshold - 2, user_id)
    elif temperature < cool_threshold:
        change_threshold('cool', cool_threshold - 2, user_id)


def too_cold(hot_threshold, warm_threshold, cool_threshold, temperature, user_id):

    if temperature >= hot_threshold:
        change_threshold('hot', hot_threshold + 2, user_id)
    elif warm_threshold <= temperature < hot_threshold:
        change_threshold('warm', warm_threshold + 2, user_id)
    elif cool_threshold <= temperature < warm_threshold:
        change_threshold('cool', cool_threshold + 2, user_id)
    elif temperature < cool_threshold:
        pass


def get_outfit_temperature(outfit_id):
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)

        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute("SELECT temperature "
                         "FROM outfits WHERE id = %s;"
                         , (outfit_id,))
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data[0]
    except Exception as e:
        print(f"An error occurred: {e}")


def change_temp_thresholds(user_id, outfit_id, feedback):
    temperature = get_outfit_temperature(outfit_id)[0]
    user_thresholds = get_users_thresholds(user_id)
    hot_threshold = int(user_thresholds[0][0])
    warm_threshold = int(user_thresholds[0][1])
    cool_threshold = int(user_thresholds[0][2])
    if feedback == "too hot":
        too_hot(hot_threshold, warm_threshold, cool_threshold, temperature, user_id)
    elif feedback == "too cold":
        too_cold(hot_threshold, warm_threshold, cool_threshold, temperature, user_id)


def temperature(latitude, longitude):
    longitude1 = str(int(round(float(longitude))))
    latitude1 = str(int(round(float(latitude))))
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + latitude1 + '&lon=' + longitude1 + '&appid=8f3241a0140c7cbf04fd85bcb7b1cef9')
    json_obj = r.json()
    return json_obj


def delete_outfit(outfit_id):
    try:

       # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()
        sql = "DELETE FROM outfits WHERE id = %s;"
        val = (outfit_id)
        cursordb.execute(sql, val)
        db.commit()
        cursordb.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")


def regenerate(json_obj, user_id, outfit_id):
    delete_outfit(outfit_id)
    return getOutfit(json_obj, user_id)
