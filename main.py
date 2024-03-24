import time

from app.config import logger
from app.controllers import bot

if __name__ == "__main__":
    logger.debug("bot has been successfully started")
    while True:  # currently a necessary measure, until found a solution to the problem of falling during stagnation
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as error:
            logger.error(repr(error))
            time.sleep(60)
