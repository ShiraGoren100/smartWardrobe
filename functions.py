import mysql.connector

# print(mysql.connector.__version__)

# Establish a connection to the MySQL server
# db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
cursordb = db.cursor()


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
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        #  db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursor = db.cursor()
        sql = "INSERT INTO user (userName, password, email, hot, warm, cool) VALUES (%s, %s, %s)"
        val = (username, password, email, warm_threshold, cool_threshold, cold_threshold )
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
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
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


def insert_new_item(data, user_id):
    """
    add a new clothing item to db.
    :param data: dict with all info about new item
    """
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursor = db.cursor()
        # get general attributes of item (assuming data is a json and first things are as follows:

        pic = data['img']
        category = data['category']

        # get category id from categories table
        category_id = get_category_id(category)

        # add clothing item to db
        sql = "INSERT INTO clothing_item (picture, user_id, category) VALUES (%s, %s, %s)"
        val = (pic, user_id, category_id)
        cursor.execute(sql, val)
        db.commit()

        # get item id
        item_id = get_item_id(pic, user_id, category_id, data)

        add_item_tags(data, item_id)

        cursor.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")


def add_item_tags(data, item_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursor = db.cursor()

        for x in data.keys():
            if x != 'user_id' and x != 'img' and x != 'category':
                # Get tag id

                cursor.execute("SELECT id FROM tags WHERE tag_name = %s", (x,))
                tag_id = cursor.fetchone()[0]

                # Add tag and item to tag-item table
                sql = "INSERT INTO tags_clothing_item (clothing_item_id, tag_id, tag_value) VALUES (%s, %s, %s)"
                val = (item_id, tag_id, data[x])
                cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()
        print("Added tags")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_item_id(pic, user_id, category_id, data):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursor = db.cursor()
        cursordb.execute(
            "SELECT id FROM clothing_item WHERE picture = %s AND user_id = %s AND category = %s",
            (pic, user_id, category_id))
        # Fetch the result
        item_id = cursordb.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        return item_id
    except Exception as e:
        print(f"An error occurred: {e}")


def get_item_pic(item_id):
    """
    returns item picture
    :param item_id:
    :return:
    """
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT pic FROM clothing_item WHERE  item_id = %s",
            ((item_id)))
        # Fetch the result
        pic = cursordb.fetchone()[0]
        dump = cursordb.fetchall()
        cursordb.close()
        db.close()
        return pic
    except Exception as e:
        print(f"An error occurred: {e}")


def get_category_id(category):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()
        cursordb.execute("SELECT id FROM categories WHERE type = %s", (category,))
        # Fetch the result
        cat_id = cursordb.fetchone()[0]
        dump = cursordb.fetchall()
        cursordb.close()
        db.close()
        return str(cat_id)
    except Exception as e:
        print(f"An error occurred: {e}")


def get_closet(user_id, category):

    """
    returns all items of certain category in users closet
    :param user_id:
    :return:
    """
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()
        category_id = get_category_id(category)
        cursordb.execute(
            "SELECT * FROM clothing_item WHERE  user_id = %s and category= %s",(user_id, category_id))
        # Fetch the result
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")

def get_item_property(item_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT tc.tag_name, tci.tag_value FROM tags_clothing_item tci JOIN tags tc ON tci.tag_id = tc.id where tci.clothing_item_id=%s;",(item_id,))
        # Fetch the result
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")



def generate(json_obj):
    return


def delete_item(item_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)
        cursordb = db.cursor()
        # Delete from tags_clothing_item table
        cursordb.execute("DELETE FROM smartwardrobe.tags_clothing_item WHERE clothing_item_id = %s;", (item_id,))
        db.commit()
        print(cursordb.statement)

        # Delete from clothing_item table
        cursordb.execute("DELETE FROM smartwardrobe.clothing_item WHERE id = %s;", (item_id,))
        db.commit()
        print(cursordb.statement)

        # Close the cursor and database connection
        cursordb.close()
        db.close()

    except mysql.connector.Error as err:
        print("An error occurred:", err)

    except Exception as e:
        print(f"An error occurred: {e}")

    return None