import json

from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from src.db.models import Event, User, Category

from src.user_func.show_events import show_event_after_creating
from src.user_func.edit_statuses_for_handler import edit_statuses_in_database
from src.user_func.start_command import return_main_menu
from src.user_func.main_menu.user_profile_dir.user_profile import show_my_profile

from locales.locales_texts import return_local_text


def return_mes_for_callback_user_profile(callback_data, callback_query, db_session, photo, user, path_to_locales):
    response_text = return_local_text(
        user_id=callback_query.from_user.id,
        text="unknown_button",
        locales_dir=path_to_locales
    )
    main_menu = return_local_text(user_id=callback_query.from_user.id, text="main_menu", locales_dir=path_to_locales)
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{main_menu}", callback_data="edit_event_cancel")],
        ]
    )

    cancel_mes = return_local_text(user_id=callback_query.from_user.id, text="cancel", locales_dir=path_to_locales)

    if callback_data[11:17] == "choose":
        if callback_data[18:22] == "city":
            user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
            from_json_data = json.loads(user_in_db.statuses_edit_event)

            from_json_data["city"] = callback_data[23:]
            json_data = json.dumps(from_json_data)
            user_in_db.statuses_edit_event = json_data

            response_text = return_local_text(
                user_id=callback_query.from_user.id,
                text="edit_event_ask_max_amount_of_people",
                locales_dir=path_to_locales
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
                ]
            )

        elif callback_data[18:26] == "category":
            user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
            from_json_data = json.loads(user_in_db.statuses_edit_event)

            from_json_data["category_name"] = callback_data[27:]
            from_json_data["description"] = False  # todo
            from_json_data["city"] = False
            from_json_data["max_amount_of_people"] = False
            from_json_data["date"] = False

            json_data = json.dumps(from_json_data)
            user_in_db.statuses_edit_event = json_data

            response_text = return_local_text(user_id=callback_query.from_user.id, text="edit_event_ask_description", locales_dir=path_to_locales)
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
                ]
            )

        else:
            print("err_find_in_code")

    elif callback_data[11:] == "approve_changes":
        user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
        from_json_data = json.loads(user_in_db.statuses_edit_event)

        all_data_received = all([i for i in from_json_data.values()])

        if all_data_received:
            category = db_session.query(Category).filter_by(name=from_json_data["category_name"]).first()

            if category is None:
                category = Category(name=from_json_data["category_name"])
                db_session.add(category)

            creator = db_session.query(User).filter_by(tg_id=callback_query.from_user.id).first()
            photo = from_json_data["photo"]

            event = Event(
                creator=creator,
                title=from_json_data["title"],
                language='ru',
                description=from_json_data["description"],
                city=from_json_data["city"],
                max_amount_of_people=from_json_data["max_amount_of_people"],
                date=from_json_data["date"],
                photo=photo,
                location=from_json_data["location"],
                temp_info=''
            )

            db_session.add_all([event, creator])
            event.categories.append(category)
            event.attendees.append(user_in_db)

            edit_statuses_in_database(status=True, reason="event", message=callback_query.message, db_session=db_session, user=user)

            response_text, keyboard = show_event_after_creating(
                user_id=callback_query.from_user.id,
                db_session=db_session,
                event_id=event.id,
                path_to_locales=path_to_locales
            )

        else:
            response_text = "err"
            main_menu = return_local_text(user_id=callback_query.from_user.id, text="main_menu", locales_dir=path_to_locales)
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(f"{main_menu}", callback_data="edit_event_cancel")],
                ]
            )

        user_in_db.status = ""

    elif callback_data[11:] == "cancel":
        edit_statuses_in_database(status=True, reason="event", message=callback_query.message, db_session=db_session, user=user)
        user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
        user_in_db.status = ""
        response_text, keyboard = return_main_menu(user_id=callback_query.from_user.id, path_to_locales=path_to_locales)

    else:
        response_text = "find_this_mes_in_code_ctrl+F"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
            ]
        )

    db_session.commit()
    
    return response_text, keyboard, photo
