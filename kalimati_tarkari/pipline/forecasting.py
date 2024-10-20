from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import tensorflow as tf
from kalimati_tarkari.logger import logging
from pathlib import Path

class ForecastingPipeline:
    def __init__(self):
        # Load the model
        self.model = tf.saved_model.load(Path("artifacts/model_trainer/artifacts/model_trainer/Potato"))
        
        # Load train and test data
        self.test = pd.read_csv(Path("artifacts/data_spliting/test.csv"))
        self.train = pd.read_csv(Path("artifacts/data_spliting/train.csv"))
    
    def normalize_data(self):
        scaler = StandardScaler()

        # Load train and test data
        train_data = self.train
        test_data = self.test

        # Drop 'Date' column
        train_data.drop(columns=['Date'], inplace=True)
        test_data.drop(columns=['Date'], inplace=True)

        # Fit scaler to training data
        train_data_scaled = scaler.fit_transform(train_data.values)

        # Apply the same transformation to the test data
        test_data_scaled = scaler.transform(test_data.values)

        return test_data_scaled, train_data_scaled, scaler
    
    def forecasts(self, X_test, n_steps=60, forecast_length=30):
        # Get the last window from X_test to start forecasting
        x_input = X_test[-1].reshape(1, -1)

        # Convert the input into a list for ease of extending
        temp_input = list(x_input)
        temp_input = temp_input[0].tolist()

        # List to store forecasted values
        lst_output = []

        # Access the prediction function from the loaded model
        predict_function = self.model.signatures["serving_default"]

        i = 0
        while i < forecast_length:
            if len(temp_input) > n_steps:
                # Adjust the input to only keep the last 'n_steps' elements
                x_input = np.array(temp_input[-n_steps:])
                x_input = x_input.reshape(1, n_steps, 1)
                print('lst_out',lst_output)
                x_input = tf.constant(x_input, dtype=tf.float32)
                # Predict the next value using the model

                y_hat = predict_function(tf.constant(x_input))['output_0']
                # Extend the temporary input list with the predicted value
                temp_input.extend(y_hat.numpy()[0])

                # Store the predicted value in the output list
                lst_output.append(y_hat.numpy()[0][0])

            else:
                # Reshape input properly for the LSTM model
                x_input = x_input.reshape((1, n_steps, 1))
                x_input = tf.constant(x_input, dtype=tf.float32)
                y_hat = predict_function(tf.constant(x_input))['output_0']
                temp_input.extend(y_hat.numpy()[0])
                lst_output.append(y_hat.numpy()[0][0])
            i += 1

        
        return lst_output

    
    def test_splitting(self, train, test):
        window_size = 60

        # Concatenate train and test data
        dataset_total = np.concatenate((train, test), axis=0)

        # Prepare input data
        inputs = dataset_total[len(dataset_total) - len(test) - window_size:]
        X_test = []
        y_test = []

        # Prepare test data windows
        for i in range(window_size, window_size + len(test)):
            X_test.append(inputs[i - window_size:i, :])
            y_test.append(inputs[i, -1])  # Assuming last column is the target

        # Convert to numpy arrays
        X_test, y_test = np.array(X_test).astype('float32'), np.array(y_test).reshape(-1, 1)

        return X_test, y_test
