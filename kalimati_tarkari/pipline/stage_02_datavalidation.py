from kalimati_tarkari.config.configuration import ConfigurationManager
from kalimati_tarkari.components.data_validation import DataValiadtion
from kalimati_tarkari.logger import logging


STAGE_NAME = "Data Validation stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValiadtion(config=data_validation_config)
        data_validation.validate_all_columns()