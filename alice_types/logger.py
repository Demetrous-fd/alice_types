import sys

from loguru import logger

logger.add(sys.stdout, format="<green>{time}</green> {level} : {message}", filter="alice_types", level="INFO", enqueue=True)
logger.add(sys.stderr, format="<red>{time}</red> {level} : {message}", filter="alice_types", level="INFO", enqueue=True)
