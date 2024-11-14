from flask import Flask, render_template, request, jsonify
import os
import json
import threading
import time
from kalimati_tarkari.pipline.forecasting import ForecastingPipeline
from kalimati_tarkari.logger import logging
from flask_cors import CORS
from retrain import Retrain
from fetch_db import FetchDB

# Disable TensorFlow OneDNN optimizations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


# Function to run train_check continuously in the background
def continuous_training_check(interval=55):  # Run every 55 seconds by default
    while True:
        try:
            
            retrain = Retrain()
            retrain.train_check()
        except Exception as e:
            print(f"Error in continuous training check: {e}")
        time.sleep(interval)

app = Flask(__name__)
CORS(app)

@app.route('/forecast', methods=['GET'])
def index():
    if request.method == 'GET':
        try:
            # Fetch data from the database
            obj = FetchDB()
            dates, averages = obj.get_data()
            
            # Prepare the response as a dictionary
            response_data = {
                'dates': dates,
                'averages': averages
            }
            
            # Return the data as a JSON response
            return jsonify(response_data)
        except Exception as e:
            print('The Exception message is:', e)
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Start the background thread for continuous training check
    threading.Thread(target=continuous_training_check, args=(55,), daemon=True).start()
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=4000, debug=True)
