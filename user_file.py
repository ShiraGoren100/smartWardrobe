import mysql.connector

cool_threshold = 18
warm_threshold = 24
cold_threshold = 14


def insert_new_user(username, password, email):
    """
    create new user and insert into db
    :param username:
    :param password:
    :param email:
    :return: the users id
    """
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursor = db.cursor()
        sql = "INSERT INTO user (userName, password, email, hot, warm, cool, days_interval) VALUES (%s, %s, %s,%s, %s, %s, %s)"
        val = (username, password, email, warm_threshold, cool_threshold, cold_threshold, 3)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    except Exception as e:
        print(f"An error occurred: {e}")

    return get_user_id(password, email)


def get_user_id(password, email):
    """
    get user id based on all other parameters
    :param password:
    :param email:
    :return: user id
    """
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT id,username,days_interval FROM user WHERE  password = %s And email = %s",
            ((password), (email)))
        # Fetch the result
        user_id = cursordb.fetchone()[0]
        user_name = cursordb.fetchone()[1]
        dump = cursordb.fetchall()
        cursordb.close()
        db.close()
        return str(user_id), user_name
    except Exception as e:
        print(f"An error occurred: {e}")


def get_users_thresholds(user_id):
    """
    returns the weather threshold of user
    :param user_id:
    :return:
    """

    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursordb = db.cursor()
        cursordb.execute("SELECT hot,warm,cool FROM user WHERE id = %s;", [user_id])
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


def set_days_interval(user_id, val):
    """
    set the interval between re-wearing an outfit
    :param user_id:
    :param val:
    :return:
    """
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
