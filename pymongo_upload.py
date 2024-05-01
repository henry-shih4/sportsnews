# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_db import get_database
import json

def upload_to_mongodb(json_file):
    dbname = get_database()
    collection_name = dbname["articles"]

 

    with open(json_file) as f:
        articles = json.load(f)

    existing_items = collection_name.find({'title': {'$in': [article['title'] for article in articles]}})

    existing_names = set(item['title'] for item in existing_items)
    new_items = [item for item in articles if item['title'] not in existing_names]

    if len(new_items) == 0:
        print('All items already exist in the MongoDB database') 
    
    if new_items:
        collection_name.insert_many(new_items)
        print("Data inserted successfully into MongoDB")

