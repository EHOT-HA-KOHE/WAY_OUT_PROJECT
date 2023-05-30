import json

from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, BotCommand)

from locales.locales_texts import return_local_text


def text_handler(message, path_to_locales, from_json_data, user_in_db):
    local_mes = return_local_text(user_id=message.chat.id, text="dont_understand_you", locales_dir=path_to_locales)
    keyboard = None
    cancel_mes = return_local_text(user_id=message.chat.id, text="cancel", locales_dir=path_to_locales)

    if not from_json_data["name"]:
        print("name")
        from_json_data["name"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="ask_sex", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("men", callback_data="registration_choose_sex_men"),
                    InlineKeyboardButton("women", callback_data="registration_choose_sex_women")
                ],
                [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")],
            ]
        )

    elif not from_json_data["sex"]:
        print("sex")
        from_json_data["sex"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="ask_age", locales_dir=path_to_locales)

    elif not from_json_data["age"]:
        print("age")

        try:
            int(message.text)
        except Exception as err:
            local_mes = return_local_text(user_id=message.chat.id, text="error_age", locales_dir=path_to_locales)
            return local_mes, keyboard

        from_json_data["age"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="ask_city", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Prague", callback_data="registration_choose_city_prague")],
                # [InlineKeyboardButton("Another", callback_data="registration_enter_city")],
                [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")],
            ]
        )

    elif not from_json_data["city"]:
        print("city")
        from_json_data["city"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="ask_info", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")],
            ]
        )

    elif not from_json_data["info"]:
        print("info")
        from_json_data["info"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="ask_photo", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")],
            ]
        )

    # elif not from_json_data["photo"]:
    #     print("photo")
    #     from_json_data["photo"] = message.text
    #     json_data = json.dumps(from_json_data)
    #     user_in_db.statuses = json_data
    #
    #     local_mes = return_local_text(
    #         user_id=message.chat.id,
    #         text="finish_register",
    #         locales_dir=path_to_locales
    #     )

    return local_mes, keyboard
