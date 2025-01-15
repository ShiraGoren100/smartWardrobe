import json
import pytest
import API
import closet
import user_file


#todo: change longitude and latitude to fit weathe rwe expect when running tests
@pytest.fixture
def client():
    app = API.app.test_client()
    return app


def test_register(client):
    """
    tests ther register functionality- adds user to db,checks all is well
    :param client:
    :return:
    """
    # Prepare test data
    data = {
        "email": "test@example.com",
        "password": "password123",
        "username": "testuser"
    }

    # Send POST request to register endpoint
    response = client.post('/register', json=data)
    assert response.status_code == 200

    # Validate the response
    user = json.loads(response.data)
    assert isinstance(user, dict)
    assert "userId" in user
    assert "displayName" in user
    assert "interval" in user
    assert user["displayName"] == "testuser"


def test_login(client):
    # Prepare test data
    data = {
        'email': "test@example.com",
        'password': "password123"
    }

    # Make a POST request to the login endpoint
    response = client.post('/login', json=data)

    # Check the response
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Convert the response data to a dictionary
    user = json.loads(response.data)

    # Perform assertions on the user data
    assert 'userId' in user
    assert 'displayName' in user
    assert 'interval' in user
    assert user['displayName'] == "testuser"


def test_add_item(client):
    # Prepare test data
    data = {
        'img': 'value1.jpg',
        'category': 'dresses',
        'color': 'blue',
        'sleeves': 'short sleeves',
        'length': 'knee length',
        'weather': 'hot',
        'thickness': 'light'
    }
    user_id = user_file.get_user_id("password123", "test@example.com")[0]
    # Make a POST request to the addItem endpoint
    response = client.post('/addItem?id='+user_id, json=data)

    # Check the response
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Convert the response data to a dictionary
    result = json.loads(response.data)
    category_id = closet.get_category_id('dresses')
    item_id = closet.get_item_id('value1.jpg', user_id, category_id)
    item = closet.get_item_by_id(item_id)[0]
    # check that item was added to the db
    assert item[0] == item_id
    assert item[1] == 'value1.jpg'
    assert item[2] == int(user_id)
    assert item[3] == int(category_id)
    list2 = []
    tags = API.get_item_as_clist([item_id, 'value1.jpg'], list2)

    assert {'title': 'color', 'value': 'blue'} in list2[0]['properties']
    assert {'title': 'Weather', 'value': 'hot'} in list2[0]['properties']
    assert {'title': 'Thickness', 'value': 'light'} in list2[0]['properties']
    assert {'title': 'Length', 'value': 'knee length'} in list2[0]['properties']
    assert {'title': 'Sleeves', 'value': 'short sleeves'} in list2[0]['properties']


def test_delete_item(client):

    user_id = user_file.get_user_id("password123", "test@example.com")[0]
    item_id = closet.get_item_id('value1.jpg', user_id, 3)

    # Send a DELETE request to delete the item
    response = client.delete('/deleteItem', query_string={'id': item_id})
    assert response.status_code == 200

    # Verify that the item is deleted
    response = client.get('/closet', query_string={'id': user_id, 'category': 'Dresses'})
    assert response.status_code == 200
    data = json.loads(response.data)
    if data:
         assert item_id not in [item['id'] for item in data['list']]

def call_generate(longitude, latitude, user_id, client):
    # Send GET request to generate_outfit endpoint
    response = client.get('/outfit', query_string={'id': user_id, 'latitude': latitude, 'longitude': longitude})

    # Check the response
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Convert the response data to a dictionary
    outfit = json.loads(response.data)
    return outfit


def call_regenerate(longitude, latitude, user_id, client, outfitid):
    # Send GET request to generate_outfit endpoint
    response = client.get('/regenerate', query_string={'id': user_id, 'latitude': latitude, 'longitude': longitude, 'outfitid':outfitid})

    # Check the response
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Convert the response data to a dictionary
    outfit = json.loads(response.data)
    return outfit


def add_item(user_id, data, client):
    # Make a POST request to the addItem endpoint
    response = client.post('/addItem?id='+user_id, json=data)

    # Check the response
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Convert the response data to a dictionary
    result = json.loads(response.data)


def create_test_wardrobe(user_id, client):
    # Prepare test data
    closet_list = [{
        'img': 'Shirt1.jpg',
        'category': 'Shirts',
        'color': 'white',
        'sleeves': 'short sleeves',
        'weather': 'hot',
        'thickness': 'light'},
        {
            'img': 'Shirt2.jpg',
            'category': 'Shirts',
            'color': 'pink',
            'sleeves': 'short sleeves',
            'weather': 'hot',
            'thickness': 'light'
        },
        {
            'img': 'Shirt3.jpg',
            'category': 'Shirts',
            'color': 'black',
            'sleeves': 'short sleeves',
            'weather': 'hot',
            'thickness': 'light'
        },
        {
            'img': 'Shirt4.jpg',
            'category': 'Shirts',
            'color': 'purple',
            'sleeves': 'long sleeves',
            'weather': 'hot',
            'thickness': 'light'
        },
        {
            'img': 'Shirt5.jpg',
            'category': 'Shirts',
            'color': 'yellow',
            'sleeves': 'short sleeves',
            'weather': 'cold',
            'thickness': 'light'
        },
        {
            'img': 'Shirt6.jpg',
            'category': 'Shirts',
            'color': 'green',
            'sleeves': 'short sleeves',
            'weather': 'warm',
            'thickness': 'light'
        },
        {
            'img': 'Shirt7.jpg',
            'category': 'Shirts',
            'color': 'white',
            'sleeves': 'short sleeves',
            'weather': 'cool',
            'thickness': 'light'
        },
        {
            'img': 'Shirt8.jpg',
            'category': 'Shirts',
            'color': 'grey',
            'sleeves': 'short sleeves',
            'weather': 'hot',
            'thickness': 'medium'
        },
        {
            'img': 'Shirt9.jpg',
            'category': 'Shirts',
            'color': 'maroon',
            'sleeves': 'short sleeves',
            'weather': 'warm',
            'thickness': 'medium'
        },
        {
            'img': 'Shirt10.jpg',
            'category': 'Shirts',
            'color': 'magenta',
            'sleeves': 'short sleeves',
            'weather': 'hot',
            'thickness': 'heavy'
        },
        {
            'img': 'Shirt11.jpg',
            'category': 'Shirts',
            'color': 'white',
            'sleeves': 'long sleeves',
            'weather': 'warm',
            'thickness': 'light'
        },{
            'img': 'Shirt12.jpg',
            'category': 'Shirts',
            'color': 'white',
            'sleeves': 'long sleeves',
            'weather': 'warm',
            'thickness': 'heavy'
        },{
            'img': 'Shirt13.jpg',
            'category': 'Shirts',
            'color': 'white',
            'sleeves': 'long sleeves',
            'weather': 'cold',
            'thickness': 'heavy'
        },{
            'img': 'Shirt11.jpg',
            'category': 'Shirts',
            'color': 'white',
            'sleeves': 'long sleeves',
            'weather': 'cool',
            'thickness': 'medium'
        },{
            'img': 'pants1.jpg',
            'category': 'Pants',
            'color': 'white',
           'length': 'long',
            'weather': 'warm',
            'thickness': 'light'
        },{
            'img': 'pants2.jpg',
            'category': 'Pants',
            'color': 'white',
           'length': 'short',
            'weather': 'hot',
            'thickness': 'light'
        },{
            'img': 'pants3.jpg',
            'category': 'Pants',
            'color': 'white',
           'length': 'long',
            'weather': 'cool',
            'thickness': 'medium'
        },{
            'img': 'pants4.jpg',
            'category': 'Pants',
            'color': 'white',
           'length': 'knee length',
            'weather': 'warm',
            'thickness': 'light'
        },{
            'img': 'pants5.jpg',
            'category': 'Pants',
            'color': 'white',
           'length': 'knee length',
            'weather': 'warm',
            'thickness': 'light'
        },{
            'img': 'skirts1.jpg',
            'category': 'Skirts',
            'color': 'white',
           'length': 'long',
            'weather': 'hot',
            'thickness': 'light'
        },{
            'img': 'skirts2.jpg',
            'category': 'Skirts',
            'color': 'white',
           'length': 'short',
            'weather': 'cold',
            'thickness': 'light'
        },{
            'img': 'dress1.jpg',
            'category': 'Dresses',
            'color': 'white',
           'length': 'short',
            'weather': 'hot',
            'thickness': 'light'
        },{
            'img': 'dress2.jpg',
            'category': 'Dresses',
            'color': 'white',
           'length': 'short',
            'weather': 'cool',
            'thickness': 'heavy'
        },{
            'img': 'shoes1.jpg',
            'category': 'Footwear',
            'color': 'white',
            'weather': 'cool',

        },{
            'img': 'shoes2.jpg',
            'category': 'Footwear',
            'color': 'white',
            'weather': 'warm',
        },{
            'img': 'shoes3.jpg',
            'category': 'Footwear',
            'color': 'white',
            'weather': 'hot',
        },{
            'img': 'shoes4.jpg',
            'category': 'Footwear',
            'color': 'black',
            'weather': 'hot',
        },{
            'img': 'shoes5.jpg',
            'category': 'Footwear',
            'color': 'white',
            'weather': 'cold',
        },{
            'img': 'Sweater1.jpg',
            'category': 'Sweaters',
            'color': 'white',
            'sleeves': 'long sleeves',
            'weather': 'cool',
            'thickness': 'medium'
        },{
            'img': 'Sweatert2.jpg',
            'category': 'Shirts',
            'color': 'white',
            'sleeves': 'long sleeves',
            'weather': 'cold',
            'thickness': 'heavy'
        },{
            'img': 'coat1.jpg',
            'category': 'Coats',
            'color': 'white',
            'sleeves': 'long sleeves',
            'weather': 'cool',
            'thickness': 'medium'
        },{
            'img': 'coat2.jpg',
            'category': 'Coats',
            'color': 'pink',
            'sleeves': 'long sleeves',
            'weather': 'cold',
            'thickness': 'Heavy'
        }
    ]
    item_id_list = []
    for item in closet_list:
        add_item(user_id, item, client)
        category_id = closet.get_category_id(item['category'])
        item_id = closet.get_item_id(item['img'], user_id, category_id)
        item_id_list.append(item_id)
    return item_id_list


def test_generate_outfit(client):
    # Prepare test data
    user_id = user_file.get_user_id("password123", "test@example.com")[0]
    # create a test wardrobe
    item_id_list = create_test_wardrobe(user_id, client)
    # test for hot weather
    latitude = '32.083549'
    longitude = '34.815498'
    outfit = call_generate(longitude, latitude, user_id, client)

    # Perform assertions on the outfit data
    assert 'outfitId' in outfit
    assert 'date' in outfit
    assert 'list' in outfit
    assert 'userId' in outfit
    assert isinstance(outfit['outfitId'], int)
    assert isinstance(outfit['date'], str)
    assert isinstance(outfit['list'], list)

    # Perform assertions on each item in the outfit
    for item in outfit['list']:
        assert 'id' in item
        assert 'img' in item
        assert 'properties' in item
        assert isinstance(item['id'], int)
        assert isinstance(item['img'], str)
        assert isinstance(item['properties'], list)
        assert len(item['properties']) > 0  # Assuming each item has at least one property
        assert {'title': 'Thickness', 'value': 'heavy'} not in item['properties']

    # test for cold weather
    latitude = '-82.862755'
    longitude = '135.000000'
    outfit = call_generate(longitude, latitude, user_id, client)


    # test for warm weather
    latitude = '39.320980'
    longitude = '-111.093735'
    outfit = call_generate(longitude, latitude, user_id, client)
    for item in outfit['list']:
        assert {'title': 'Thickness', 'value': 'heavy'} not in item['properties']

    # test for cool weather
    latitude = '56.130367'
    longitude = '-106.346771'
    outfit = call_generate(longitude, latitude, user_id, client)

    # delete all the items we are adding
    for id in item_id_list:
        # Send a DELETE request to delete the item
        response = client.delete('/deleteItem', query_string={'id': id})
        assert response.status_code == 200
        # Validate the response
        user = json.loads(response.data)


def same_outfit(outfit1, outfit2):
    for item1 in outfit1['list']:
        for item2 in outfit2['list']:
            if item1['id'] != item2['id']:
                return False
    return True

def test_REgenerate_outfit(client):
    # Prepare test data
    user_id = user_file.get_user_id("password123", "test@example.com")[0]
    # create a test wardrobe
    item_id_list = create_test_wardrobe(user_id, client)
    # test for hot weather
    latitude = '32.083549'
    longitude = '34.815498'
    outfit1 = call_generate(longitude, latitude, user_id, client)
    outfit2 = call_regenerate(longitude, latitude, user_id, client, outfit1['outfitId'])

    # Perform assertions on each item in the outfit
    for item in outfit2['list']:
        assert 'id' in item
        assert 'img' in item
        assert 'properties' in item
        assert isinstance(item['id'], int)
        assert isinstance(item['img'], str)
        assert isinstance(item['properties'], list)
        assert len(item['properties']) > 0  # Assuming each item has at least one property
        assert {'title': 'Thickness', 'value': 'heavy'} not in item['properties']
    assert not same_outfit(outfit1, outfit2)

    # test for cold weather
    latitude = '-82.862755'
    longitude = '135.000000'
    outfit1 = call_generate(longitude, latitude, user_id, client)
    outfit2 = call_regenerate(longitude, latitude, user_id, client, outfit1['outfitId'])
    assert not same_outfit(outfit1, outfit2)

    # test for warm weather
    latitude = '39.320980'
    longitude = '-111.093735'
    outfit1 = call_generate(longitude, latitude, user_id, client)
    outfit2 = call_regenerate(longitude, latitude, user_id, client, outfit1['outfitId'])
    for item in outfit2['list']:
        assert {'title': 'Thickness', 'value': 'heavy'} not in item['properties']
    assert not same_outfit(outfit1, outfit2)

    # test for cool weather
    latitude = '56.130367'
    longitude = '-106.346771'
    outfit1 = call_generate(longitude, latitude, user_id, client)
    outfit2 = call_regenerate(longitude, latitude, user_id, client, outfit1['outfitId'])
    assert not same_outfit(outfit1, outfit2)


    # delete all the items we are adding
    for id in item_id_list:
        # Send a DELETE request to delete the item
        response = client.delete('/deleteItem', query_string={'id': id})
        assert response.status_code == 200



def test_clear_test():

    user_id = user_file.get_user_id("password123", "test@example.com")[0]
    user_file.remove_user(user_id)  # Remove the registered user