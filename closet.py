import datetime
import random
import mysql.connector



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

        cursor.close()
        db.close()
        # get item id
        item_id = get_item_id(pic, user_id, category_id)

        add_item_tags(data, item_id)

    except Exception as e:
        print(f"An error occurred: {e}")


def add_item_tags(data, item_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
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


def get_item_id(pic, user_id, category_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
        cursor = db.cursor()
        cursor.execute(
            "SELECT id FROM clothing_item WHERE picture = %s AND user_id = %s AND category = %s",
            (pic, user_id, category_id))
        # Fetch the result

        item_id = cursor.fetchall()
        cursor.close()
        db.close()
        return item_id[0][0]
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
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
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
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
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


def get_items_from_closet(user_id, category):
    """
    returns all items of certain category in users closet
    :param user_id:
    :return:
    """
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
        cursordb = db.cursor()
        category_id = get_category_id(category)
        cursordb.execute(
            "SELECT * FROM clothing_item WHERE  user_id = %s and category= %s", (user_id, category_id))
        # Fetch the result
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


def get_item_by_id(item_id):
    """
    returns all item properties by the item id
    :param user_id:
    :return:
    """
    try:
        # db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "    SELECT * FROM clothing_item WHERE id = %s", (item_id,))
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
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
        cursordb = db.cursor()
        cursordb.execute(
            "SELECT tc.tag_name, tci.tag_value FROM tags_clothing_item tci JOIN tags tc ON tci.tag_id = tc.id where tci.clothing_item_id=%s;", (item_id,))
        # Fetch the result
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_item(item_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)
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


def add_outfit(user_id, top, bottom, outwear, shoes, temperature):
    """
    add outfit to db
    """
    date = datetime.now()
    date_string = date.strftime("%Y-%m-%d")
    try:

        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()
        sql = "INSERT INTO outfits (top, bottom, outwear, shoes, last_used, user_id, temperature) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (top, bottom, outwear, shoes, date_string, user_id, temperature)
        cursordb.execute(sql, val)
        db.commit()
        cursordb.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_outfit_by_id(id):
    """
    returns outfit based on outfit id    :param id:
    :return: all outfit info
    """
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute("SELECT * "
                         "FROM outfits WHERE id = %s;", ([id]))
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


def check_outfit(user_id, top, bottom, shoes):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute("SELECT last_used, id "
                         "FROM outfits WHERE user_id = %s  "
                         "AND top = %s  AND bottom = %s  "
                         "AND shoes = %s;", (user_id, top, bottom, shoes))
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


def get_jacket(thickness):
    """
     returns jacket based on weather and top chosen
     """
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()
        cursordb.execute(
            "SELECT ci.id, ci.picture, ci.user_id, ci.category, "
            "tci_weather.tag_value AS weather, "
            "tci_sleeves.tag_value AS sleeves, "
            "tci_thickness.tag_value AS thickness "
            "tci_length.tag_value AS length, "
            "FROM clothing_item ci "
            "JOIN categories c ON ci.category = c.id "
            "JOIN tags_clothing_item tci_weather ON tci_weather.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_sleeves ON tci_sleeves.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_length ON tci_length.clothing_item_id = ci.id "
            "JOIN tags_clothing_item tci_thickness ON tci_thickness.clothing_item_id = ci.id "
            "JOIN tags t_weather ON t_weather.id = tci_weather.tag_id "
            "JOIN tags t_sleeves ON t_sleeves.id = tci_sleeves.tag_id "
            "JOIN tags t_length ON t_length.id = tci_length.tag_id "
            "JOIN tags t_thickness ON t_thickness.id = tci_thickness.tag_id "
            "WHERE c.type = 'outwear' "
            "AND t_weather.tag_name = 'weather' "
            "AND t_thickness.tag_name = 'thickness'"
            " AND tci_thickness.tag_value = %s;"
            ";",
            [thickness]
        )
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        if data == []:
            return [None]
        random_choice = random.choice(data)
        return random_choice

    except Exception as e:
        print(f"An error occurred: {e}")


def get_outfit_temperature(outfit_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe",port=3307)

        cursordb = db.cursor()

        # get all clothing items that are classified as summer.
        cursordb.execute("SELECT temperature "
                         "FROM outfits WHERE id = %s;"
                         , (outfit_id,))
        data = cursordb.fetchall()
        cursordb.close()
        db.close()
        return data[0]
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_outfit(outfit_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")
        # db = mysql.connector.connect(host="localhost", user="root", passwd="TxEhuTkXhxnt1", database="SmartWardrobe", port=3307)

        cursordb = db.cursor()
        sql = "DELETE FROM outfits WHERE id = %s;"
        val = (outfit_id)
        cursordb.execute(sql, val)
        db.commit()
        cursordb.close()
        db.close()

    except Exception as e:
        print(f"An error occurred: {e}")
