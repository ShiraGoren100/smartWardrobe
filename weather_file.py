import requests


def get_weather(json_obj):
    """
    define weather related needs for outfit
    :param json_obj:
    :return:
    """
    temp_k = float(json_obj['main']['temp'])
    temp_c = temp_k - 273.15  # convert to celsius
    return temp_c


def temperature(latitude, longitude):
    longitude1 = str(int(round(float(longitude))))
    latitude1 = str(int(round(float(latitude))))
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + latitude1 + '&lon=' + longitude1 + '&appid=8f3241a0140c7cbf04fd85bcb7b1cef9')
    json_obj = r.json()
    return json_obj


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