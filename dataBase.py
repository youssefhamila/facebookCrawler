import pymongo
from bson.json_util import dumps
from fastapi.responses import JSONResponse


#connect to database
def connection(collection):
	#docker DB
	myclient = pymongo.MongoClient(host="test_mongodb",port=27017,username="root",password="pass",authSource="admin")
	#local DB
	#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["Facebook"]
	mycol = mydb[collection]
	return mycol
#insert in DB
def insert_database(data,mycol):
	try:
		mycol.insert_one(data)
		return True
	except:
		return False
#return all posts from DB
def showAll():
	mycol=connection('posts')
	l=[]
	result=list(mycol.find({}))
	cursor=mycol.find()
	for document in cursor:
		l.append(document)
	return JSONResponse(content=dumps(l))
