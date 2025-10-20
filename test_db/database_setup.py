# https://www.mongodb.com/resources/languages/python#creating-a-mongodb-database-in-python

from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_project():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   # add in mongodb username and password
   CONNECTION_STRING = "mongodb+srv://<username>:<password>@cluster0.okjtuan.mongodb.net/"
 
   # Create a connection using MongoClient
   client = MongoClient(CONNECTION_STRING, server_api=ServerApi('1'))

   # Create the database 
   return client # ['animal_adoption']
  
# Get the database
if __name__ == "__main__":   
  
    dbname = get_project()

    # test the connection 
#    try:
#        dbname.admin.command('ping')
#        print("Pinged your deployment. You successfully connected to MongoDB!")
#    except Exception as e:
#        print(e)

