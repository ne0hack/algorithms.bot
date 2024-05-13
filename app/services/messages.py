from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_page_message() -> (str, InlineKeyboardMarkup):
    """
    Forms the start menu of the message
    """
    message = "Choose the level of complexity of the algorithms:"

    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="🟢 Easy", callback_data="lvl_easy")
    btn2 = InlineKeyboardButton(text="🟠 Medium", callback_data="lvl_medium")
    btn3 = InlineKeyboardButton(text="🔴 Hard", callback_data="lvl_hard")
    markup.add(btn1, btn2, btn3)

    return message, markup


def algorithms_list_message(page_options: dict) -> (str, InlineKeyboardMarkup):
    """
    Returns the generated list of algorithms in Markdown format
    """
    if not page_options["data"]:
        message = "All algorithms of this level have been solved! 🎉"
        return message, None

    message = "Unsolved algorithms:\n"
    for algorithm in page_options["data"][page_options["page"] - 1]:
        message += page_options["color"] + " [" + algorithm["title"].strip() + "]" + "(" + algorithm["link"] + ")\n\n"

    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="◀️", callback_data="prev_page")
    btn2 = InlineKeyboardButton(text=f"{page_options['page']}/{len(page_options['data'])}", callback_data="cnt_page")
    btn3 = InlineKeyboardButton(text="▶️", callback_data="next_page")
    markup.add(btn1, btn2, btn3)

    return message, markup
