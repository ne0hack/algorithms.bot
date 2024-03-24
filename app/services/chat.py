from telebot.apihelper import ApiTelegramException


def clear_chat(bot_conn, chat_id: int, message_id: int, num_mes_clear: int = 4) -> None:
    """Clears previous messages up to `num_mes_clear`"""
    for shift in range(num_mes_clear):
        try:
            bot_conn.delete_message(chat_id, message_id - shift)
        except ApiTelegramException:
            pass
