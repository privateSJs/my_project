import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# Path to file -> data.yaml
DATASET_DIR = BASE_DIR / "training" / "yolo" / "datasets"
YOLO_CONFIG_DIR = DATASET_DIR / "data.yaml"
TRAIN_DIR = DATASET_DIR / "train" / "images"
VAL_DIR = DATASET_DIR / "valid" / "images"
TEST_DIR = DATASET_DIR / "test" / "images"
SAVE_TRAINED_PATH = DATASET_DIR / "runs" / "detect"
MODEL_TRAINED_FILE = DATASET_DIR / "runs" / "detect" / "train" / "weights" / "best.pt"

# Configuration for logger and path to file -> logger
LOGS_DIR = BASE_DIR / "utils" / "logs"
LAST_HISTORY_LOGS = LOGS_DIR / "last_run.logs"
FULL_HISTORY_LOGS = LOGS_DIR / "full_run.logs"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [Module: %(module)s, in function: %(funcName)s] - %(message)s"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
## Log level value returning
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# Path to assets with prediction product
PREDICT_DIR = BASE_DIR / "assets" / "resized"

