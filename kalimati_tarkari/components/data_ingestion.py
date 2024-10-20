import os
import sys

from pandas import DataFrame
from kalimati_tarkari.exception import KalimatiException
from kalimati_tarkari.logger import logging
from kalimati_tarkari.data_acess.kalimati_data import KalimatiData



class DataIngestion:
    def __init__(self,data_ingestion_config):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise KalimatiException(e,sys)
        

    
    def export_data_into_feature_store(self)->DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from mongodb to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info(f"Exporting data from mongodb")
            usvisa_data = KalimatiData()
            dataframe = usvisa_data.export_collection_as_dataframe(collection_name=
                                                                   self.data_ingestion_config.collection_name)
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path  = self.data_ingestion_config.local_data_file
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise KalimatiException(e,sys)
        
    
   