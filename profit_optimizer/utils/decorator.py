from datetime import datetime
from functools import wraps

from .logger import logger


def timing_decorator(algorithm_name: str):
    """
    A decorator to measure the execution time of a function and log relevant details,
    specifically tailored for algorithms. It logs the start time, end time, and total
    execution time in seconds using the provided `algorithm_name`.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("=" * 80)
            start_time = datetime.now()
            logger.info(f"Running {algorithm_name} algorithm at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 80)

            # Exécuter la fonction
            result = func(*args, **kwargs)

            # Afficher les informations de fin
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            print("=" * 80)
            logger.info(f"{algorithm_name} algorithm ends at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"Running time: {execution_time:.4f} seconds")
            print("=" * 80)

            return result

        return wrapper

    return decorator
