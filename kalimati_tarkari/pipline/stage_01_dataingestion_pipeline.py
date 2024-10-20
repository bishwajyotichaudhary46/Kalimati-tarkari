from kalimati_tarkari.config.configuration import ConfigurationManager
from kalimati_tarkari.components.data_ingestion import DataIngestion
from kalimati_tarkari.logger import logging
from kalimati_tarkari.exception import KalimatiException
class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion.export_data_into_feature_store()
        except Exception as e:
            raise KalimatiException(e)