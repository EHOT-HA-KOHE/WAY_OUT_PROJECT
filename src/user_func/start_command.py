from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from src.user_func.main_menu.user_profile_dir.files.change_language import update_user
from src.user_func.main_menu.user_profile_dir.files.edit_user_profile import change_statuses_in_database

from locales.locales_texts import return_local_text


def start_register_new_user(tg_id: int, message, db_session, user, path_to_locales):
    update_user(tg_id=tg_id, language=message.from_user.language_code, db_session=db_session, user=user)
    change_statuses_in_database(status=True, message=message, db_session=db_session, user=user)

    local_mes = return_local_text(
        user_id=tg_id,
        text="start_register_message",
        locales_dir=path_to_locales
    )

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Yes", callback_data="registration_start")],
            [InlineKeyboardButton("Do this later", callback_data="registration_reject")]
        ]
    )

    return local_mes, keyboard


def return_main_menu(user_id: int, path_to_locales):
    local_mes = return_local_text(user_id=user_id, text="start_message", locales_dir=path_to_locales)

    my_actions = return_local_text(user_id=user_id, text="main_menu_my_actions", locales_dir=path_to_locales)
    wayout_events = return_local_text(user_id=user_id, text="main_menu_wayout_events", locales_dir=path_to_locales)
    users_events = return_local_text(user_id=user_id, text="main_menu_users_events", locales_dir=path_to_locales)
    user_profile = return_local_text(user_id=user_id, text="main_menu_user_profile", locales_dir=path_to_locales)
    # partners_events = return_local_text(user_id=user_id, text="my_actions", locales_dir=path_to_locales)
    # hot_events = return_local_text(user_id=user_id, text="my_actions", locales_dir=path_to_locales)

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{my_actions}", callback_data=f"main_menu_my_actions")],
            [InlineKeyboardButton(f"{wayout_events}", callback_data=f"main_menu_wayout_events")],
            [InlineKeyboardButton(f"{users_events}", callback_data=f"main_menu_users_events")],
            [InlineKeyboardButton(f"{user_profile}", callback_data=f"main_menu_user_profile")],
        ]
    )

    return local_mes, keyboard
