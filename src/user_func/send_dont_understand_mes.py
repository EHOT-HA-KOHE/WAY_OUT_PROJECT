import time

from locales.locales_texts import return_local_text


def send_dont_understand_mes(user_id, bot, path_to_locales):
    local_mes = return_local_text(user_id=user_id, text="dont_understand_you", locales_dir=path_to_locales)
    mes_to_del = bot.send_message(chat_id=user_id, text=local_mes)
    time.sleep(1.5)
    bot.delete_messages(chat_id=user_id, message_ids=mes_to_del.id)