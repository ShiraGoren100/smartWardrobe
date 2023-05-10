import mysql.connector

# print(mysql.connector.__version__)

# Establish a connection to the MySQL server
db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
#db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
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
       # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
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
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
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


def insert_new_item(data):
    """
    add a new clothing item to db.
    :param data: dict with all info about new item
    """
    try:
        #db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="smatrwardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",
                                     port=3307)
        cursor = db.cursor()
        # get general attributes of item (assuming data is a json and first things are as follows:
        user_id = data['user_id']
        pic = data['picture']
        category = data['category']

        # get category id from categories table
        cursordb.execute(
            "SELECT id FROM categories WHERE  type = %s",
            ((category)))
        # Fetch the result
        category_id = cursordb.fetchone()[0]

        #add clothing item to db
        sql = "INSERT INTO clothing_item (picture, user_id, category) VALUES (%s, %s, %s)"
        val = (pic, user_id, category_id)
        cursor.execute(sql, val)

        #get item id
        cursordb.execute(
            "SELECT id FROM clothing_item WHERE  picture = %s, user_id = %s, category = %s",
            ((pic), (user_id), (category_id)))
        # Fetch the result
        item_id = cursordb.fetchone()[0]

        #run through rest of data, this is where the tags are
        for x in data.keys():
            if x != 'user_id' and x!= 'picture' and x != 'category':
                # get tag id
                "SELECT id FROM tags WHERE  tag_name = %s",
                ((data[x]))
                # Fetch the result
                tag_id = cursordb.fetchone()[0]
                # add tag and item to tag-item table
                sql = "INSERT INTO tags_clothing_item (clothing_item_id, tag_id, tag_value) VALUES (%s, %s, %s)"
                val = (item_id, tag_id, data[x])
                cursor.execute(sql, val)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")


