from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

# load mongoDB password 
mongo_password = os.getenv('MONGO_PASSWORD')

def delete_database(database_uri, database_name, collection_name):
    client = MongoClient(database_uri)
    try:
        database = client[database_name]
        if collection_name in database.list_collection_names():
            database[collection_name].drop()
            print(f"Collection {collection_name} deleted successfully. ")
        else:
            print(f"Collection {collection_name} NOT FOUND in the database {database_name}")

    except Exception as e: 
        print(f"Error: {e}")

if __name__ =="__main__":
        mongo_uri = os.getenv('MONGODB_URI')  
        database_name = "github_issues"
        collection_name = "ghw"
        delete_database(mongo_uri, database_name, collection_name)