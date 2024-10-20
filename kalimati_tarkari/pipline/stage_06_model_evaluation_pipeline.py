from kalimati_tarkari.config.configuration import ConfigurationManager
from kalimati_tarkari.components.model_evaluation import ModelEvaluation
from kalimati_tarkari.logger import logging




class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        config = config.get_model_evaluation_config()
        eval = ModelEvaluation(config=config)
        train,test = eval.noramalizing_data()
        X_test, y_test = eval.test_spliting(train,test)
        logging.info(f"Evaluation Metrics ")
        eval.eval(X_test,y_test)