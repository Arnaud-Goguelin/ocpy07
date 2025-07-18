import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        # display in terminal
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
