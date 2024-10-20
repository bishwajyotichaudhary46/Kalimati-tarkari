
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import numpy as np

# Deep learning
from sklearn.preprocessing import StandardScaler
from kalimati_tarkari.logger import logging
import tensorflow as tf

from kalimati_tarkari.config.configuration import ModelEvaluationConfig

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config


    def noramalizing_data(self):

        scaler = StandardScaler()

        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)
        train_data.drop(columns=['Date'], inplace=True)
        test_data.drop(columns=['Date'], inplace=True)
        train_data = scaler.fit_transform(train_data.values.reshape(-1,1))

        test_data = scaler.transform(test_data.values.reshape(-1,1))
        return  test_data,train_data

    
    def eval_metrics(self,actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    
    def test_spliting(self,train, test):
        window_size = 60
        # Concatenate train data to test data
        dataset_total = np.concatenate((train, test), axis = 0)
        # Split test data and last window-size of train data
        inputs = dataset_total[len(dataset_total) - len(test) - window_size:]
        # Do the same thing for test data
        X_test = []
        y_test = []
        for i in range(window_size, window_size+len(test)):
            X_test.append(inputs[i-window_size:i,:]) 
            y_test.append(inputs[i,-1]) # consider Close as target
        # Change them to numpy array
        X_test, y_test = np.array(X_test).astype('float32'), np.array(y_test).reshape(-1, 1)
        logging.info(X_test.shape)
    
        return X_test,y_test
    
    

    def eval(self, X_test, y_test):
        try:
            # Load the saved model
            loaded_model = tf.saved_model.load(self.config.Potato)

            # Get the serving function (default signature for inference)
            model = loaded_model.signatures["serving_default"]

            # Make predictions using the loaded model
            test_predict = model(tf.constant(X_test))

            # Print the keys of the prediction output for debugging
            print(f"Available output keys: {test_predict.keys()}")

            # Modify this based on the printed keys (this is just an example)
            # You need to update 'dense' to the correct key based on the output.
            output_key = list(test_predict.keys())[0]  # Just pick the first key for now

            # Extract predictions from the output tensor
            predictions = test_predict[output_key].numpy().squeeze()

            # Calculate evaluation metrics
            rmse, mae, r2 = self.eval_metrics(y_test.squeeze(), predictions)

            # Log the evaluation metrics
            logging.info(f"RMSE: {rmse}, MAE: {mae}, R2: {r2}")

            return rmse, mae, r2

        except Exception as e:
            logging.error(f"Error in model evaluation: {e}")
            return None
        