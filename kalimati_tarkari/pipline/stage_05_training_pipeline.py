from kalimati_tarkari.config.configuration import ConfigurationManager
from kalimati_tarkari.components.model_trainer import HybridModel
from kalimati_tarkari.logger import logging




class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_config = config.get_model_trainer_config()
        trainer = HybridModel(config=data_config)
        train, test = trainer.noramalizing_data()
        X_train,y_train =  trainer.train_spliting(train)
        X_test, y_test = trainer.test_spliting(train,test)
        model = trainer.model_trainer(X_train,y_train)

