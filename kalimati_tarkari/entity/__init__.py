import os
from kalimati_tarkari.constants import *
from dataclasses import dataclass




@dataclass
class DataIngestionConfig:
    root_dir: Path
    local_data_file: Path
    collection_name:str = DATA_INGESTION_COLLECTION_NAME

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    final_data: Path

@dataclass(frozen=True)
class DataSplitingConfig:
    root_dir: Path
    data_path: Path

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    scaler: str
    filters: int
    kernel_size: int
    activation: str
    loss: str
    optimizer: str
    epoch: int
    batch_size: int
    Potato: Path

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    Potato: Path
    scaler: Path