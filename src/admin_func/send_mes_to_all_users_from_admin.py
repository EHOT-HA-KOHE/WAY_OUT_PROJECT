import json

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, InputMediaPhoto
from pyrogram.enums import ParseMode

from locales.locales_texts import return_local_text


def send_mes_to_all_users_from_admin(bot, db_session, db_user, path_to_locales):
    users = db_session.query(db_user).all()

    for user in users:
        main_menu = return_local_text(user_id=user.tg_id, text="main_menu", locales_dir=path_to_locales)

        response_text, photo, link = return_data_to_send_mes_to_users_from_admin()

        temp_keyboard = [
            [InlineKeyboardButton(main_menu, callback_data="main_menu")],
        ]

        if link != "0":
            follow_button = return_local_text(user_id=user.tg_id, text="follow_button", locales_dir=path_to_locales)
            temp_keyboard.insert(0, [InlineKeyboardButton(follow_button, url=link)])

        keyboard = InlineKeyboardMarkup(temp_keyboard)
        try:
            bot.edit_message_media(
                chat_id=user.tg_id,
                message_id=int(user.start_mes_id),
                media=InputMediaPhoto(photo, caption=response_text),
                reply_markup=keyboard,
            )
        except Exception as err:
            ...


def return_data_to_send_mes_to_users_from_admin():
    with open("./src/admin_func/data_for_sending_mes_to_users_from_admin.json", "r") as file:
        data = json.load(file)

    response_text = data["description"]
    link = data["link"]
    photo = data["photo"]

    return response_text, photo, link


def start_creating_mes_to_send_users_from_admin():
    response_text = "Start creating message to send to all users?"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Start", callback_data="creating_message_to_send_to_all_users_start")]])

    return response_text, keyboard


def gather_data_to_send_mes_to_users_from_admin(bot, chat_id, action, mes_id):
    with open("./src/admin_func/data_for_sending_mes_to_users_from_admin.json", "r") as file:
        data = json.load(file)

    if action == "start":
        data["mes_id"] = mes_id
        data["description"] = False
        data["link"] = False
        data["photo"] = False

    elif action == "cancel":
        data["description"] = True
        data["link"] = True
        data["photo"] = True
        bot.delete_messages(chat_id=chat_id, message_ids=int(data["mes_id"]))
        data["mes_id"] = True

    with open("./src/admin_func/data_for_sending_mes_to_users_from_admin.json", "w") as file:
        json.dump(data, file, indent=4)


def text_handler_to_data_to_send_mes_to_users_from_admin(text, bot, message):
    with open("./src/admin_func/data_for_sending_mes_to_users_from_admin.json", "r") as file:
        data = json.load(file)

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="creating_message_to_send_to_all_users_cancel")]])
    response_text = "err"
    mes_id = data["mes_id"]

    if not data["description"] or not data["link"]:
        if not data["description"]:
            data["description"] = f"{text}"
            response_text = "Send link or send 0"

        elif not data["link"]:
            data["link"] = f"{text}"
            response_text = "Send photo"

        # bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)
        with open("./src/admin_func/data_for_sending_mes_to_users_from_admin.json", "w") as file:
            json.dump(data, file, indent=4)

    else:
        keyboard = None

    return response_text, keyboard, mes_id


def photo_handler_to_data_to_send_mes_to_users_from_admin(chat_id, photo, bot, message):
    with open("./src/admin_func/data_for_sending_mes_to_users_from_admin.json", "r") as file:
        data = json.load(file)

    mes_id = data["mes_id"]
    description = data["description"]
    link = data["link"]

    if not data["photo"]:
        data["photo"] = f"{photo}"

        # with open("./src/admin_func/data_for_sending_mes_to_users_from_admin.json", "w") as file:
        #     json.dump(data, file, indent=4)

        bot.delete_messages(
            chat_id=chat_id,
            message_ids=[mes_id, message.id],
            # text=response_text,
            # reply_markup=keyboard,
        )

        temp_keyboard = [
            [InlineKeyboardButton("Publish", callback_data=f"creating_message_to_send_to_all_users_publish")],
            [InlineKeyboardButton("Cancel", callback_data=f"creating_message_to_send_to_all_users_cancel")],
        ]

        if link != "0":
            temp_keyboard.insert(0, [InlineKeyboardButton("Link", url=link)])

        keyboard = InlineKeyboardMarkup(temp_keyboard)

        temp_mes = bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=f"{description}\n\nТак будет выглядеть готовое сообщение 👆",
            reply_markup=keyboard,
            disable_notification=True,
            parse_mode=ParseMode.HTML
        )

        data["mes_id"] = f"{temp_mes.id}"

        with open("./src/admin_func/data_for_sending_mes_to_users_from_admin.json", "w") as file:
            json.dump(data, file, indent=4)


def callback_handler_to_data_to_send_mes_to_users_from_admin(callback, bot, db_session, db_user, path_to_locales):
    if callback.data[38:] == "start":
        gather_data_to_send_mes_to_users_from_admin(bot=bot, chat_id=callback.message.chat.id, action="start", mes_id=callback.message.id)

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cancel", callback_data="creating_message_to_send_to_all_users_cancel")]])

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text="Send text for message",
            reply_markup=keyboard,
        )

    elif callback.data[38:] == "cancel":
        gather_data_to_send_mes_to_users_from_admin(bot=bot, chat_id=callback.message.chat.id, action="cancel", mes_id="0")

    elif callback.data[38:] == "publish":
        send_mes_to_all_users_from_admin(bot, db_session, db_user, path_to_locales)

        with open("./src/admin_func/data_for_sending_mes_to_users_from_admin.json", "r") as file:
            data = json.load(file)

        mes_id = data["mes_id"]
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="Объявление было отправлено всем пользователям",
            reply_to_message_id=int(mes_id),
            parse_mode=ParseMode.HTML
        )
    # else:
    #     ...
