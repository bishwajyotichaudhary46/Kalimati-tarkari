import pymongo
from kalimati_tarkari.constants import MONGODB_URL_KEY, DATABASE_NAME

class FetchDB:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGODB_URL_KEY)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db['forecasted_data']

    def get_data(self):
        data = self.collection.find()
        dates = []
        averages = []
        for doc in data:
            dates.append(doc.get('Date'))
            averages.append(float(doc.get('Average')))
        print(averages,dates)
        self.client.close()
        return dates, averages