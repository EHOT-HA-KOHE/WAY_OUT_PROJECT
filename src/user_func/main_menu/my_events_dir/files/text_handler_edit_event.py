import json

from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, BotCommand)

from locales.locales_texts import return_local_text


def text_handler_edit_event(message, path_to_locales, from_json_data, user_in_db):
    local_mes = return_local_text(user_id=message.chat.id, text="dont_understand_you", locales_dir=path_to_locales)
    main_menu_mes = return_local_text(user_id=message.chat.id, text="main_menu", locales_dir=path_to_locales)
    cancel_mes = return_local_text(user_id=message.chat.id, text="cancel", locales_dir=path_to_locales)
    keyboard = None

    if not from_json_data["title"]:
        print("title")
        from_json_data["title"] = message.text
        from_json_data["description"] = True    # todo
        from_json_data["city"] = True
        from_json_data["max_amount_of_people"] = True
        from_json_data["date"] = True

        json_data = json.dumps(from_json_data)
        user_in_db.statuses_edit_event = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="edit_event_ask_category_name", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("SPORT", callback_data="edit_event_choose_category_SPORT"),
                    InlineKeyboardButton("GAMES", callback_data="edit_event_choose_category_GAMES")
                ],
                [
                    InlineKeyboardButton("COMMUNICATION", callback_data="edit_event_choose_category_COMMUNICATION"),
                    InlineKeyboardButton("TRIPS", callback_data="edit_event_choose_category_TRIPS")
                ],
                [
                    InlineKeyboardButton("LET'S VISIT TOGETHER ...", callback_data="edit_event_choose_category_LET'S_VISIT"),
                    InlineKeyboardButton("OTHER", callback_data="edit_event_choose_category_OTHER")
                 ],
                [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
            ]
        )

    elif not from_json_data["description"]:
        if len(message.text) >= 700:
            local_mes = return_local_text(
                user_id=message.chat.id,
                text="error_edit_event_ask_description",
                locales_dir=path_to_locales
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
                ]
            )
            return local_mes, keyboard

        print("description")
        from_json_data["description"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses_edit_event = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="edit_event_ask_city", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Prague", callback_data="edit_event_choose_city_prague")],
                [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
            ]
        )

    elif not from_json_data["city"]:
        print("city")

        from_json_data["city"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses_edit_event = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="edit_event_ask_max_amount_of_people", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
            ]
        )

    elif not from_json_data["max_amount_of_people"]:
        print("max_amount_of_people")

        try:
            int(message.text)
        except Exception as err:
            local_mes = return_local_text(user_id=message.chat.id, text="error_edit_user_ask_max_amount_of_people", locales_dir=path_to_locales)
            return local_mes, keyboard

        from_json_data["max_amount_of_people"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses_edit_event = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="edit_event_ask_date", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
            ]
        )

    elif not from_json_data["date"]:
        print("date")
        from_json_data["date"] = message.text
        # from_json_data["location"] = False
        json_data = json.dumps(from_json_data)
        user_in_db.statuses_edit_event = json_data
        #
        # local_mes = return_local_text(user_id=message.chat.id, text="edit_event_ask_location", locales_dir=path_to_locales)
        # keyboard = InlineKeyboardMarkup(
        #     [
        #         [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
        #     ]
        # )

        local_mes = return_local_text(user_id=message.chat.id, text="edit_event_ask_make_group", locales_dir=path_to_locales)
        # cancel_mes = return_local_text(user_id=message.chat.id, text="cancel", locales_dir=path_to_locales)
        yes_button = return_local_text(user_id=message.chat.id, text="yes", locales_dir=path_to_locales)
        no_button = return_local_text(user_id=message.chat.id, text="no", locales_dir=path_to_locales)

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(no_button, callback_data="edit_event_choose_make_group_no"),
                    InlineKeyboardButton(yes_button, callback_data="edit_event_choose_make_group_yes"),
                ],
                [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
            ]
        )

    return local_mes, keyboard
