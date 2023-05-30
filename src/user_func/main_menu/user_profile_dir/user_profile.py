from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from src.user_func.main_menu.user_profile_dir.files.edit_user_profile import change_statuses_in_database

from locales.locales_texts import return_local_text


def show_my_profile(user_id, db_session, user, path_to_locales):
    user_in_db = db_session.query(user).filter(user.tg_id == user_id).first()
    mes = return_local_text(
        user_id=user_id,
        text="user_info",
        locales_dir=path_to_locales
    )

    account_info = f'Name: {user_in_db.name}\n'\
                   f'Sex: {user_in_db.sex}\n'\
                   f'Age: {user_in_db.age}\n'\
                   f'City: {user_in_db.city}\n'\
                   f'Info: {user_in_db.info}\n' \

    response_text = f"**{mes}**\n\n{account_info}"

    edit_profile = return_local_text(user_id=user_id, text="edit_profile", locales_dir=path_to_locales)
    change_language = return_local_text(user_id=user_id, text="change_language", locales_dir=path_to_locales)
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{edit_profile}", callback_data="main_menu_user_profile_edit_profile")],
            [InlineKeyboardButton(f"{change_language}", callback_data="main_menu_user_profile_change_language")],
            [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")]
        ]
    )
    
    return response_text, keyboard


def edit_user_data(callback_query, db_session, user, path_to_locales):
    change_statuses_in_database(status=False, message=callback_query.message, db_session=db_session, user=user)

    cancel_mes = return_local_text(user_id=callback_query.from_user.id, text="cancel", locales_dir=path_to_locales)
    response_text = return_local_text(user_id=callback_query.from_user.id, text="ask_name", locales_dir=path_to_locales)
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{callback_query.from_user.first_name}",
                    callback_data=f"registration_choose_name_{callback_query.from_user.first_name}"
                )
            ],
            # [InlineKeyboardButton("Choose another", callback_data="registration_enter_name")],
            [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")]
        ]
    )

    return response_text, keyboard


def change_interface_language(user_id, path_to_locales):
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)

    response_text = return_local_text(user_id=user_id, text="select_language", locales_dir=path_to_locales)
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("RU", callback_data="change_lang_ru"),
                InlineKeyboardButton("UA", callback_data="change_lang_ua")
            ],
            [InlineKeyboardButton("EN", callback_data="change_lang_en")],
            [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
        ]
    )

    return response_text, keyboard
