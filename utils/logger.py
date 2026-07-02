import logging
import os


LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(

    filename=os.path.join(LOG_DIR, "shopsmart.log"),

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)


logger = logging.getLogger("ShopSmart")


def info(message):

    logger.info(message)


def warning(message):

    logger.warning(message)


def error(message):

    logger.error(message)