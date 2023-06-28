import random
from datetime import datetime
from closet import get_outfit_by_id, check_outfit, add_outfit, delete_outfit
from outfit_generateor import get_top_item, get_bottom_item, get_dress_item, get_shoes_item, get_jacket
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
            clothing_type = choose_outfit_type(options)
            if clothing_type != "Dresses":
                top = get_top_item("shirts", weather, user_id)
                bottom = get_bottom_item(clothing_type, weather, user_id)
                if bottom == [] or top == []:
                    options.remove(clothing_type)
            else:
                top = get_dress_item(clothing_type, weather, user_id)
                bottom = [None]
                if top == [] or top == None:
                    options.remove(clothing_type)
                    top = []
        shoes = get_shoes_item("Footwear", weather, user_id)
        if shoes == []:
            shoes = [None]
        outwear = get_outwear(top, weather, user_id)
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


def get_outwear(top, weather, user_id):
    """
    returns outwear for outfit

    """
    if weather == 'hot':
        return [None]
    if weather == 'warm':
        if top[6] == 'light':
            # get a light jacket
            return get_jacket('light', user_id)
        else:
            return [None]
    if weather == 'cool':
        if top[6] == 'light':
            return get_jacket('heavy', user_id)
        if top[6] == 'medium':
            return get_jacket('medium', user_id)
        if top[6] == 'heavy':
            return [None]
    if weather == 'cold':
        return get_jacket('heavy', user_id)
