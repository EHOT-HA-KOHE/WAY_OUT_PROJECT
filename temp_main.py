import gettext
import json
import time

from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, BotCommand)

from src.db.models import User
from src.db.connection import Session, first_db_connect
from src.user_func.change_language import change_user_language
from locales.locales_texts import return_local_text_for_user
from locales.texts.apply_changes_in_texts import update_locales_texts

api_id = 21405010
api_hash = 'f02ca9c4a50a86708d782b83682c2327'
bot_token = '6039441521:AAElNiHFFTEu8nM9EWqtdnu17FuSOyUz-40'
STATUS = "Не доставлен"
PATH_TO_LOCALES = "locales/mo_files"

update_locales_texts(path_to_locale_dir=PATH_TO_LOCALES, path_to_texts_dir='locales/texts')
bot = Client("my__bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
first_db_connect()
db_session = Session()


bot.start()
bot.set_bot_commands(
    [
        BotCommand("start", "Первый запуск"),
        BotCommand("send_text", "Отправить текст"),
        BotCommand("show_my_lang", "Показать какой язык у меня установлен"),
        BotCommand("change_my_lang", "Изменить язык"),
        BotCommand("id", "Отправить tg_id"),
        BotCommand("show_my_profile", "show_my_profile"),
        BotCommand("edit_profile", "edit_profile"),
    ]
)

# Мой 691259064
# Сашин 755464644
# id = 755464644
# photo_id = "AgACAgIAAxkBAAO3ZGI6VODFzHV2csgb0RnXr_xOKl8AAinMMRvFVhFLvtumpa9t5gkACAEAAwIAA3kABx4E"
# bot.send_photo(id, photo_id)

bot.stop()


def update_user(tg_id: int, language: str):
    user_in_db = db_session.query(User).filter(User.tg_id == tg_id).first()
    # print(user_in_db)

    if user_in_db is None:
        new_user = User(tg_id=tg_id, language=language)
        db_session.add(new_user)
        db_session.commit()

        # user_in_db = new_user
        user_in_db = db_session.query(User).filter(User.tg_id == tg_id).first()

    if language != user_in_db.language:
        user_in_db.language = language
        db_session.commit()


def start_register_new_user(tg_id: int, language: str):
    update_user(tg_id=tg_id, language=language)
    # db_session.commit()

    data = {
        "name": True,
        "sex": True,
        "age": True,
        "city": True,
        "info": True,
        "photo": True,
    }

    json_data = json.dumps(data)
    user_in_db = db_session.query(User).filter(User.tg_id == tg_id).first()
    user_in_db.statuses = json_data
    db_session.commit()

    local_mes = return_local_text_for_user(
        user_id=tg_id,
        text="start_register_message",
        locales_dir=PATH_TO_LOCALES
    )

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Yes", callback_data="registration_start")],
            [InlineKeyboardButton("Do this later", callback_data="registration_reject")]
        ]
    )

    return local_mes, keyboard


@bot.on_message(filters.photo)
def handle_photo(client, message):
    # Получение идентификатора фотографии
    photo_id = message.photo.file_id
    # Отправка сообщения с идентификатором фотографии
    message.reply_text(f"Идентификатор фото: `{photo_id}`")

    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    from_json_data = json.loads(user_in_db.statuses)

    local_mes = return_local_text_for_user(
        user_id=message.chat.id,
        text="dont_understand_you",
        locales_dir=PATH_TO_LOCALES
    )

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Cancel", callback_data="??????????????")],
        ]
    )

    if not from_json_data["photo"]:
        print("photo")
        from_json_data["photo"] = message.photo.file_id
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text_for_user(
            user_id=message.chat.id,
            text="finish_register",
            locales_dir=PATH_TO_LOCALES
        )

        user_profile = f'Name: {from_json_data["name"]}\n' \
                       f'Sex: {from_json_data["sex"]}\n' \
                       f'Age: {from_json_data["age"]}\n' \
                       f'City: {from_json_data["city"]}\n' \
                       f'Info: {from_json_data["info"]}\n' \

        local_mes = f"{local_mes}\n\n{user_profile}"

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Approve changes", callback_data="registration_approve_changes")],
            ]
        )

    db_session.commit()

    bot.delete_messages(
        chat_id=message.chat.id,
        message_ids=message.id,
    )

    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=from_json_data["reg_mes_id"],
            text=local_mes,
            reply_markup=keyboard,
        )

    except Exception as err:
        print(err)
        local_mes = return_local_text_for_user(
            user_id=message.chat.id,
            text="still_dont_understand_you",
            locales_dir=PATH_TO_LOCALES
        )

        mes_to_del = bot.send_message(
            message.chat.id,
            local_mes
        )
        time.sleep(2)

        bot.delete_messages(
            chat_id=message.chat.id,
            message_ids=mes_to_del.id,
        )


@bot.on_message(filters.command("start") & filters.private)
def start(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()

    if user_in_db is None:
        local_mes, keyboard = start_register_new_user(tg_id=message.chat.id, language=message.from_user.language_code)
        bot.send_message(
            chat_id=message.chat.id,
            text=local_mes,
            reply_markup=keyboard,
        )

    else:
        local_mes = return_local_text_for_user(
            user_id=message.chat.id,
            text="start_message",
            locales_dir=PATH_TO_LOCALES
        )

        bot.send_message(message.chat.id, local_mes)


@bot.on_message(filters.command("send_text") & filters.private)
def send_text(bot, message):
    # user_lang = return_user_local(message.chat.id)
    # mes = return_local_text_for_user(user_id=message.chat.id, message="test_message")

    mes = return_local_text_for_user(user_id=message.chat.id, text="test_message", locales_dir=PATH_TO_LOCALES)
    bot.send_message(message.chat.id, mes)


@bot.on_message(filters.command("show_my_profile") & filters.private)
def show_my_profile(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    from_json_data = json.loads(user_in_db.statuses)

    bot.send_photo(
        chat_id=message.chat.id,
        photo=from_json_data["photo"],
        caption=f"{user_in_db}\n\nName: {from_json_data['name']}",
    )


@bot.on_message(filters.command("show_my_lang") & filters.private)
def show_my_lang(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    bot.send_message(message.chat.id, user_in_db.language)


@bot.on_message(filters.command("edit_profile") & filters.private)
def edit_profile(bot, message):

    response_text = return_local_text_for_user(
        user_id=message.chat.id,
        text="ask_name",
        locales_dir=PATH_TO_LOCALES
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{message.chat.first_name}",
                    callback_data=f"registration_choose_name_{message.chat.first_name}"
                )
            ],
            [InlineKeyboardButton("Choose another", callback_data="registration_enter_name")]
        ]
    )

    mes = bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=keyboard,
    )

    data = {
        "reg_mes_id": mes.id,
        "name": False,
        "sex": False,
        "age": False,
        "city": False,
        "info": False,
        "photo": False,
    }

    json_data = json.dumps(data)
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    user_in_db.statuses = json_data
    db_session.commit()


@bot.on_message(filters.command("change_my_lang") & filters.private)
def change_my_lang(bot, message):
    inline_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("RU", callback_data="change_lang:ru"),
                InlineKeyboardButton("UA", callback_data="change_lang:ua")
            ],
            [InlineKeyboardButton("EN", callback_data="change_lang:en")],
        ]
    )

    mes = return_local_text_for_user(user_id=message.chat.id, text="сhoose_language", locales_dir=PATH_TO_LOCALES)

    bot.send_message(
        chat_id=message.chat.id,
        text=mes,
        reply_markup=inline_keyboard,
    )


@bot.on_message(filters.command("id") & filters.private)
def send_my_id(bot, message):
    bot.send_message(message.chat.id, message.chat.id)


# =====================================


@bot.on_message(filters.text & filters.private)
def send_weather_at_users_city(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    from_json_data = json.loads(user_in_db.statuses)

    local_mes = return_local_text_for_user(
        user_id=message.chat.id,
        text="dont_understand_you",
        locales_dir=PATH_TO_LOCALES
    )

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Cancel", callback_data="registration_cancel")],
        ]
    )

    if not from_json_data["name"]:
        print("name")
        from_json_data["name"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text_for_user(
            user_id=message.chat.id,
            text="ask_sex",
            locales_dir=PATH_TO_LOCALES
        )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("men", callback_data="registration_choose_sex_men"),
                    InlineKeyboardButton("women", callback_data="registration_choose_sex_women")
                ],
                [InlineKeyboardButton("Cancel", callback_data="registration_cancel")],
            ]
        )

    elif not from_json_data["sex"]:
        print("sex")
        from_json_data["sex"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text_for_user(
            user_id=message.chat.id,
            text="ask_age",
            locales_dir=PATH_TO_LOCALES
        )

    elif not from_json_data["age"]:
        print("age")
        from_json_data["age"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text_for_user(
            user_id=message.chat.id,
            text="ask_city",
            locales_dir=PATH_TO_LOCALES
        )
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Prague", callback_data="registration_choose_city_prague")],
                [InlineKeyboardButton("Another", callback_data="registration_enter_city")],
                [InlineKeyboardButton("Cancel", callback_data="registration_cancel")],
            ]
        )

    elif not from_json_data["city"]:
        print("city")
        from_json_data["city"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text_for_user(
            user_id=message.chat.id,
            text="ask_info",
            locales_dir=PATH_TO_LOCALES
        )

    elif not from_json_data["info"]:
        print("info")
        from_json_data["info"] = message.text
        json_data = json.dumps(from_json_data)
        user_in_db.statuses = json_data

        local_mes = return_local_text_for_user(
            user_id=message.chat.id,
            text="ask_photo",
            locales_dir=PATH_TO_LOCALES
        )

    # elif not from_json_data["photo"]:
    #     print("photo")
    #     from_json_data["photo"] = message.text
    #     json_data = json.dumps(from_json_data)
    #     user_in_db.statuses = json_data
    #
    #     local_mes = return_local_text_for_user(
    #         user_id=message.chat.id,
    #         text="finish_register",
    #         locales_dir=PATH_TO_LOCALES
    #     )

    db_session.commit()

    bot.delete_messages(
        chat_id=message.chat.id,
        message_ids=message.id,
    )

    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=from_json_data["reg_mes_id"],
            text=local_mes,
            reply_markup=keyboard,
        )
    except Exception as err:
        print(err)
        local_mes = return_local_text_for_user(
            user_id=message.chat.id,
            text="still_dont_understand_you",
            locales_dir=PATH_TO_LOCALES
        )

        mes_to_del = bot.send_message(
            message.chat.id,
            local_mes
        )
        time.sleep(2)

        bot.delete_messages(
            chat_id=message.chat.id,
            message_ids=mes_to_del.id,
        )


# =====================================


@bot.on_callback_query(filters.regex(r'change_lang:..'))
def handle_change_lang(client, callback_query):
    callback_data = callback_query.data
    lang = callback_data[12:]

    update_user(tg_id=callback_query.from_user.id, language=lang)
    response_text = return_local_text_for_user(
        user_id=callback_query.from_user.id,
        text="language_was_changed",
        locales_dir=PATH_TO_LOCALES
    )

    bot.answer_callback_query(
        callback_query.id,
        text=response_text,
        show_alert=True
    )


@bot.on_callback_query(filters.regex(r'registration_.*'))
def handle_registration(client, callback_query):
    callback_data = callback_query.data

    if callback_data[13:18] == "enter":
        if callback_data[19:] == "name":
            response_text = return_local_text_for_user(
                user_id=callback_query.from_user.id,
                text="ask_name",
                locales_dir=PATH_TO_LOCALES
            )
        elif callback_data[19:] == "city":
            response_text = return_local_text_for_user(
                user_id=callback_query.from_user.id,
                text="ask_city",
                locales_dir=PATH_TO_LOCALES
            )

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cancel", callback_data="registration_cancel")],
            ]
        )

    elif callback_data[13:] == "start":
        data = {
            "reg_mes_id": callback_query.message.id,
            "name": False,
            "sex": False,
            "age": False,
            "city": False,
            "info": False,
            "photo": False,
        }

        json_data = json.dumps(data)
        user_in_db = db_session.query(User).filter(User.tg_id == callback_query.from_user.id).first()
        user_in_db.statuses = json_data
        # db_session.commit()

        response_text = return_local_text_for_user(
            user_id=callback_query.from_user.id,
            text="ask_name",
            locales_dir=PATH_TO_LOCALES
        )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{callback_query.from_user.first_name}",
                        callback_data=f"registration_choose_name_{callback_query.from_user.first_name}"
                    )
                ],
                [InlineKeyboardButton("Choose another", callback_data="registration_enter_name")],
                [InlineKeyboardButton("Cancel", callback_data="registration_cancel")]
            ]
        )

    elif callback_data[13:19] == "choose":
        if callback_data[20:24] == "name":
            user_in_db = db_session.query(User).filter(User.tg_id == callback_query.from_user.id).first()
            from_json_data = json.loads(user_in_db.statuses)

            from_json_data["name"] = callback_data[25:]
            json_data = json.dumps(from_json_data)
            user_in_db.statuses = json_data

            response_text = return_local_text_for_user(
                user_id=callback_query.from_user.id,
                text="ask_sex",
                locales_dir=PATH_TO_LOCALES
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("men", callback_data="registration_choose_sex_men"),
                        InlineKeyboardButton("women", callback_data="registration_choose_sex_women")
                    ],
                    [InlineKeyboardButton("Cancel", callback_data="registration_cancel")]
                ]
            )

            print(callback_query.message.id)

        elif callback_data[20:23] == "sex":
            user_in_db = db_session.query(User).filter(User.tg_id == callback_query.from_user.id).first()
            from_json_data = json.loads(user_in_db.statuses)

            from_json_data["sex"] = callback_data[24:]
            json_data = json.dumps(from_json_data)
            user_in_db.statuses = json_data

            response_text = return_local_text_for_user(
                user_id=callback_query.from_user.id,
                text="ask_age",
                locales_dir=PATH_TO_LOCALES
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Cancel", callback_data="registration_cancel")],
                ]
            )

        elif callback_data[20:24] == "city":
            user_in_db = db_session.query(User).filter(User.tg_id == callback_query.from_user.id).first()
            from_json_data = json.loads(user_in_db.statuses)

            from_json_data["city"] = callback_data[25:]
            json_data = json.dumps(from_json_data)
            user_in_db.statuses = json_data

            response_text = return_local_text_for_user(
                user_id=callback_query.from_user.id,
                text="ask_info",
                locales_dir=PATH_TO_LOCALES
            )
            keyboard = InlineKeyboardMarkup(
                [
                    # [
                    #     InlineKeyboardButton("men", callback_data="registration_choose_sex_men"),
                    #     InlineKeyboardButton("women", callback_data="registration_choose_sex_women")
                    # ],
                    [InlineKeyboardButton("Cancel", callback_data="registration_cancel")],
                ]
            )

    elif callback_data[13:] == "approve_changes":
        user_in_db = db_session.query(User).filter(User.tg_id == callback_query.from_user.id).first()
        from_json_data = json.loads(user_in_db.statuses)

        all_data_received = all([i for i in from_json_data.values()])

        if all_data_received:
            user_in_db.name = from_json_data["name"]
            user_in_db.sex = from_json_data["sex"]
            user_in_db.age = from_json_data["age"]
            user_in_db.city = from_json_data["city"]
            user_in_db.info = from_json_data["info"]
            user_in_db.photo = from_json_data["photo"]

            data = {
                "name": True,
                "sex": True,
                "age": True,
                "city": True,
                "info": True,
                "photo": True,
            }

            json_data = json.dumps(data)
            user_in_db.statuses = json_data

            response_text = return_local_text_for_user(
                user_id=callback_query.from_user.id,
                text="successful_register",
                locales_dir=PATH_TO_LOCALES
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Show prof", callback_data="??????????????")],
                    [InlineKeyboardButton("Menu", callback_data="??????????????")],
                ]
            )

        else:
            response_text = "err"

    elif callback_data[13:] == "reject":
        response_text = return_local_text_for_user(
            user_id=callback_query.from_user.id,
            text="user_register_later",
            locales_dir=PATH_TO_LOCALES
        )
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cancel", callback_data="registration_cancel")],
            ]
        )

    elif callback_data[13:] == "cancel":
        user_in_db = db_session.query(User).filter(User.tg_id == callback_query.from_user.id).first()
        # from_json_data = json.loads(user_in_db.statuses)

        data = {
            "name": True,
            "sex": True,
            "age": True,
            "city": True,
            "info": True,
            "photo": True,
        }

        json_data = json.dumps(data)
        user_in_db.statuses = json_data

        response_text = "ggg"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cancel", callback_data="registration_cancel")],
            ]
        )

    else:
        response_text = "ggg"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cancel", callback_data="registration_cancel")],
            ]
        )

    db_session.commit()

    bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.id,
        text=response_text,
        reply_markup=keyboard,
    )


@bot.on_callback_query()
def handle_callback_query(client, callback_query):
    # callback_data = callback_query.data
    response_text = return_local_text_for_user(
        user_id=callback_query.from_user.id,
        text="unknown_button",
        locales_dir=PATH_TO_LOCALES
    )

    bot.send_message(callback_query.from_user.id, text=response_text)


if __name__ == '__main__':
    print('I AM ALIVE')
    bot.run()
