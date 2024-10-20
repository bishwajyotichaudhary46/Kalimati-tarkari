from kalimati_tarkari.config.configuration import ConfigurationManager
from kalimati_tarkari.components.data_spliting import DataSpliting
from kalimati_tarkari.logger import logging




class DataSplitingTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_spliting_config = config.get_data_spliting_config()
        data_spliting = DataSpliting(config=data_spliting_config)
        data_spliting.get_data_spliting()