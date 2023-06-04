import json

from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from locales.locales_texts import return_local_text


def accept_photo_for_edit_event(message, from_json_data, user_in_db, path_to_locales):
    response_text = return_local_text(user_id=message.chat.id, text="dont_understand_you", locales_dir=path_to_locales)
    keyboard = None

    if not from_json_data["photo"]:
        from_json_data["photo"] = message.photo.file_id
        json_data = json.dumps(from_json_data)
        user_in_db.statuses_edit_event = json_data

        temp_mes = return_local_text(
            user_id=message.chat.id,
            text="edit_event_approve_changes_text",
            locales_dir=path_to_locales
        )
        approve_button = return_local_text(user_id=message.chat.id, text="publish", locales_dir=path_to_locales)
        cancel_mes = return_local_text(user_id=message.chat.id, text="cancel", locales_dir=path_to_locales)

        event_info = f'Title: {from_json_data["title"]}\n'\
                     f'Category: {from_json_data["category_name"]}\n'\
                     f'Description: {from_json_data["description"]}\n'\
                     f'City: {from_json_data["city"]}\n'\
                     f'Max amount of people: {from_json_data["max_amount_of_people"]}\n'\
                     f'Date: {from_json_data["date"]}\n'\
                     f'Location: {from_json_data["location"]}\n'\

        response_text = f"{event_info}\n\n{temp_mes}"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(approve_button, callback_data="edit_event_approve_changes")],
                [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
            ]
        )

    return response_text, keyboard


def accept_location_for_edit_event(chat_id, from_json_data, path_to_locales):
    ...
