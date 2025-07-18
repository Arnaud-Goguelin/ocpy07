import csv
import os

from profit_optimizer.utils import DataFilesNames, DataValidationError, logger
from .action import Action


class Data:

    def __init__(self):
        self.actions: set = set()
        self.data_folder = "profit_optimizer/data"

    def _validate_directory_and_files(self):
        """
        Validates the existence of the data directory and required files within it.

        :raises FileNotFoundError: If the data directory does not exist or if any required
            files are missing.
        :return: None
        """

        if not os.path.exists(self.data_folder):
            raise DataValidationError(f"Folder '{self.data_folder}' does not exist.")

        missing_files = set()

        for file_name in DataFilesNames:
            file_path = os.path.join(self.data_folder, file_name.value)
            if not os.path.exists(file_path):
                missing_files.add(file_name.value)

        if missing_files:
            raise DataValidationError(f"Missing files: {', '.join(missing_files)}.")
        print()
        logger.info("Data directory and files validated.")

    def load(self):
        """
        Loads data from a CSV file in the configured directory and stores self.data.

        :raises FileNotFoundError: If the directory or file is not found.
        :raises ValueError: If the file format is not compatible.
        :return: None
        """
        try:
            self._validate_directory_and_files()
        except DataValidationError as error:
            logger.error(error)
            return

        file_path = os.path.join(self.data_folder, DataFilesNames.actions.value)

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # read first line and ignore it => skip headers
            next(reader)

            self.actions = {
                Action(
                    name=row["Actions"],
                    cost=row["Cost"],
                    profitability=row["Profitability"],
                )
                for row in reader
            }

        logger.info(f"Data loaded from '{file_path}' - {len(self.actions)} rows loaded.")
