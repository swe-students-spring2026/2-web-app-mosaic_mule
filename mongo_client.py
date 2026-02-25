import pymongo
from bson.objectid import ObjectId
import datetime

# make a connection to the database server
connection = pymongo.MongoClient("mongodb://your_username:your_username@your_host_name:27017")
# select a specific database on the server
db = connection["db_name"]