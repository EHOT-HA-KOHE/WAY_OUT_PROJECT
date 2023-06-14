from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from src.db.models import Event, User, Category

from locales.locales_texts import return_local_text


def return_user_info_and_photo(db_session, user_id, creator_id, photo):
    temp_user = db_session.query(User).filter_by(tg_id=user_id).first()

    user_info = f'**Name:** {temp_user.name}\n' \
                f'**Sex:** {temp_user.sex}\n' \
                f'**Age:** {temp_user.age}\n' \
                f'**City:** {temp_user.city}\n' \
                f'**Info:** {temp_user.info}\n' \

    if int(user_id) == creator_id:
        user_info = f"**This is the event CREATOR** 😎 \n\n" + user_info

    temp_photo = temp_user.photo
    if temp_photo != "":
        photo = temp_photo

    return user_info, photo


def return_creator_of_event(event_id, db_session, callback_data_for_back_button, photo_main_menu, path_to_locales):
    # if callback_data_for_back_button[:32] == "main_menu_users_events_from_last":
    #     callback_data_for_back_button += f"_{user_id}"

    event = db_session.query(Event).filter_by(id=event_id).first()

    response_text, photo = return_user_info_and_photo(
        db_session=db_session,
        user_id=event.creator.tg_id,
        creator_id=event.creator.tg_id,
        photo=photo_main_menu
    )

    main_menu = return_local_text(user_id=event.creator.tg_id, text="main_menu", locales_dir=path_to_locales)
    back_button = return_local_text(user_id=event.creator.tg_id, text="back_button", locales_dir=path_to_locales)
    write_button = return_local_text(user_id=event.creator.tg_id, text="write_button", locales_dir=path_to_locales)

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{write_button}", user_id=event.creator.tg_id)],
            [
                InlineKeyboardButton(f"{main_menu}", callback_data="main_menu"),
                InlineKeyboardButton(back_button, callback_data=f"{callback_data_for_back_button}")
            ],
        ]
    )

    return response_text, keyboard, photo


def return_users_list_for_users_events_from_last(user_id_locales, db_session, photo, event_id_and_user_id, path_to_locales):
    main_menu = return_local_text(user_id=user_id_locales, text="main_menu", locales_dir=path_to_locales)

    event_id, user_id = event_id_and_user_id.split("_")

    event = db_session.query(Event).filter_by(id=event_id).first()
    joined_users_list = event.attendees
    users_ids = [user_profile.tg_id for user_profile in joined_users_list]
    users_ids.sort(reverse=True)

    if len(users_ids) != 0:
        if user_id == "":
            user_id = users_ids[0]
        index = users_ids.index(int(user_id))
        back_button_number = users_ids[index - 1]
        if index == (len(users_ids) - 1):
            next_button_number = users_ids[0]
        else:
            next_button_number = users_ids[index + 1]

        user_info, photo = return_user_info_and_photo(db_session, user_id, event.creator.tg_id, photo)
        back_button = return_local_text(user_id=user_id_locales, text="back_button", locales_dir=path_to_locales)

        if len(users_ids) == 1:
            temp_mes = return_local_text(user_id=user_id_locales, text="list_of_events_from_last_one_event",
                                         locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    # [InlineKeyboardButton(back_button, callback_data=f"main_menu_users_events_from_last_show_events_{event_id}")],
                    [
                        InlineKeyboardButton(f"{main_menu}", callback_data="main_menu"),
                        InlineKeyboardButton(back_button, callback_data=f"main_menu_users_events_from_last_show_events_{event_id}")
                    ],
                ]
            )

        else:
            temp_mes = return_local_text(user_id=user_id_locales, text="list_of_events_from_last",
                                         locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"<--", callback_data=f"main_menu_users_events_from_last_show_users_{event_id}_{back_button_number}"),
                        InlineKeyboardButton(f"-->", callback_data=f"main_menu_users_events_from_last_show_users_{event_id}_{next_button_number}")
                    ],
                    # [InlineKeyboardButton(f"{back_button}", callback_data=f"main_menu_users_events_from_last_show_events_{event_id}")],
                    [
                        InlineKeyboardButton(f"{main_menu}", callback_data="main_menu"),
                        InlineKeyboardButton(f"{back_button}", callback_data=f"main_menu_users_events_from_last_show_events_{event_id}")
                    ],
                ]
            )

        response_text = f"{user_info}\n\n{temp_mes}\n{index+1}/{len(users_ids)}"

    else:
        response_text = return_local_text(user_id=user_id_locales, text="event_have_not_joined_users", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
            ]
        )

    return response_text, keyboard, photo


def return_users_list_for_my_events_created_by_user(user_id_locales, db_session, photo, event_id_and_user_id, path_to_locales):
    main_menu = return_local_text(user_id=user_id_locales, text="main_menu", locales_dir=path_to_locales)

    event_id, user_id = event_id_and_user_id.split("_")

    event = db_session.query(Event).filter_by(id=event_id).first()
    joined_users_list = event.attendees
    users_ids = [user_profile.tg_id for user_profile in joined_users_list]
    users_ids = users_ids[::-1]
    # users_ids.sort(reverse=True)

    if len(users_ids) != 0:
        if user_id == "":
            user_id = users_ids[0]
        index = users_ids.index(int(user_id))
        back_button_number = users_ids[index - 1]
        if index == (len(users_ids) - 1):
            next_button_number = users_ids[0]
        else:
            next_button_number = users_ids[index + 1]

        user_info, photo = return_user_info_and_photo(db_session, user_id, event.creator.tg_id, photo)
        back_button = return_local_text(user_id=user_id_locales, text="back_button", locales_dir=path_to_locales)

        if len(users_ids) == 1:
            temp_mes = return_local_text(user_id=user_id_locales, text="list_of_events_from_last_one_event",
                                         locales_dir=path_to_locales)

            temp_keyboard = [
                # [InlineKeyboardButton(back_button, callback_data=f"main_menu_my_events_i_created_{event_id}")],
                [
                    InlineKeyboardButton(f"{main_menu}", callback_data="main_menu"),
                    InlineKeyboardButton(back_button, callback_data=f"main_menu_my_events_i_created_{event_id}")
                ],
            ]

        else:
            temp_mes = return_local_text(user_id=user_id_locales, text="list_of_users_who_joined_this_event",
                                         locales_dir=path_to_locales)

            temp_keyboard = [
                [
                    InlineKeyboardButton(f"<--", callback_data=f"main_menu_my_events_i_created_show_users_{event_id}_{back_button_number}"),
                    # InlineKeyboardButton(f"{back_button}", callback_data=f"main_menu_my_events_i_created_{event_id}"),
                    InlineKeyboardButton(f"-->", callback_data=f"main_menu_my_events_i_created_show_users_{event_id}_{next_button_number}")
                ],
                # [InlineKeyboardButton(f"{back_button}", callback_data=f"main_menu_my_events_i_created_{event_id}")],
                [
                    InlineKeyboardButton(f"{main_menu}", callback_data="main_menu"),
                    InlineKeyboardButton(f"{back_button}", callback_data=f"main_menu_my_events_i_created_{event_id}"),
                ],
            ]

        if user_id_locales != int(user_id):
            write_button = return_local_text(user_id=user_id_locales, text="write_button", locales_dir=path_to_locales)
            temp_keyboard.insert(0, [InlineKeyboardButton(f"{write_button}", user_id=user_id)])

        keyboard = InlineKeyboardMarkup(temp_keyboard)
        response_text = f"{user_info}\n\n{temp_mes}\n{index+1}/{len(users_ids)}"

    else:
        response_text = return_local_text(user_id=user_id_locales, text="event_have_not_joined_users", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
            ]
        )

    return response_text, keyboard, photo


def return_users_list_for_my_events_user_joined(user_id_locales, db_session, photo, event_id_and_user_id, path_to_locales):
    main_menu = return_local_text(user_id=user_id_locales, text="main_menu", locales_dir=path_to_locales)

    event_id, user_id = event_id_and_user_id.split("_")

    event = db_session.query(Event).filter_by(id=event_id).first()
    joined_users_list = event.attendees
    users_ids = [user_profile.tg_id for user_profile in joined_users_list]
    users_ids = users_ids[::-1]
    # users_ids.sort(reverse=True)

    if len(users_ids) != 0:
        if user_id == "":
            user_id = users_ids[0]
        index = users_ids.index(int(user_id))
        back_button_number = users_ids[index - 1]
        if index == (len(users_ids) - 1):
            next_button_number = users_ids[0]
        else:
            next_button_number = users_ids[index + 1]

        user_info, photo = return_user_info_and_photo(db_session, user_id, event.creator.tg_id, photo)
        back_button = return_local_text(user_id=user_id_locales, text="back_button", locales_dir=path_to_locales)

        if len(users_ids) == 1:
            temp_mes = return_local_text(user_id=user_id_locales, text="list_of_events_from_last_one_event",
                                         locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    # [InlineKeyboardButton(back_button, callback_data=f"main_menu_my_events_i_joined_{event_id}")],
                    [
                        InlineKeyboardButton(f"{main_menu}", callback_data="main_menu"),
                        InlineKeyboardButton(back_button, callback_data=f"main_menu_my_events_i_joined_{event_id}")
                    ],
                ]
            )

        else:
            temp_mes = return_local_text(user_id=user_id_locales, text="list_of_users_who_joined_this_event", locales_dir=path_to_locales)

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"<--", callback_data=f"main_menu_my_events_i_joined_show_users_{event_id}_{back_button_number}"),
                        # InlineKeyboardButton(f"{back_button}", callback_data=f"main_menu_my_events_i_joined_{event_id}"),
                        InlineKeyboardButton(f"-->", callback_data=f"main_menu_my_events_i_joined_show_users_{event_id}_{next_button_number}")
                    ],
                    # [InlineKeyboardButton(f"{back_button}", callback_data=f"main_menu_my_events_i_joined_{event_id}")],
                    [
                        InlineKeyboardButton(f"{main_menu}", callback_data="main_menu"),
                        InlineKeyboardButton(f"{back_button}", callback_data=f"main_menu_my_events_i_joined_{event_id}"),
                    ],
                ]
            )

        response_text = f"{user_info}\n\n{temp_mes}\n{index+1}/{len(users_ids)}"

    else:
        response_text = return_local_text(user_id=user_id_locales, text="event_have_not_joined_users", locales_dir=path_to_locales)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
            ]
        )

    return response_text, keyboard, photo
