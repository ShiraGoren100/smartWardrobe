from closet import get_outfit_temperature
from generate import too_hot, too_cold
from user_file import get_users_thresholds


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