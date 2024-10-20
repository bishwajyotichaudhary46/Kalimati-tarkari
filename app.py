from flask import Flask, render_template, request,jsonify
import os 
import json
#import numpy as np
#import pandas as pd
from kalimati_tarkari.pipline.forecasting import ForecastingPipeline
from kalimati_tarkari.logger import logging
from flask_cors import CORS
#from fetch_data_model import fetch_data_model
#import datetime
#from retrain import Retrain


#Fetching Data From DataBase
#obj = fetch_data_model()
# For Retraining Model
#retrain = Retrain()
#retrain.train_check()

"""
if today == da
    
"""
app = Flask(__name__) # initializing a flask app
CORS(app)

#@app.route("/fetch")
#def fetch_data():
#    return obj.get_data_all()


@app.route("/retrain",methods=['GET'])
def train():
    os.system("python main.py")
    return "Retraining Successful!"

@app.route('/forecast',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            
            obj = ForecastingPipeline()
            period = request.json["period"]
            period = int(period)
            logging.info(period)
            forecast = obj.forecasting(period = period)
            
            logging.info(type(forecast))
            json_str = json.dumps(forecast)

            




            return jsonify(forecast)
        

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=True)
    


