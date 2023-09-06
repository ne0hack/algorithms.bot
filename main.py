import os
import time
from sys import stdout

from telebot import TeleBot
from loguru import logger

from src.data import get_solved_algorithms, get_unsolved_algorithms
from src.messages import clear_chat, algorithms_list_message, start_page_message

logger.remove()
logger.add(stdout, format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {name}: {message}")

bot = TeleBot(os.getenv("TELEGRAM_BOT_TOCKEN"))
admin_id = int(os.getenv("ADMIN_ID"))
usolved_algorithms = get_unsolved_algorithms(solved_algorithms=get_solved_algorithms())
page_options = {"page": -1, "limit": 10, "data": [], "color": ""}


@bot.message_handler(commands=["start"])
def start_page(request):
    global page_options

    if int(request.from_user.id) == admin_id:
        page_options["page"] = -1
        clear_chat(bot_conn=bot, chat_id=request.chat.id, message_id=request.message_id)
        message, markup = start_page_message()
        bot.send_message(request.from_user.id, message, reply_markup=markup)


@bot.message_handler(commands=["update"])
def update_algorithms(request):
    logger.debug("algorithm database update")
    global usolved_algorithms, page_options

    if int(request.from_user.id) == admin_id:
        page_options["page"] = -1
        clear_chat(bot_conn=bot, chat_id=request.chat.id, message_id=request.message_id)

        message = "Updating data... Please wait!"
        bot.send_message(request.from_user.id, message)

        usolved_algorithms = get_unsolved_algorithms(solved_algorithms=get_solved_algorithms())
        bot.delete_message(request.from_user.id, request.message_id + 1)

        start_page(request)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global page_options

    if "lvl" in call.data:
        lvl = call.data.split("_")[-1]
        lvl_color = {"easy": "🟢", "medium": "🟠", "hard": "🔴"}

        page_options["page"] = 1
        page_options["color"] = lvl_color[lvl]
        page_options["data"].clear()
        for i in range(0, len(usolved_algorithms[lvl]), page_options["limit"]):
            page_options["data"].append(usolved_algorithms[lvl][i : i + page_options["limit"]])

        message, markup = algorithms_list_message(page_options=page_options)
        bot.edit_message_text(
            chat_id=call.from_user.id,
            text=message,
            message_id=call.message.id,
            reply_markup=markup,
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )

    elif "next" in call.data or "prev" in call.data:
        if call.data == "prev_page":
            if page_options["page"] != 1:
                page_options["page"] -= 1
            else:
                page_options["page"] = len(page_options["data"])
        else:
            if len(page_options["data"]) == page_options["page"]:
                page_options["page"] = 1
            else:
                page_options["page"] += 1

        try:
            message, markup = algorithms_list_message(page_options=page_options)
            bot.edit_message_text(
                chat_id=call.from_user.id,
                text=message,
                message_id=call.message.id,
                reply_markup=markup,
                parse_mode="Markdown",
                disable_web_page_preview=True,
            )
        except IndexError:
            message = "An index error occurred, try restarting!"
            bot.send_message(chat_id=call.from_user.id, text=message)


@bot.message_handler(content_types=["text", "sticker", "photo", "audio"])
def messages_from_user(request):
    if request.content_type == "text" and request.text.strip().isdigit() and page_options["page"] != -1:
        user_to_page = int(request.text.strip())
        if 0 < user_to_page <= len(page_options["data"]):
            page_options["page"] = user_to_page
            message, markup = algorithms_list_message(page_options=page_options)
            bot.send_message(
                request.from_user.id,
                message,
                reply_markup=markup,
                parse_mode="Markdown",
                disable_web_page_preview=True,
            )
            clear_chat(bot_conn=bot, chat_id=request.chat.id, message_id=request.message_id)
        else:
            bot.delete_message(request.from_user.id, request.message_id)
    else:
        bot.delete_message(request.from_user.id, request.message_id)


if __name__ == "__main__":
    logger.debug("bot has been started")
    while True:  # currently a necessary measure, until found a solution to the problem of falling during stagnation
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as error:
            logger.error(repr(error))
            time.sleep(60)
