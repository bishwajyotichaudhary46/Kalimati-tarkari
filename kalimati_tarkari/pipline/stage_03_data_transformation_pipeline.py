from kalimati_tarkari.config.configuration import ConfigurationManager
from kalimati_tarkari.components.data_transformation import DataTransformation
from kalimati_tarkari.logger import logging


STAGE_NAME = "Data Transformation stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.get_data_transform()
