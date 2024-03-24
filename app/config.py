import os
from sys import stdout

import environ
from loguru import logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env = environ.Env()
env.read_env(env_file=os.path.join(BASE_DIR, "..", ".env"))

TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", default=None)
ADMIN_ID = int(env("ADMIN_ID", default=0))

logger.remove()
logger.add(stdout, format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {name}: {message}")
