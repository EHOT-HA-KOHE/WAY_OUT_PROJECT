import json

from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from src.db.models import Event, User, Category

from src.user_func.show_events import show_event_after_creating
from src.user_func.edit_statuses_for_handler import edit_statuses_in_database
from src.user_func.start_command import return_main_menu
from src.user_func.main_menu.user_profile_dir.user_profile import show_my_profile

from locales.locales_texts import return_local_text


def return_mes_for_callback_user_profile(callback_data, callback_query, db_session, photo,
                                         user, bot,  path_to_locales, chat_id_for_verif):
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
            from_json_data["creator"] = callback_query.from_user.id
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

        elif callback_data[18:29] == "part_prague":
            if len(callback_data) > 29:
                user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
                from_json_data = json.loads(user_in_db.statuses_edit_event)

                from_json_data["location"] = f"Prague {callback_data[30:]}"
                from_json_data["photo"] = False

                json_data = json.dumps(from_json_data)
                user_in_db.statuses_edit_event = json_data

                response_text = return_local_text(user_id=callback_query.from_user.id, text="edit_event_ask_photo",
                                              locales_dir=path_to_locales)
                keyboard = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
                    ]
                )

            else:
                response_text = return_local_text(user_id=callback_query.from_user.id, text="edit_event_ask_location_prague", locales_dir=path_to_locales)
                back_button = return_local_text(user_id=callback_query.from_user.id, text="back_button", locales_dir=path_to_locales)

                temp_keyboard = [
                    [InlineKeyboardButton(f"Prague all", callback_data="edit_event_choose_part_prague_all")],
                    [
                        InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel"),
                        InlineKeyboardButton(back_button, callback_data="edit_event_cancel")
                    ],
                ]

                counter = 0
                row = []
                for prague_num in range(1, 13):
                    row.append(InlineKeyboardButton(f"Praha {prague_num}", callback_data=f"edit_event_choose_part_prague_{prague_num}"))
                    if prague_num % 3 == 0:
                        temp_keyboard.insert(counter, row)
                        counter += 1
                        row = []

                keyboard = InlineKeyboardMarkup(temp_keyboard)

        elif callback_data[18:28] == "make_group":
            user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
            from_json_data = json.loads(user_in_db.statuses_edit_event)
            from_json_data["make_group"] = callback_data[29:]
            from_json_data["location"] = False

            temp_keyboard = [
                    [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
                ]

            response_text = return_local_text(user_id=callback_query.from_user.id, text="edit_event_ask_location", locales_dir=path_to_locales)
            if from_json_data["city"] == "prague":
                response_text = return_local_text(user_id=callback_query.from_user.id, text="edit_event_ask_location_prague", locales_dir=path_to_locales)
                part_of_prague = return_local_text(user_id=callback_query.from_user.id, text="part_of_prague_button", locales_dir=path_to_locales)
                temp_keyboard.insert(0, [InlineKeyboardButton(part_of_prague, callback_data="edit_event_choose_part_prague")])

            json_data = json.dumps(from_json_data)
            user_in_db.statuses_edit_event = json_data

            keyboard = InlineKeyboardMarkup(temp_keyboard)

            # temp_mes = return_local_text(
            #     user_id=callback_query.from_user.id,
            #     text="edit_event_approve_changes_text",
            #     locales_dir=path_to_locales
            # )
            # approve_button = return_local_text(user_id=callback_query.from_user.id, text="publish", locales_dir=path_to_locales)
            # cancel_mes = return_local_text(user_id=callback_query.from_user.id, text="cancel", locales_dir=path_to_locales)
            #
            # event_info = f'Title: {from_json_data["title"]}\n' \
            #              f'Category: {from_json_data["category_name"]}\n' \
            #              f'Description: {from_json_data["description"]}\n' \
            #              f'City: {from_json_data["city"]}\n' \
            #              f'Max amount of people: {from_json_data["max_amount_of_people"]}\n' \
            #              f'Date: {from_json_data["date"]}\n' \
            #              f'Location: {from_json_data["location"]}\n' \
            #
            # response_text = f"{event_info}\n\n{temp_mes}"
            # keyboard = InlineKeyboardMarkup(
            #     [
            #         [InlineKeyboardButton(approve_button, callback_data="edit_event_approve_changes")],
            #         [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
            #     ]
            # )

        else:
            print("err_find_in_code")

    elif callback_data[11:] == "approve_changes":
        user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
        from_json_data = json.loads(user_in_db.statuses_edit_event)

        all_data_received = all([i for i in from_json_data.values()])

        if all_data_received:


            # category = db_session.query(Category).filter_by(name=from_json_data["category_name"]).first()
            # if category is None:
            #     category = Category(name=from_json_data["category_name"])
            #     db_session.add(category)

            creator = db_session.query(User).filter_by(tg_id=callback_query.from_user.id).first()
            # photo = from_json_data["photo"]
            # print(type(user_in_db.statuses_edit_event))

            event = Event(
                creator=creator,
                # title=from_json_data["title"],
                # language='ru',
                # description=from_json_data["description"],
                # city=from_json_data["city"],
                # max_amount_of_people=from_json_data["max_amount_of_people"],
                # date=from_json_data["date"],
                # photo=photo,
                # location=from_json_data["location"],
                temp_info=user_in_db.statuses_edit_event
            )

            # db_session.add(event)
            db_session.add_all([event, creator])
            # event.categories.append(category)
            # event.attendees.append(user_in_db)

            edit_statuses_in_database(status=True, reason="event", message=callback_query.message, db_session=db_session, user=user)

            # response_text, keyboard = show_event_after_creating(  # todo dont del !!!!!!
            #     user_id=callback_query.from_user.id,
            #     db_session=db_session,
            #     event_id=event.id,
            #     path_to_locales=path_to_locales
            # )
            event_info_for_verif = f'title = {from_json_data["title"]} \n' \
                                   f'description = {from_json_data["description"]} \n' \
                                   f'city = {from_json_data["city"]} \n' \
                                   f'category = {from_json_data["category_name"]} \n' \
                                   f'max_amount_of_people = {from_json_data["max_amount_of_people"]} \n' \
                                   f'make_group: {from_json_data["make_group"]}\n'\
                                   f'date = {from_json_data["date"]} \n' \
                                   f'location = {from_json_data["location"]}' \

            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(f"Опубликовать", callback_data=f"verif_event_publish_{event.id}")],
                    [InlineKeyboardButton(f"Отклонить", callback_data=f"verif_event_rejectt_{event.id}")],
                ]
            )

            bot.send_photo(
                chat_id=chat_id_for_verif,
                photo=from_json_data["photo"],
                caption=event_info_for_verif,
                reply_markup=keyboard
            )
            # print(chat_id_for_verif)

            response_text = return_local_text(
                user_id=callback_query.from_user.id,
                text="your_event_has_been_sent_to_verif",
                locales_dir=path_to_locales
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")],
                ]
            )

        else:
            response_text = "err"
            # main_menu = return_local_text(user_id=callback_query.from_user.id, text="main_menu", locales_dir=path_to_locales)
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
