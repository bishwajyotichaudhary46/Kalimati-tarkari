from urllib.parse import quote_plus
import pandas as pd
import pymongo
from kalimati_tarkari.constants import COLLECTION_NAME, MONGODB_URL_KEY, DATABASE_NAME



# Load the data from CSV
df = pd.read_csv("notebook/final_data.csv")

# Filter the DataFrame for 'आलु रातो' (Potato)
df_potato = df[df['Commodity'] == 'आलु रातो']
df_potato = df_potato[['Date', 'Average']]  # Selecting 'Date' and 'Average' columns

# Convert the DataFrame to dictionary format (list of records)
data = df_potato.to_dict(orient='records')

# Select the last record
last_data = data[-1]

# MongoDB client connection
client = pymongo.MongoClient(MONGODB_URL_KEY)
data_base = client[DATABASE_NAME]
collection = data_base[COLLECTION_NAME]

# Insert the last record into the collection
rec = collection.insert_one(last_data)

# Print the inserted document ID
print(f"Inserted document ID: {rec.inserted_id}")
