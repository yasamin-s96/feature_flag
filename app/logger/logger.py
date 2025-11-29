import logging
from logging.handlers import TimedRotatingFileHandler

from pythonjsonlogger.json import JsonFormatter

from app.core.settings import settings

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

formatter = JsonFormatter("{asctime}:{levelname}:{name}:{message}", style="{")

handler = TimedRotatingFileHandler(
    filename=f"{settings.core.LOCAL_STORAGE_PATH}/logs/app.log",
    when="midnight",
    interval=1,
    encoding="utf-8",
    backupCount=7,
)

handler.setFormatter(formatter)


if __name__ == "__main__":
    logger.info("hi")