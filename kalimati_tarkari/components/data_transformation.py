import os
from datetime import datetime, timedelta
import pandas as pd
from kalimati_tarkari.exception import KalimatiException
from kalimati_tarkari.logger import logging
from kalimati_tarkari.config.configuration import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.devanagari_to_english = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
        }

    def replace_devanagari_with_eng(self,text):
        for dev, eng in self.devanagari_to_english.items():
            text = text.replace(dev, eng)
        return text

    def cleaning_data(self,data_path):
        data = pd.read_csv(self.config.data_path)
         # Generate the range of dates for the year 2024
        date_range = []
        current = datetime(2013, 4, 15)
        end_date = datetime.now()
        while current <= end_date:
            date_range.append(current.strftime('%m/%d/%Y'))
            current += timedelta(days=1)

        date_range = pd.Index(date_range)
        complete_df = pd.DataFrame(date_range, columns=['Date'])
        final_df = pd.merge(complete_df,data, on=['Date'], how='left')
        final_df['Average'] = final_df['Average'].str.replace("रू","")
        final_df['Average'] = final_df['Average'].astype('str').apply(self.replace_devanagari_with_eng).astype('float')
        final_df['Date'] = pd.to_datetime(final_df['Date'])
        final_df['Date'] = final_df['Date'].dt.date
        final_df.set_index('Date', inplace=True)
        return final_df
        
        


    
    def get_data_transform(self):
        final_df = self.cleaning_data(self.config.data_path)
        missing = final_df.isnull().sum()
        logging.info(missing)
        final_df['Average'].fillna(final_df["Average"].ewm(span=60, adjust=False).mean(),inplace=True)
        logging.info("filling Missing value done sucessfully !")
        return final_df.to_csv("artifacts/data_transformation/final_data.csv",index=True)
        
        
    
    
