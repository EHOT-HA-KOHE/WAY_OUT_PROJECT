import json

from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from locales.locales_texts import return_local_text


def accept_photo_for_edit_user(message, from_json_data, user_in_db, path_to_locales):
    response_text = return_local_text(user_id=message.chat.id, text="dont_understand_you", locales_dir=path_to_locales)
    keyboard = None

    if not from_json_data["photo"]:
        print("photo")
        from_json_data["photo"] = message.photo.file_id
        json_data = json.dumps(from_json_data)
        user_in_db.statuses_edit_user = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="edit_user_finish_register",
                                      locales_dir=path_to_locales)

        approve_mes = return_local_text(user_id=message.chat.id, text="approve_changes", locales_dir=path_to_locales)
        cancel_mes = return_local_text(user_id=message.chat.id, text="cancel", locales_dir=path_to_locales)

        user_profile = f'Name: {from_json_data["name"]}\n' \
                       f'Sex: {from_json_data["sex"]}\n' \
                       f'Age: {from_json_data["age"]}\n' \
                       f'City: {from_json_data["city"]}\n' \
                       f'Info: {from_json_data["info"]}\n' \

        response_text = f"{local_mes}\n\n{user_profile}"

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(approve_mes, callback_data="registration_approve_changes")],
                [InlineKeyboardButton(cancel_mes, callback_data="registration_cancel")],
            ]
        )

    return response_text, keyboard
