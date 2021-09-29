import pymongo

mongo_url = "mongodb://localhost:27017"

client = pymongo.MongoClient(mongo_url)

db = client.get_database("onlineStoreData")
