import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["caesarcipher"]
mycol = mydb["cryptographies"]
print(mydb.list_collection_names())
