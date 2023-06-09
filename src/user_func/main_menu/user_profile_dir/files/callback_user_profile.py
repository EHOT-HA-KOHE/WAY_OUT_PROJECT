import json

from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from src.user_func.edit_statuses_for_handler import edit_statuses_in_database
from src.user_func.start_command import return_main_menu
from src.user_func.main_menu.user_profile_dir.user_profile import show_my_profile

from locales.locales_texts import return_local_text


def return_mes_for_callback_registration(callback_data, callback_query, db_session, user, path_to_locales):
    response_text = return_local_text(
        user_id=callback_query.from_user.id,
        text="unknown_button",
        locales_dir=path_to_locales
    )
    main_menu = return_local_text(user_id=callback_query.from_user.id, text="main_menu", locales_dir=path_to_locales)
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
        ]
    )

    cancel_mes = return_local_text(user_id=callback_query.from_user.id, text="cancel", locales_dir=path_to_locales)

    if callback_data[13:18] == "enter":
        if callback_data[19:] == "name":
            response_text = return_local_text(
                user_id=callback_query.from_user.id,
                text="edit_user_ask_name",
                locales_dir=path_to_locales
            )
        elif callback_data[19:] == "city":
            response_text = return_local_text(
                user_id=callback_query.from_user.id,
                text="edit_user_ask_city",
                locales_dir=path_to_locales
            )

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")],
            ]
        )

    elif callback_data[13:19] == "choose":
        if callback_data[20:24] == "name":
            user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
            from_json_data = json.loads(user_in_db.statuses_edit_user)

            from_json_data["name"] = callback_data[25:]
            json_data = json.dumps(from_json_data)
            user_in_db.statuses_edit_user = json_data

            response_text = return_local_text(
                user_id=callback_query.from_user.id,
                text="edit_user_ask_sex",
                locales_dir=path_to_locales
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("men", callback_data="registration_choose_sex_men"),
                        InlineKeyboardButton("women", callback_data="registration_choose_sex_women")
                    ],
                    [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")]
                ]
            )

            print(callback_query.message.id)

        elif callback_data[20:23] == "sex":
            user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
            from_json_data = json.loads(user_in_db.statuses_edit_user)

            from_json_data["sex"] = callback_data[24:]
            json_data = json.dumps(from_json_data)
            user_in_db.statuses_edit_user = json_data

            response_text = return_local_text(
                user_id=callback_query.from_user.id,
                text="edit_user_ask_age",
                locales_dir=path_to_locales
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")],
                ]
            )

        elif callback_data[20:24] == "city":
            user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
            from_json_data = json.loads(user_in_db.statuses_edit_user)

            from_json_data["city"] = callback_data[25:]
            json_data = json.dumps(from_json_data)
            user_in_db.statuses_edit_user = json_data

            response_text = return_local_text(
                user_id=callback_query.from_user.id,
                text="edit_user_ask_info",
                locales_dir=path_to_locales
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")],
                ]
            )

    elif callback_data[13:] == "approve_changes":
        user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
        from_json_data = json.loads(user_in_db.statuses_edit_user)

        all_data_received = all([i for i in from_json_data.values()])

        if all_data_received:
            user_in_db.name = from_json_data["name"]
            user_in_db.sex = from_json_data["sex"]
            user_in_db.age = from_json_data["age"]
            user_in_db.city = from_json_data["city"]
            user_in_db.info = from_json_data["info"]
            user_in_db.photo = from_json_data["photo"]

            edit_statuses_in_database(status=True, reason="user", message=callback_query.message, db_session=db_session, user=user)

            response_text, keyboard = show_my_profile(
                user_id=callback_query.from_user.id,
                db_session=db_session,
                user=user,
                path_to_locales=path_to_locales
            )

        else:
            response_text = "err"
            main_menu = return_local_text(user_id=callback_query.from_user.id, text="main_menu", locales_dir=path_to_locales)
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
        user_in_db.status = ""

    elif callback_data[13:] == "cancel":
        edit_statuses_in_database(status=True, reason="user", message=callback_query.message, db_session=db_session, user=user)
        user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()   # todo user_in_db получается в каэжлм if
        user_in_db.status = ""
        response_text, keyboard = return_main_menu(user_id=callback_query.from_user.id, path_to_locales=path_to_locales)

    else:
        response_text = "find_this_mes_in_code_ctrl+F"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")],
            ]
        )

    db_session.commit()
    
    return response_text, keyboard
