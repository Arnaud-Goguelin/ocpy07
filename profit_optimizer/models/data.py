import csv
import os

from profit_optimizer.utils import DATA_FILE_FORMAT, DataFilesNames, DataValidationError, logger
from .action import Action


class Data:

    def __init__(self, file_name: str = DataFilesNames.test.value):
        self.actions: set = set()
        self.data_folder = "profit_optimizer/data"
        self.file_name = f"{file_name}.{DATA_FILE_FORMAT}"

    def _validate_directory_and_files(self):
        """
        Validates the existence of the data directory and required files within it.

        :raises FileNotFoundError: If the data directory does not exist or if any required
            files are missing.
        :return: None
        """

        if not os.path.exists(self.data_folder):
            raise DataValidationError(f"Folder '{self.data_folder}' does not exist.")

        file_path = os.path.join(self.data_folder, self.file_name)
        if not os.path.exists(file_path):
            raise DataValidationError(f"Missing files: {self.file_name}")
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

        file_path = os.path.join(self.data_folder, self.file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # read first line and ignore it => skip headers
            next(reader)

            # using a set allows us to delete duplicate Action (cf. __eq__ method in Action model)
            # this avoids to analyze many times the same actions in algorithms
            actions_set = set()
            errors_count = 0

            for row in reader:
                try:
                    new_action = Action(
                        name=row["Action"],
                        cost=row["Cost"],
                        profitability=row["Profitability"],
                    )
                    if new_action:
                        actions_set.add(new_action)

                except (TypeError, ValueError) as error:
                    logger.warning(f"Action {row["Action"]} ignored, error while reading CSV file: {error}")
                    errors_count += 1

        self.actions = actions_set
        logger.info(
            f"Data loaded from '{file_path}' - {len(self.actions)} rows loaded. {errors_count} errors ignored."
        )
