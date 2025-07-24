from enum import Enum

SCALE_FACTOR = 100

DATA_FILE_FORMAT = "csv"


class DataFilesNames(str, Enum):
    test = "dataset_test"
    dataset_1 = "dataset_1"
    dataset_2 = "dataset_2"
