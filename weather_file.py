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


