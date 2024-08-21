from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client=MongoClient(mongo_uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db=client["RAG_database"]
collection=db["Data"]


client_collection=db["clients"]
bot_collection=db["bots"]
user_collection =db["users"]