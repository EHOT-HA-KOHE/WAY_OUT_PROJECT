import random

from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from src.db.models import Event, User, Category
from src.user_func.show_events import return_event_info_and_photo
from locales.locales_texts import return_local_text
from src.user_func.edit_statuses_for_handler import edit_statuses_in_database


def pars_users_events_callback_data(user_id, callback_data, db_session, path_to_locales, photo):
    if callback_data[23:33] == "categories":
        if callback_data[34:38] == "show":
            response_text, keyboard, photo = return_users_events_by_category(
                user_id=user_id,
                db_session=db_session,
                photo=photo,
                event_id=callback_data[39:],
                path_to_locales=path_to_locales
            )

        else:
            response_text, keyboard = return_users_events_categories_buttons(user_id, db_session, path_to_locales)

    elif callback_data[23:] == "dates":
        response_text, keyboard = return_users_events_buttons(user_id, path_to_locales)

    elif callback_data[23:35] == "random_event":
        response_text, keyboard, photo = return_users_events_random_event(
            user_id=user_id,
            random_event_id=callback_data[36:],
            db_session=db_session,
            photo=photo,
            path_to_locales=path_to_locales
        )

    else:
        response_text, keyboard = return_users_events_buttons(user_id, path_to_locales)

    return response_text, keyboard, photo


def return_users_events_buttons(user_id, path_to_locales):
    response_text = return_local_text(user_id=user_id, text="main_menu_users_events_text", locales_dir=path_to_locales)
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)
    categories = return_local_text(user_id=user_id, text="main_menu_users_events_categories_button", locales_dir=path_to_locales)
    dates = return_local_text(user_id=user_id, text="main_menu_users_events_dates_button", locales_dir=path_to_locales)
    random_event = return_local_text(user_id=user_id, text="main_menu_users_events_random_event_button", locales_dir=path_to_locales)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(categories, callback_data="main_menu_users_events_categories"),
                InlineKeyboardButton(dates, callback_data="main_menu_users_events_dates")
            ],
            [InlineKeyboardButton(random_event, callback_data="main_menu_users_events_random_event_")],
            [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
        ]
    )

    return response_text, keyboard


def return_users_events_categories_buttons(user_id, db_session, path_to_locales):
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)
    response_text = return_local_text(user_id=user_id, text="choose_category_of_users_events_for_filter", locales_dir=path_to_locales)

    categories = db_session.query(Category).all()
    category_names = [category.name for category in categories]

    if len(category_names) == 0:
        response_text = return_local_text(user_id=user_id, text="events_dosent_exist", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],])
        return response_text, keyboard

    if "WAY_OUT" in category_names:
        category_names.remove("WAY_OUT")

    buttons = []
    row = []

    for index, category_name in enumerate(category_names):
        event_ids = (db_session.query(Event.id).join(Event.categories).filter(Category.name == category_name).all())
        events_ids = [event_id[0] for event_id in event_ids]
        events_ids.sort(reverse=True)

        row.append(InlineKeyboardButton(f"{category_name}", callback_data=f"main_menu_users_events_categories_show_{events_ids[0]}"))
        if index % 2 != 0 and index != 0 or index == len(category_names) - 1:
            buttons.append(row)
            row = []

    buttons.append([InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")])
    keyboard = InlineKeyboardMarkup(buttons)

    return response_text, keyboard


def return_users_events_by_category(user_id, db_session, photo, event_id, path_to_locales):
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)

    temp_event = db_session.query(Event).filter_by(id=int(event_id)).first()
    event_category = temp_event.categories[0].name
    event_ids = db_session.query(Event.id).join(Event.categories).filter(Category.name == event_category).all()
    events_ids = [event_id[0] for event_id in event_ids]

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
        join_button = return_local_text(user_id=user_id, text="join_button", locales_dir=path_to_locales)

        if len(events_ids) == 1:
            temp_mes = return_local_text(user_id=user_id, text="list_of_events_filter_category_one_event",
                                         locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(join_button, callback_data=f"add_or_del_user_on_or_from_event_add_{event_id}")],
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        else:
            temp_mes = return_local_text(user_id=user_id, text="list_of_events_filter_category",
                                         locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(join_button, callback_data=f"add_or_del_user_on_or_from_event_add_{event_id}")],
                    [
                        InlineKeyboardButton(f"<--", callback_data=f"main_menu_users_events_categories_show_{back_button_number}"),
                        InlineKeyboardButton(f"-->", callback_data=f"main_menu_users_events_categories_show_{next_button_number}")
                    ],
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        response_text = f"{event_info}\n\n{temp_mes} {event_category}\n{index+1}/{len(events_ids)}"

    else:
        response_text = return_local_text(user_id=user_id, text="you_dont_have_created_events", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
            ]
        )

    return response_text, keyboard, photo


def return_users_events_random_event(user_id, random_event_id, db_session, photo, path_to_locales):
    main_menu = return_local_text(user_id=user_id, text="main_menu", locales_dir=path_to_locales)

    temp_events_ids = db_session.query(Event.id).all()
    events_ids = [event_id[0] for event_id in temp_events_ids]

    if len(events_ids) != 0:
        join_button = return_local_text(user_id=user_id, text="join_button", locales_dir=path_to_locales)
        if random_event_id == "":
            random_event_id = random.choice(events_ids)
        event_info, photo, amount_of_people = return_event_info_and_photo(db_session, random_event_id)

        if len(events_ids) == 1:
            temp_mes = return_local_text(user_id=user_id, text="list_of_random_events_one_event", locales_dir=path_to_locales)
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(join_button, callback_data=f"add_or_del_user_on_or_from_event_add_{random_event_id}")],
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        else:
            temp_mes = return_local_text(user_id=user_id, text="list_of_random_events", locales_dir=path_to_locales)
            another_button = return_local_text(user_id=user_id, text="another_button", locales_dir=path_to_locales)

            events_ids.remove(int(random_event_id))
            next_random_event_id = random.choice(events_ids)

            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(join_button, callback_data=f"add_or_del_user_on_or_from_event_add_{random_event_id}")],
                    [InlineKeyboardButton(another_button,
                                          callback_data=f"main_menu_users_events_random_event_{next_random_event_id}")],
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        response_text = f"{event_info}\n\n{temp_mes} {len(events_ids)+1}"

    else:
        response_text = return_local_text(user_id=user_id, text="events_dosent_exist", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],])
        return response_text, keyboard, photo

    return response_text, keyboard, photo
