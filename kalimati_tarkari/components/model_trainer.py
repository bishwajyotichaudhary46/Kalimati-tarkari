from sklearn.preprocessing import StandardScaler
import pandas as pd
from kalimati_tarkari.logger import logging
import joblib
import numpy as np
import os

# Deep learning
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Flatten, Convolution1D, RepeatVector, TimeDistributed
from sklearn.preprocessing import StandardScaler

from kalimati_tarkari.config.configuration import ModelTrainerConfig

class HybridModel:

    def __init__(self, config = ModelTrainerConfig):
        self.config = config

    def noramalizing_data(self):

        scaler = StandardScaler()

        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)
        train_data.drop(columns=['Date'], inplace=True)
        test_data.drop(columns=['Date'], inplace=True)
        train_data = scaler.fit_transform(train_data.values.reshape(-1,1))

        test_data = scaler.transform(test_data.values.reshape(-1,1))
        joblib.dump(scaler, self.config.Potato)
        #print(test_data)
        return  test_data,train_data
    # Here we will use previous one 60 days as features and next day as output or target
    # Preparing Train dataset

    def train_spliting(self,train):
        window_size = 60
        # Creating a data structure with 60 timesteps and 1 output
        X_train = []
        y_train = []
        for i in range(window_size, train.shape[0]):
            X_train.append(train[i-window_size:i]) 
            y_train.append(train[i, -1]) # consider Close as target
        # Change them to numpy array
        X_train, y_train = np.array(X_train).astype('float32'), np.array(y_train).reshape(-1,1)
        logging.info("Success training data fully spliting")
        return X_train,y_train
    
    # Preparing Test dataset

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
    
    
        
   
    def model_trainer(self,X_train, y_train):

        model = Sequential()

        # First Conv1D layer with input shape (timesteps, features)
        model.add(Convolution1D(filters=self.config.filters, kernel_size=self.config.kernel_size, activation=self.config.activation,  input_shape=(X_train[1,:].shape)))

        # Second Conv1D layer
        model.add(Convolution1D(filters=self.config.filters, kernel_size=self.config.kernel_size, activation=self.config.activation))

        # Flatten before the LSTM
        model.add(Flatten())

        model.add(RepeatVector(y_train.shape[1]))
        # LSTM layer that does not return sequences
        model.add(LSTM(128, activation=self.config.activation))

        # Dense layer for output
        model.add(Dense(100, activation=self.config.activation))

        # Final Dense layer to predict a single value (for each sample)
        model.add(Dense(1))

        # Compile the model
        model.compile(loss=self.config.loss, optimizer=self.config.optimizer)
        logging.info("Model Training start")
        # Fit the model
        model.fit(X_train, y_train, epochs=self.config.epoch, batch_size=self.config.batch_size)
        logging.info("Model Trained Sucessfully")
        model.summary()
        tf.saved_model.save(model, os.path.join(self.config.root_dir, self.config.Potato))
        logging.info(" Model  save suceessfully!  ")
        return model

        

    

    

