import json
import time

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, InputMediaPhoto

from src.db.models import User
from src.db.connection import Session, first_db_connect
from src.user_func.start_command import start_register_new_user, return_main_menu
from src.user_func.main_menu.user_profile_dir.files.change_language import change_user_language
from src.user_func.text_handle import text_handler
from src.user_func.main_menu.user_profile_dir.files.callback_registration import return_mes_for_callback_registration
from src.user_func.main_menu.user_profile_dir.user_profile import (
    show_my_profile,
    edit_user_data,
    change_interface_language
)

from locales.locales_texts import return_local_text
from locales.texts.apply_changes_in_texts import update_locales_texts


api_id = 21405010
api_hash = 'f02ca9c4a50a86708d782b83682c2327'
bot_token = '6039441521:AAElNiHFFTEu8nM9EWqtdnu17FuSOyUz-40'
PATH_TO_LOCALES = "locales/mo_files"
PHOTO_MAIN_MENU = "AgACAgIAAxkBAAIFwWRt4KSe5O284zko1v3teK2caWUTAAJLxTEbTWFxS0qyGrww6LnfAAgBAAMCAAN4AAceBA"

update_locales_texts(path_to_locale_dir=PATH_TO_LOCALES, path_to_texts_dir='locales/texts')
bot = Client("my__bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
first_db_connect()
db_session = Session()


bot.start()
bot.set_bot_commands(
    [
        BotCommand("start", "Главное меню"),
        BotCommand("del_my_account", "del_my_account"),
        BotCommand("send_message_with_link", "send_message_with_link"),
        BotCommand("send_message_with_link_tg_id", "send_message_with_link_tg_id"),
        BotCommand("send_message_with_link_button", "send_message_with_link_button"),
    ]
)
bot.stop()


@bot.on_message(filters.photo)
def handle_photo(client, message):
    # bot.send_message(message.chat.id, message.photo.file_id)

    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    from_json_data = json.loads(user_in_db.statuses)

    response_text = return_local_text(
        user_id=message.chat.id,
        text="dont_understand_you",
        locales_dir=PATH_TO_LOCALES
    )
    main_menu = return_local_text(user_id=message.chat.id, text="main_menu", locales_dir=PATH_TO_LOCALES)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f"{main_menu}", callback_data="main_menu")]])

    if not from_json_data["photo"]:
        print("photo")
        from_json_data["photo"] = message.photo.file_id
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text(user_id=message.chat.id, text="finish_register", locales_dir=PATH_TO_LOCALES)

        approve_mes = return_local_text(user_id=message.chat.id, text="approve_changes", locales_dir=PATH_TO_LOCALES)
        cancel_mes = return_local_text(user_id=message.chat.id, text="cancel", locales_dir=PATH_TO_LOCALES)

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

    else:
        bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)
        message_for_del = bot.send_message(chat_id=message.chat.id, text=response_text)
        time.sleep(1.5)
        bot.delete_messages(chat_id=message.chat.id, message_ids=message_for_del.id)
        return

    db_session.commit()

    bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)

    bot.edit_message_media(
        chat_id=message.chat.id,
        message_id=from_json_data["reg_mes_id"],
        media=InputMediaPhoto(from_json_data["photo"], caption=response_text),
        reply_markup=keyboard,
    )


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

    # bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=keyboard)
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


@bot.on_message(filters.command("send_message_with_link") & filters.private)
def send_message_with_link(bot, message):
    text = "Привет! Вот ссылка на мой аккаунт: [Ссылка](https://t.me/vanchouz)"
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        # parse_mode="Markdown"
    )


@bot.on_message(filters.command("send_message_with_link_tg_id") & filters.private)
def send_message_with_link(bot, message):
    # text = "Привет! Вот ссылка на мой аккаунт: [Ссылка](https://t.me/vanchouz)"
    # text = "Привет! Вот ссылка на мой аккаунт: [user](tg://user?id=582712403)" \
    text = "Привет! Вот ссылка на мой аккаунт: [user](tg://user?id=691259064)" \
           "\n\n[URL](https://pyrogram.org)"
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        # disable_web_page_preview=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )


@bot.on_message(filters.command("send_message_with_link_button") & filters.private)
def send_message_with_link(bot, message):
    text = "Привет! Вот ссылка на мой аккаунт:"
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                text=f"SOME",
                user_id=874821265,
                # url="https://t.me/vanchouz",
                # url="https://t.me/user?id=691259064",
                )
            ],
        ]
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard,
        # parse_mode="Markdown"
    )


# =====================================


@bot.on_message(filters.text & filters.private)
def text_handle(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    from_json_data = json.loads(user_in_db.statuses)

    local_mes, keyboard = text_handler(
        message=message,
        path_to_locales=PATH_TO_LOCALES,
        from_json_data=from_json_data,
        user_in_db=user_in_db
    )

    if keyboard is None:
        mes_to_del = bot.send_message(chat_id=message.chat.id, text=local_mes)
        time.sleep(1.5)
        bot.delete_messages(chat_id=message.chat.id, message_ids=mes_to_del.id)

    else:
        db_session.commit()

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=from_json_data["reg_mes_id"],
            text=local_mes,
            reply_markup=keyboard,
        )

    bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)


# =====================================


@bot.on_callback_query(filters.regex(r'main_menu_.*'))
def handle_main_menu_point(client, callback_query):
    callback_data = callback_query.data

    if callback_data[10:22] == "user_profile":

        if callback_data[23:] == "change_language":
            response_text, keyboard = change_interface_language(
                user_id=callback_query.from_user.id,
                path_to_locales=PATH_TO_LOCALES
            )
            media = InputMediaPhoto(PHOTO_MAIN_MENU, caption=response_text)

        elif callback_data[23:] == "edit_profile":
            response_text, keyboard = edit_user_data(
                callback_query=callback_query,
                db_session=db_session,
                user=User,
                path_to_locales=PATH_TO_LOCALES
            )
            media = InputMediaPhoto(PHOTO_MAIN_MENU, caption=response_text)

        else:
            user_in_db = db_session.query(User).filter(User.tg_id == callback_query.from_user.id).first()
            user_photo = user_in_db.photo

            response_text, keyboard = show_my_profile(
                user_id=callback_query.from_user.id,
                db_session=db_session,
                user=User,
                path_to_locales=PATH_TO_LOCALES
            )
            media = InputMediaPhoto(user_photo, caption=response_text)

    else:
        local_mes = return_local_text(
            user_id=callback_query.from_user.id,
            text="dont_understand_you",
            locales_dir=PATH_TO_LOCALES
        )
        mes_for_del = bot.send_message(chat_id=callback_query.from_user.id, text=local_mes)
        time.sleep(1.5)
        bot.delete_messages(chat_id=callback_query.from_user.id, message_ids=mes_for_del.id)
        return

    try:
        bot.edit_message_media(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.id,
            media=media,
            reply_markup=keyboard,
        )
    except Exception as err:
        bot.edit_message_media(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.id,
            media=InputMediaPhoto(PHOTO_MAIN_MENU, caption=response_text),
            reply_markup=keyboard,
        )


@bot.on_callback_query(filters.regex(r'main_menu'))
def handle_main_menu(client, callback_query):
    response_text, keyboard = return_main_menu(user_id=callback_query.from_user.id, path_to_locales=PATH_TO_LOCALES)

    bot.edit_message_media(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.id,
        media=InputMediaPhoto(PHOTO_MAIN_MENU, caption=response_text),
        reply_markup=keyboard,
    )


@bot.on_callback_query(filters.regex(r'registration_.*'))
def handle_registration(client, callback_query):
    callback_data = callback_query.data

    if callback_data[13:] == "reject":
        response_text, keyboard = return_main_menu(user_id=callback_query.from_user.id, path_to_locales=PATH_TO_LOCALES)

    else:
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


@bot.on_callback_query(filters.regex(r'change_lang_..'))
def handle_change_lang(client, callback_query):
    callback_data = callback_query.data
    lang = callback_data[12:]

    response_text = change_user_language(
        callback_query=callback_query,
        lang=lang,
        db_session=db_session,
        user=User,
        path_to_locales=PATH_TO_LOCALES
    )

    bot.answer_callback_query(callback_query.id, text=response_text, show_alert=True)
    bot.answer_callback_query(callback_query.id, text=response_text, show_alert=True)


@bot.on_callback_query()
def handle_callback_query(client, callback_query):
    response_text = return_local_text(
        user_id=callback_query.from_user.id,
        text=f"unknown_button\n\ncallback_data = {callback_query.data}",
        locales_dir=PATH_TO_LOCALES
    )

    bot.send_message(callback_query.from_user.id, text=response_text)


# =====================================

@bot.on_message()
def handle_location(client, message):
    if message.location:
        # Получаем координаты геопозиции
        latitude = message.location.latitude
        longitude = message.location.longitude

        # Сохраняем геопозицию в переменной
        saved_location = (latitude, longitude)

        # Отправляем обратно сохраненную геопозицию
        client.send_location(
            chat_id=message.chat.id,
            latitude=saved_location[0],
            longitude=saved_location[1]
        )
    else:
        local_mes = return_local_text(user_id=message.chat.id, text="dont_understand_you", locales_dir=PATH_TO_LOCALES)
        mes_for_del = bot.send_message(text=local_mes, chat_id=message.chat.id)
        time.sleep(1.5)
        bot.delete_messages(chat_id=message.chat.id, message_ids=mes_for_del.id)

    bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)

# =====================================


if __name__ == '__main__':
    print('I AM ALIVE')
    bot.run()
