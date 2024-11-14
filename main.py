from kalimati_tarkari.logger import logging
from kalimati_tarkari.exception import KalimatiException
from kalimati_tarkari.pipline.stage_01_dataingestion_pipeline import DataIngestionTrainingPipeline
from kalimati_tarkari.pipline.stage_02_datavalidation import DataValidationTrainingPipeline
from kalimati_tarkari.pipline.stage_03_data_transformation_pipeline import DataTransformationTrainingPipeline
from kalimati_tarkari.pipline.stage_04_dataspliting_pipeline import DataSplitingTrainingPipeline
from kalimati_tarkari.pipline.stage_05_training_pipeline import ModelTrainingPipeline
from kalimati_tarkari.pipline.stage_06_model_evaluation_pipeline import ModelEvaluationPipeline


STAGE_NAME = "Data Ingestion stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logging.info(f">>>>>> stage {STAGE_NAME} sucessfully completed <<<<<<\n\nx==========x")
except Exception as e:
    raise KalimatiException(e)



STAGE_NAME = "Data Validation stage"
if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        datavalidatin = DataValidationTrainingPipeline()
        datavalidatin.main()
        logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        
        raise KalimatiException(e)
    
STAGE_NAME = "Data Transformation stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   datatransformation = DataTransformationTrainingPipeline()
   datatransformation.main()
   logging.info(f">>>>>> stage {STAGE_NAME} sucessfully completed <<<<<<\n\nx==========x")
except Exception as e:
        raise KalimatiException(e)

STAGE_NAME = "Data Spliting stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   dataspliting = DataSplitingTrainingPipeline()
   dataspliting.main()
   logging.info(f">>>>>> stage {STAGE_NAME} sucessfully completed <<<<<<\n\nx==========x")
except Exception as e:
        raise KalimatiException(e)

STAGE_NAME = "Model Training stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   modeltrainer = ModelTrainingPipeline()
   modeltrainer.main()
   logging.info(f">>>>>> stage {STAGE_NAME} sucessfully completed <<<<<<\n\nx==========x")
except Exception as e:
        raise KalimatiException(e)

STAGE_NAME = "Model Evaluation stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   modeleval = ModelEvaluationPipeline()
   modeleval.main()
   logging.info(f">>>>>> stage {STAGE_NAME} sucessfully completed <<<<<<\n\nx==========x")
except Exception as e:
        logging.exception(e)
        raise KalimatiException(e)