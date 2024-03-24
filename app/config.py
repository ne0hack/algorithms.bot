import os
from sys import stdout

from loguru import logger

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logger.remove()
logger.add(stdout, format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {name}: {message}")
