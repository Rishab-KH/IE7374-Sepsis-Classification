#Import libraries
import pandas as pd
import numpy as np
from pathlib import Path

# Custom imports
import utils.config as config
from utils.log_config import setup_logging
from utils.data_validation import generate_and_save_schema_and_stats, validate_data

# Logger setup for schema and stats validation
# DATA_DIR = config.DATA_DIR
STATS_SCHEMA_FILE = config.STATS_SCHEMA_FILE


logger = setup_logging(config.PROJECT_ROOT, "schema_stats_utils.py")

def schema_stats_gen(ti):
    try:
        df=pd.read_csv(ti.xcom_pull('get_data_location'), sep=",")
        logger.info(f"Data loaded successfully.")
    except FileNotFoundError as e:
        logger.error(f"File not found: {ti.xcom_pull('get_data_location')}. Error: {e}")
        raise ValueError("Failed to Load Data for Schema and Statstics Validation. Stopping DAG execution.")

    generation_result=generate_and_save_schema_and_stats(df, STATS_SCHEMA_FILE)
    if not generation_result:
        raise ValueError("Schema and Statstics Generation failed. Stopping DAG execution.")

def schema_and_stats_validation(ti):
    data_dir = ti.xcom_pull('get_data_location')
    try:
        df=pd.read_csv(data_dir, sep=",")
        logger.info(f"Data loaded successfully.")
    except FileNotFoundError as e:
        logger.error(f"File not found: {ti.xcom_pull('get_data_location')}. Error: {e}")
        raise ValueError("Failed to Load Data for Schema and Statstics Validation. Stopping DAG execution.")
    validation_result, validation_message = validate_data(df)
    ti.xcom_push(key='validation_message', value=validation_message)
    if validation_result:
        if "batch" in data_dir: # If we have batch-x in gs:// that means we are running retrain pipeline
            return ["download_data","download_scaler","download_latest_model"]
        else:
            return 'data_processing_and_saving.train_test_split'
    return 'prepare_email_content'