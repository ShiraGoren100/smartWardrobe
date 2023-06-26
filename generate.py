import random
from datetime import datetime
from closet import get_outfit_by_id, check_outfit, get_jacket, add_outfit, delete_outfit
from outfit_generateor import get_top_item, get_bottom_item, get_dress_item, get_shoes_item
from user_file import get_users_thresholds, get_days_interval, change_threshold
from weather_file import get_weather


def choose_outfit_type(options):
    """
    choose outfit type
    :param options: lost of options of outfit types-dress\skirt\pants ect.
    :return:randomly chosen option
    """
    random_choice = random.choice(options)
    return random_choice





def chooseOutfitType(options):
    pass


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


# def is_type_sleeves(top_id, sleeve_type):
#     try:
#         #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
#         db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
#
#         cursordb = db.cursor()
#
#         cursordb.execute(
#             "SELECT ci.id, ci.picture, ci.user_id, ci.category "
#             "FROM clothing_item ci JOIN categories c ON ci.category = c.id "
#             "JOIN tags_clothing_item tci ON tci.clothing_item_id = ci.id "
#             "JOIN tags t ON t.id = tci.tag_id WHERE ci.id = %s"
#             "AND t.tag_name ='sleeves'"
#             "AND tci.tag_value = %s", [top_id, sleeve_type])
#         data = cursordb.fetchall()
#         cursordb.close()
#         db.close()
#         if data == []:
#             return False
#         return True
#     except Exception as e:
#         print(f"An error occurred: {e}")


# def is_type_weather(clothing_id, weather_type):
#     try:
#         #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
#         db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
#
#         cursordb = db.cursor()
#
#         cursordb.execute(
#             "SELECT ci.id, ci.picture, ci.user_id, ci.category "
#             "FROM clothing_item ci JOIN categories c ON ci.category = c.id "
#             "JOIN tags_clothing_item tci ON tci.clothing_item_id = ci.id "
#             "JOIN tags t ON t.id = tci.tag_id WHERE ci.id = %s "
#             "AND t.tag_name ='sleeves'"
#             "AND tci.tag_value = %s", [clothing_id, weather_type])
#         data = cursordb.fetchall()
#         cursordb.close()
#         db.close()
#         if data == []:
#             return False
#         return True
#     except Exception as e:
#         print(f"An error occurred: {e}")


# todo:
def get_outfit(json_obj, user_id):
    """
    gets weather and decides what kind of outfit to generate
    :return: list with a tuple holding all info of outfit
    """
    temperature = int(get_weather(json_obj))
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


def regenerate(json_obj, user_id, outfit_id):
    delete_outfit(outfit_id)
    return get_outfit(json_obj, user_id)


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