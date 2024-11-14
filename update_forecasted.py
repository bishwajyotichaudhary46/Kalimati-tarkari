import pymongo
from kalimati_tarkari.constants import COLLECTION_NAME,MONGODB_URL_KEY, DATABASE_NAME
from retrain import Retrain

# Step 1: Get forecasted data
obj = Retrain()
data = obj.forecast()
print(data)
#print(MONGODB_URL_KEY)
try:
    # Step 2: MongoDB client connection
    client = pymongo.MongoClient(MONGODB_URL_KEY)
    data_base = client[DATABASE_NAME]
    collection = data_base['forecasted_data']
    
    # Step 3: Clear existing data and insert new forecasted data
    collection.delete_many({})  # Corrected method name
    collection.insert_many(data)
    
    # Step 4: Print confirmation message
    print("Forecast Updated")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Step 5: Close the MongoDB connection
    client.close()
