from datetime import datetime, timedelta
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from kalimati_tarkari.pipline.forecasting import ForecastingPipeline
from kalimati_tarkari.logger import logging
import pandas as pd
import json
class Retrain:
    def __init__(self):
        self.current_date = datetime.now()
        self.date = pd.read_csv("artifacts/retrain/my_date.csv")
        self.forecst_obj = ForecastingPipeline()
            
    
        

    def add_date(self):
        # Get the current date
        # Add 1 days to the current date
        new_date = self.current_date + timedelta(days=1) 
        new_date = new_date.strftime("%Y-%m-%d %H:%M")
        df = pd.DataFrame({"Date":[new_date]})
        df.to_csv("artifacts/retrain/my_date.csv",index=False)
        # Print the new date
        print("New date:", new_date)

    def forecast(self):
        forecasted_output = self.forecst_obj.forecasts(forecast_length=8).tolist()
        
        # Generate dates starting from today
        start_date = datetime.today()
        dates = [(start_date + timedelta(days=i)).strftime('%m/%d/%Y') for i in range(len(forecasted_output))]

        # Create a list of dictionaries in the desired format
        result = [{"Date": date, "Average": f"{value:.2f}"} for date, value in zip(dates[1:], forecasted_output[1:])]

        
        return result

    def train_check(self):
        today = str(self.current_date.strftime("%Y-%m-%d %H:%M"))
        date = self.date["Date"][0]
        if today == date:
            self.add_date()
            print("matched")
            os.system("python scraping.py")
            print("scrapped")
            os.system("python update_db.py")
            print("Database Updated Sucessfully...!!!")
            print("Retraining  started....")
            os.system("python main.py")
            print("Retraining Sucessfully...")
            os.system("python update_forecasted.py")
            return "Sucessfully retrain"
        else:
            return "Today is not retraining Date"
        

