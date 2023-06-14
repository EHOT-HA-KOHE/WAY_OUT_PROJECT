from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from pyrogram.errors import UserPrivacyRestricted

from src.db.models import Event, User, Category
from locales.locales_texts import return_local_text


def add_or_del_user_on_or_from_event(action, client_chat_creator, user_id, event_id, db_session, path_to_locales):
    user_in_db = db_session.query(User).filter(User.tg_id == user_id).first()
    event = db_session.query(Event).filter_by(id=event_id).first()

    if action == "add":
        event.attendees.append(user_in_db)
        db_session.commit()
        # client_chat_creator.start()
        if event.group_id is not None:
            try:
                client_chat_creator.add_chat_members(chat_id=event.group_id, user_ids=user_id)

            # except Exception as e:
            #     # Отлов любой ошибки и сохранение информации об ошибке в переменную e
            #     print(f"Произошла ошибка: {type(e).__name__}")
            except UserPrivacyRestricted as err:
                print(f"UserPrivacyRestricted: {err}")

            except Exception as err:
                print(err)
        # client_chat_creator.stop()

        response_text = return_local_text(user_id=user_id, text="user_successfully_added_to_the_event",
                                          locales_dir=path_to_locales)

    elif action == "del":
        event.attendees.remove(user_in_db)
        db_session.commit()
        response_text = return_local_text(user_id=user_id, text="user_successfully_del_from_the_event",
                                          locales_dir=path_to_locales)

    else:
        response_text = return_local_text(user_id=user_id, text="err", locales_dir=path_to_locales)
        keyboard = None
        return response_text, keyboard

    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
        ]
    )

    return response_text, keyboard

