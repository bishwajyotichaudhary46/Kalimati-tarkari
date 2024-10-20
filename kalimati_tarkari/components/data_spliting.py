import pandas as pd
from kalimati_tarkari.logger import logging
from kalimati_tarkari.config.configuration import DataSplitingConfig


class DataSpliting:
    def __init__(self, config=DataSplitingConfig):
        self.config = config
    
    def get_data_spliting(self):
        data = pd.read_csv(self.config.data_path)
        length = data.shape[0]
        train = data[:int(length*0.8)]
        test = data[int(length*0.8):]
        logging.info(train.shape)
        logging.info(test.shape)

        train = train.to_csv("artifacts/data_spliting/train.csv",index=False)
        test = test.to_csv("artifacts/data_spliting/test.csv", index=False)

        logging.info("Suceess fully splited")

        return train, test