import json
import time

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, InputMediaPhoto

from src.db.models import User
from src.db.connection import Session, first_db_connect
from src.user_func.start_command import start_register_new_user, return_main_menu
from src.user_func.send_dont_understand_mes import send_dont_understand_mes

from src.user_func.main_menu.main_menu_callback_handler import main_menu_callback_pars

from src.user_func.main_menu.my_events_dir.files.text_handler_edit_event import text_handler_edit_event
from src.user_func.main_menu.my_events_dir.files.callback_edit_event import return_mes_for_callback_user_profile
from src.user_func.main_menu.my_events_dir.files.photo_and_locacion_handler_edit_event import (
    accept_photo_for_edit_event,
)

from src.user_func.main_menu.user_profile_dir.files.change_language import change_user_language
from src.user_func.main_menu.user_profile_dir.files.text_handler_edit_user import text_handler_edit_user
from src.user_func.main_menu.user_profile_dir.files.photo_handler_edit_user import accept_photo_for_edit_user
from src.user_func.main_menu.user_profile_dir.files.callback_user_profile import return_mes_for_callback_registration

from src.user_func.add_or_del_user_on_or_from_event import add_or_del_user_on_or_from_event
from locales.locales_texts import return_local_text
from locales.texts.apply_changes_in_texts import update_locales_texts


api_id = 21405010
api_hash = 'f02ca9c4a50a86708d782b83682c2327'
bot_token = '6039441521:AAElNiHFFTEu8nM9EWqtdnu17FuSOyUz-40'
CHAT_ID_FOR_VERIF = "-1001967733752"
PATH_TO_LOCALES = "locales/mo_files"
PHOTO_MAIN_MENU = "AgACAgIAAxkBAAIFwWRt4KSe5O284zko1v3teK2caWUTAAJLxTEbTWFxS0qyGrww6LnfAAgBAAMCAAN4AAceBA"

update_locales_texts(path_to_locale_dir=PATH_TO_LOCALES, path_to_texts_dir='locales/texts')
bot = Client("my__bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
first_db_connect()
db_session = Session()


# ============================================


bot.start()
bot.set_bot_commands(
    [
        BotCommand("start", "Главное меню"),
        BotCommand("del_my_account", "del_my_account"),
    ]
)
bot.stop()


@bot.on_message(filters.command("test_com"))
def test_com(bot, message):
    # print(message.chat.id)
    # bot.send_photo(message.chat.id, "AgACAgQAAxkBAAIL22R8rIO38d-P8Hoi06N836H56uvYAAIvwTEb09rgU1Q0r7QK19UNAAgBAAMCAAN5AAceBA")
    ...


@bot.on_message(filters.command("start") & filters.private)
def start(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()

    if user_in_db is None:
        response_text, keyboard = start_register_new_user(
            tg_id=message.chat.id,
            message=message,
            db_session=db_session,
            user=User,
            path_to_locales=PATH_TO_LOCALES
        )

    else:
        response_text, keyboard = return_main_menu(user_id=message.chat.id, path_to_locales=PATH_TO_LOCALES)

    bot.send_photo(
        chat_id=message.chat.id,
        photo=PHOTO_MAIN_MENU,
        caption=response_text,
        reply_markup=keyboard
    )


@bot.on_message(filters.command("del_my_account") & filters.private)
def del_my_account(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()

    db_session.delete(user_in_db)
    db_session.commit()
    bot.send_message(message.chat.id, f"User {message.chat.id} del from db")


# =====================================


@bot.on_message(filters.text & filters.private)
def text_handle(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    # keyboard = None

    if user_in_db.status == "edit_user":
        from_json_data = json.loads(user_in_db.statuses_edit_user)
        local_mes, keyboard = text_handler_edit_user(
            message=message,
            path_to_locales=PATH_TO_LOCALES,
            from_json_data=from_json_data,
            user_in_db=user_in_db
        )

    elif user_in_db.status == "edit_event":
        from_json_data = json.loads(user_in_db.statuses_edit_event)
        local_mes, keyboard = text_handler_edit_event(
            message=message,
            path_to_locales=PATH_TO_LOCALES,
            from_json_data=from_json_data,
            user_in_db=user_in_db
        )

    else:
        send_dont_understand_mes(user_id=message.chat.id, bot=bot, path_to_locales=PATH_TO_LOCALES)
        bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)
        return

    if keyboard is None:
        send_dont_understand_mes(user_id=message.chat.id, bot=bot, path_to_locales=PATH_TO_LOCALES)

    else:
        db_session.commit()
        try:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=from_json_data["mes_id"],
                text=local_mes,
                reply_markup=keyboard,
            )
        except Exception as err:
            send_dont_understand_mes(user_id=message.chat.id, bot=bot, path_to_locales=PATH_TO_LOCALES)

    bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)


# =====================================


@bot.on_callback_query(filters.regex(r'main_menu_.*'))
def handle_main_menu_point(client, callback_query):
    keyboard, response_text, media = main_menu_callback_pars(
        callback_query=callback_query,
        db_session=db_session,
        bot=bot,
        user=User,
        path_to_locales=PATH_TO_LOCALES,
        photo_main_menu=PHOTO_MAIN_MENU,
    )

    try:
        db_session.commit()

        bot.edit_message_media(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.id,
            media=media,
            reply_markup=keyboard,
        )
    except Exception as err:
        try:
            bot.edit_message_text(
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.id,
                text=response_text,
                reply_markup=keyboard,
            )
        except Exception as err:
            ...


@bot.on_callback_query(filters.regex(r'main_menu'))
def handle_main_menu(client, callback_query):
    response_text, keyboard = return_main_menu(user_id=callback_query.from_user.id, path_to_locales=PATH_TO_LOCALES)

    bot.edit_message_media(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.id,
        media=InputMediaPhoto(PHOTO_MAIN_MENU, caption=response_text),
        reply_markup=keyboard,
    )


@bot.on_callback_query(filters.regex(r'add_or_del_user_on_or_from_event_.*'))
def add_or_del_user_on_or_from_event_handler(client, callback_query):
    callback_data = callback_query.data

    response_text, keyboard = add_or_del_user_on_or_from_event(
        action=callback_data[33:36],
        user_id=callback_query.from_user.id,
        event_id=callback_data[37:],
        db_session=db_session,
        path_to_locales=PATH_TO_LOCALES
    )

    if keyboard is None:
        send_dont_understand_mes(user_id=callback_query.from_user.id, bot=bot, path_to_locales=PATH_TO_LOCALES)
        return

    bot.edit_message_media(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.id,
        media=InputMediaPhoto(PHOTO_MAIN_MENU, caption=response_text),
        reply_markup=keyboard,
    )


@bot.on_callback_query(filters.regex(r'registration_.*'))
def handle_registration(client, callback_query):
    callback_data = callback_query.data

    response_text, keyboard = return_mes_for_callback_registration(
        callback_data=callback_data,
        callback_query=callback_query,
        db_session=db_session,
        user=User,
        path_to_locales=PATH_TO_LOCALES
    )

    bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.id,
        text=response_text,
        reply_markup=keyboard,
    )


@bot.on_callback_query(filters.regex(r'edit_event_.*'))
def handle_edit_event(client, callback_query):
    callback_data = callback_query.data

    response_text, keyboard, photo = return_mes_for_callback_user_profile(
        callback_data=callback_data,
        callback_query=callback_query,
        db_session=db_session,
        photo=PHOTO_MAIN_MENU,
        user=User,
        path_to_locales=PATH_TO_LOCALES
    )

    # bot.edit_message_text(
    #     chat_id=callback_query.from_user.id,
    #     message_id=callback_query.message.id,
    #     text=response_text,
    #     reply_markup=keyboard,
    # )

    bot.edit_message_media(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.id,
        media=InputMediaPhoto(photo, caption=response_text),
        reply_markup=keyboard,
    )


@bot.on_callback_query(filters.regex(r'change_lang_..'))
def handle_change_lang(client, callback_query):
    callback_data = callback_query.data

    response_text = change_user_language(
        callback_query=callback_query,
        lang=callback_data[12:],
        db_session=db_session,
        user=User,
        path_to_locales=PATH_TO_LOCALES
    )

    bot.answer_callback_query(callback_query.id, text=response_text, show_alert=True)


@bot.on_callback_query()
def handle_callback_query(client, callback_query):
    response_text = return_local_text(
        user_id=callback_query.from_user.id,
        text=f"unknown_button\n\ncallback_data = {callback_query.data}",
        locales_dir=PATH_TO_LOCALES
    )

    mes_to_del = bot.send_message(callback_query.from_user.id, text=response_text)
    time.sleep(1.5)
    bot.delete_messages(chat_id=mes_to_del.chat.id,message_ids=mes_to_del.id)


# =====================================


@bot.on_message(filters.photo)
def handle_photo(client, message):
    # bot.send_message(message.chat.id, message.photo.file_id)

    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()

    if user_in_db.status == "edit_user":
        from_json_data = json.loads(user_in_db.statuses_edit_user)

        response_text, keyboard = accept_photo_for_edit_user(
            message=message,
            from_json_data=from_json_data,
            user_in_db=user_in_db,
            path_to_locales=PATH_TO_LOCALES
        )

    elif user_in_db.status == "edit_event":
        from_json_data = json.loads(user_in_db.statuses_edit_event)

        response_text, keyboard = accept_photo_for_edit_event(
            message=message,
            from_json_data=from_json_data,
            user_in_db=user_in_db,
            path_to_locales=PATH_TO_LOCALES
        )

    else:
        send_dont_understand_mes(user_id=message.chat.id, bot=bot, path_to_locales=PATH_TO_LOCALES)
        bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)
        return

    if keyboard is None:
        send_dont_understand_mes(user_id=message.chat.id, bot=bot, path_to_locales=PATH_TO_LOCALES)

    else:
        db_session.commit()
        bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=from_json_data["mes_id"],
            media=InputMediaPhoto(from_json_data["photo"], caption=response_text),
            reply_markup=keyboard,
        )

    bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)


# =====================================

@bot.on_message(filters.location)
def handle_location(client, message):
    # # Получаем координаты геопозиции
    # latitude = message.location.latitude
    # longitude = message.location.longitude
    #
    # # Сохраняем геопозицию в переменной
    # saved_location = (latitude, longitude)
    #
    # # Отправляем обратно сохраненную геопозицию
    # bot.send_location(
    #     chat_id=message.chat.id,
    #     latitude=saved_location[0],
    #     longitude=saved_location[1],
    #     # reply_to_message_id: int | None = None,
    #     # schedule_date: datetime | None = None,
    #     # protect_content: bool | None = None,
    #     # reply_markup:
    # )
    #
    # bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)

    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    from_json_data = json.loads(user_in_db.statuses_edit_event)
    cancel_mes = return_local_text(user_id=message.chat.id, text="cancel", locales_dir=PATH_TO_LOCALES)

    if not from_json_data["location"]:
        latitude = message.location.latitude
        longitude = message.location.longitude

        print(type(latitude))
        print(latitude)

        print("location")
        from_json_data["location"] = f"{latitude}_{longitude}"
        from_json_data["photo"] = False
        json_data = json.dumps(from_json_data)
        user_in_db.statuses_edit_event = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="edit_event_ask_photo", locales_dir=PATH_TO_LOCALES)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(cancel_mes, callback_data="edit_event_cancel")],
            ]
        )

        db_session.commit()
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=from_json_data["mes_id"],
            text=local_mes,
            reply_markup=keyboard,
        )

    else:
        send_dont_understand_mes(user_id=message.chat.id, bot=bot, path_to_locales=PATH_TO_LOCALES)

    bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)

# =====================================


@bot.on_message()
def handle_unknown_message(client, message):
    send_dont_understand_mes(user_id=message.chat.id, bot=bot, path_to_locales=PATH_TO_LOCALES)
    bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)


# =====================================


if __name__ == '__main__':
    print('I AM ALIVE')
    bot.run()
