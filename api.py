import mysql.connector
# print(mysql.connector.__version__)

# Establish a connection to the MySQL server
db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
cursordb = db.cursor()


def insert_new_user(username, password, email):
    """
    create new user and insert into db
    :param username:
    :param password:
    :param email:
    :return: the users id
    """
    sql = "INSERT INTO user (userName, password, email) VALUES (%s, %s, %s)"
    val = (username, password, email)
    cursordb.execute(sql, val)
    cursordb.commit()
    return get_user_id(username, password, email)


def get_user_id(username, password, email):
    """
    get user id based on all other parameters
    :param username:
    :param password:
    :param email:
    :return: user id
    """
    cursordb.execute(
        "SELECT id FROM user WHERE userName = %s AND password = %s And email = %s",
        ((username), (password), (email)))
    # Fetch the result
    user_id = cursordb.fetchone()[0]
    return user_id

