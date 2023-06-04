from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from locales.locales_texts import return_local_text
from src.user_func.edit_statuses_for_handler import edit_statuses_in_database


def return_my_events_buttons(user_id, path_to_locales):
    response_text = return_local_text(user_id=user_id, text="main_menu_my_events_text", locales_dir=path_to_locales)
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)
    i_created = return_local_text(user_id=user_id, text="i_created", locales_dir=path_to_locales)
    i_joined = return_local_text(user_id=user_id, text="i_joined", locales_dir=path_to_locales)
    create_new = return_local_text(user_id=user_id, text="create_new", locales_dir=path_to_locales)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(i_created, callback_data="main_menu_my_events_i_created_"),
                InlineKeyboardButton(i_joined, callback_data="main_menu_my_events_i_joined_")
            ],
            [InlineKeyboardButton(create_new, callback_data="main_menu_my_events_create_event")],
            [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
        ]
    )

    return response_text, keyboard


def start_register_user_event(callback_query, path_to_locales, db_session, user):
    user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
    user_in_db.status = "edit_event"
    response_text = return_local_text(user_id=callback_query.from_user.id, text="edit_event_ask_title", locales_dir=path_to_locales)
    cancel_mes = return_local_text(user_id=callback_query.from_user.id, text="cancel", locales_dir=path_to_locales)

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
        ]
    )

    edit_statuses_in_database(
        status=False,
        reason="event",
        message=callback_query.message,
        db_session=db_session,
        user=user
    )

    return response_text, keyboard
