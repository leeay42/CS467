# https://stackoverflow.com/questions/47668507/how-to-store-images-in-mongodb-through-pymongo
# https://stackoverflow.com/questions/40015103/upload-file-size-16mb-to-mongodb
# https://www.mongodb.com/resources/languages/python#creating-a-mongodb-database-in-python


# Get the database using the method defined in database_setup
from database_setup import get_project
from datetime import datetime
from bson import Binary

# link the Mongodb project
proj_name = get_project()
# database name
dbname = proj_name['animal_adoption']
# collections in database
animals_collection = dbname['animals']
users_collection = dbname['users']

# test users information
user1 = {
    "admin_access": False,
    "first_name": 'Michael',
    "last_name": 'Scott',
    "email": 'mscott@gmail.com',
    "password": 'Dunder Mifflin',
}

user2 = {
    "admin_access": True,
    "first_name": 'Dwight',
    "last_name": 'Schrute',
    "email": 'dschrute@gmail.com',
    "password": 'beets'
}

users_collection.insert_many([user1, user2])

# test animals information 
# images need to be bson data
with open("./images/image1.png", 'rb') as f:
    image_data = f.read()

image_binary1 = Binary(image_data)

animal1 = {
    "name": 'Lassie',
    "availability": 'Not Available',
    "type": 'dog',
    "breed": 'collie',
    "description": 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    "profile_date": datetime.now(),
    "disposition": ['Animal must be leashed at all times'],
    "news_item": 'Lorem ipsum dolor sit amet',
    "public_image": image_binary1
}


with open("./images/image2.png", 'rb') as f:
    image_data = f.read()

image_binary2 = Binary(image_data)

animal2 = {
    "name": 'Salem',
    "availability": 'Available',
    "type": 'cat',
    "breed": 'domestic shorthair',
    "description": 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    "profile_date": datetime.now(),
    "disposition": ['Good with other animals', 'Good with children', 'Animal must be leashed at all times'],
    "news_item": 'Lorem ipsum dolor sit amet',
    "public_image": image_binary2
}

animals_collection.insert_many([animal1, animal2])
