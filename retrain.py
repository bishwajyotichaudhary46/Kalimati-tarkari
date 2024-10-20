from datetime import datetime, timedelta
import pandas as pd
import os
class Retrain:
    def __init__(self):
        self.current_date = datetime.now().date()
        self.date = pd.read_csv("artifacts/retrain/my_date.csv")
        

    def add_date(self):
        # Get the current date
        # Add 7 days to the current date
        new_date = self.current_date + timedelta(days=1)
        df = pd.DataFrame({"Date":[new_date]})
        df.to_csv("artifacts/retrain/my_date.csv",index=False)

        # Print the new date
        print("New date:", new_date)

    def train_check(self):
        print(type(self.date["Date"][0]))
        today =str(self.current_date)
        print(today)
        if today == self.date["Date"][0]:
            self.add_date()
            print("matched")
            os.system("python scraping.py")
            print("scrapped")
            df = pd.read_csv("notebook\final_data.csv")
            df = df[-1:]
            df['Date'] = pd.to_datetime(df['Date'])
            if df['Date'] == datetime.now():
                os.system("python update_db.py")
            os.system("python main.py")
            return "Sucessfully retrain"
        else:
            return "Today is not retraining Date"
        



obj = Retrain()

obj.train_check()
