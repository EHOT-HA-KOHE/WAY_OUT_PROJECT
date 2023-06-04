from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from src.db.models import Event, User, Category

from locales.locales_texts import return_local_text


def return_event_info_and_photo(db_session, event_id):
    temp_event = db_session.query(Event).filter_by(id=event_id).first()
    event_category = temp_event.categories[0].name

    attendees = temp_event.attendees
    attendee_ids = [user.tg_id for user in attendees]
    amount_of_people = f"{len(attendee_ids)}/{temp_event.max_amount_of_people}"

    event_info = f'**Title:** {temp_event.title}\n' \
                 f'**Category:** {event_category}\n' \
                 f'**Description:** {temp_event.description}\n' \
                 f'**City:** {temp_event.city}\n' \
                 f'**Amount of people:** {amount_of_people}\n' \
                 f'**Date:** {temp_event.date}\n' \
                 f'**Location:** {temp_event.location}\n' \

    photo = temp_event.photo

    return event_info, photo, amount_of_people


def show_event_after_creating(user_id, db_session, event_id: int, path_to_locales):
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
        ]
    )

    temp_mes = return_local_text(user_id=user_id, text="successfully_completed_event_creation", locales_dir=path_to_locales)
    event_info, photo, amount_of_people = return_event_info_and_photo(db_session, event_id)
    response_text = f"{event_info}\n\n{temp_mes}"

    return response_text, keyboard


def show_events_created_by_user(user_id, event_id, path_to_locales, db_session, photo):
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)

    user = db_session.query(User).filter_by(tg_id=user_id).first()
    user_events = user.events_created

    events_ids = [event.id for event in user_events]
    events_ids.sort(reverse=True)

    if len(events_ids) != 0:
        if event_id == "":
            event_id = events_ids[0]
        index = events_ids.index(int(event_id))
        back_button_number = events_ids[index - 1]
        if index == (len(events_ids) - 1):
            next_button_number = events_ids[0]
        else:
            next_button_number = events_ids[index + 1]

        event_info, photo, amount_of_people = return_event_info_and_photo(db_session, event_id)
        del_event_mes = return_local_text(user_id=user_id, text="delete_button", locales_dir=path_to_locales)

        if len(events_ids) == 1:
            temp_mes = return_local_text(user_id=user_id, text="list_of_events_the_user_created_one_event", locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(del_event_mes, callback_data=f"main_menu_my_events_i_created_delete_event_{event_id}")],
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        else:
            temp_mes = return_local_text(user_id=user_id, text="list_of_events_the_user_created", locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(del_event_mes, callback_data=f"main_menu_my_events_i_created_delete_event_{event_id}")],
                    [
                        InlineKeyboardButton(f"<--", callback_data=f"main_menu_my_events_i_created_{back_button_number}"),
                        InlineKeyboardButton(f"-->", callback_data=f"main_menu_my_events_i_created_{next_button_number}")
                    ],
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        response_text = f"{event_info}\n\n{temp_mes}\n**{index+1}/{len(events_ids)}**"

    else:
        response_text = return_local_text(user_id=user_id, text="you_dont_have_created_events", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
            ]
        )

    return response_text, keyboard, photo


def delete_event(user_id, event_id, path_to_locales, db_session):
    temp_mes = return_local_text(user_id=user_id, text="are_you_sure_you_want_to_delete_the_event", locales_dir=path_to_locales)

    event_info, photo, amount_of_people = return_event_info_and_photo(db_session, event_id)
    response_text = f"{event_info}\n\n{temp_mes}"

    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)
    back_button = return_local_text(user_id=user_id, text="back_button", locales_dir=path_to_locales)
    del_button = return_local_text(user_id=user_id, text="delete_button", locales_dir=path_to_locales)

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(del_button, callback_data=f"main_menu_my_events_i_created_delete_event_del_{event_id}")],
            [InlineKeyboardButton(back_button, callback_data=f"main_menu_my_events_i_created_{event_id}")],
            [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
        ]
    )

    return response_text, keyboard, photo


def delete_event_from_db(user_id, event_id, path_to_locales, db_session):
    event = db_session.query(Event).filter_by(id=event_id).first()
    event_category = event.categories[0].name
    db_session.delete(event)

    events = db_session.query(Event.id).join(Event.categories).filter(Category.name == event_category).first()

    if events is None:
        category = db_session.query(Category).filter_by(name=event_category).first()
        db_session.delete(category)

    response_text = return_local_text(user_id=user_id, text="event_has_been_successfully_deleted", locales_dir=path_to_locales)

    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
        ]
    )

    return response_text, keyboard


def show_events_the_user_joined(user_id, event_id, path_to_locales, db_session, photo):
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)

    user = db_session.query(User).filter_by(tg_id=user_id).first()
    attended_events = user.events_attended

    events_ids = [event.id for event in attended_events]
    events_ids.sort(reverse=True)

    if len(events_ids) != 0:
        if event_id == "":
            event_id = events_ids[0]
        index = events_ids.index(int(event_id))
        back_button_number = events_ids[index - 1]
        if index == (len(events_ids) - 1):
            next_button_number = events_ids[0]
        else:
            next_button_number = events_ids[index + 1]

        event_info, photo, amount_of_people = return_event_info_and_photo(db_session, event_id)
        leave_event_mes = return_local_text(user_id=user_id, text="leave_button", locales_dir=path_to_locales)

        if len(events_ids) == 1:
            temp_mes = return_local_text(user_id=user_id, text="list_of_events_the_user_joined_one_event",
                                         locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(leave_event_mes, callback_data=f"add_or_del_user_on_or_from_event_del_{event_id}")],
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        else:
            temp_mes = return_local_text(user_id=user_id, text="list_of_events_the_user_joined",
                                         locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(leave_event_mes, callback_data=f"add_or_del_user_on_or_from_event_del_{event_id}")],
                    [
                        InlineKeyboardButton(f"<--", callback_data=f"main_menu_my_events_i_joined_{back_button_number}"),
                        InlineKeyboardButton(f"-->", callback_data=f"main_menu_my_events_i_joined_{next_button_number}")
                    ],
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        response_text = f"{event_info}\n\n{temp_mes}\n**{index+1}/{len(events_ids)}**"

    else:
        response_text = return_local_text(user_id=user_id, text="you_dont_have_joined_to_events", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
            ]
        )

    return response_text, keyboard, photo
