import mysql.connector

# print(mysql.connector.__version__)

# Establish a connection to the MySQL server
# db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
cursordb = db.cursor()


def insert_new_user(username, password, email):
    """
    create new user and insert into db
    :param username:
    :param password:
    :param email:
    :return: the users id
    """
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        cursor = db.cursor()
        sql = "INSERT INTO user (userName, password, email) VALUES (%s, %s, %s)"
        val = (username, password, email)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")

    return get_user_id(password, email)



# register
def get_user_id(password, email):
    """
    get user id based on all other parameters
    :param username:
    :param password:
    :param email:
    :return: user id
    """
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT id,username FROM user WHERE  password = %s And email = %s",
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

