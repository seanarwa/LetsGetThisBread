from pymongo import MongoClient

db_client = MongoClient('localhost', 27017)
db = db_client['LetsGetThisBread']
db.drop_collection('Submission')