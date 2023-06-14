from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from src.db.models import Event, User, Category
from locales.locales_texts import return_local_text


def show_event_location(chat_id, id_for_locales, message_id, event_id, db_session, bot, path_to_locales):
    if event_id == "del":
        bot.delete_messages(chat_id=chat_id, message_ids=message_id)
        return

    temp_event = db_session.query(Event).filter_by(id=event_id).first()
    temp_location = temp_event.location.split("_")
    hide_button = return_local_text(user_id=id_for_locales, text="hide_button", locales_dir=path_to_locales)

    if temp_location[3] != "nodata":
        bot.send_venue(
            chat_id=chat_id,
            latitude=float(temp_location[1]),
            longitude=float(temp_location[2]),
            title=temp_location[3],
            address=temp_location[4],
            reply_to_message_id=message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(hide_button, callback_data=f"show_event_location_del")],
                ]
            )
        )

    else:
        bot.send_location(
            chat_id=chat_id,
            latitude=float(temp_location[1]),
            longitude=float(temp_location[2]),
            reply_to_message_id=message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(hide_button, callback_data=f"show_event_location_del")],
                ]
            )
        )
