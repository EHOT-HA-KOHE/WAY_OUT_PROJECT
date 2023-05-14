import time
import gettext

from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommand, ReplyKeyboardMarkup)
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio
from pyrogram.handlers import MessageHandler

from src.db.models import User
from src.db.connection import Session

api_id = 21405010
api_hash = 'f02ca9c4a50a86708d782b83682c2327'
bot_token = '5901674172:AAFd0jb3ovdT4lZSuH7Fs3bOVXJcCxhur7I'
STATUS = "Не доставлен"

bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
db_session = Session()


bot.start()
bot.set_bot_commands(
    [
        BotCommand("start", "Первый запуск"),
        BotCommand("send_text", "Отправить текст"),
        BotCommand("show_my_lang", "Показать какой язык у меня установлен"),
        BotCommand("change_my_lang", "Изменить язык"),
        BotCommand("id", "Отправить tg_id"),
    ]
)
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


def send_text_from_texts(language="en", message="test_message"):
    translation_domain = "messages"
    locale_dir = "locales/mo_files"
    
    gettext.bindtextdomain(translation_domain, locale_dir)
    gettext.textdomain(translation_domain)
    translation = gettext.translation(translation_domain, locale_dir, languages=[language], fallback=True)
    _ = translation.gettext

    mes = _(message)
    return mes


@bot.on_message(filters.command("start") & filters.private)
def start(bot, message):
    update_user(tg_id=message.chat.id, language=message.from_user.language_code)
    bot.send_message(message.chat.id, "Start is OK")


@bot.on_message(filters.command("send_text") & filters.private)
def send_text(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    mes = send_text_from_texts(language=user_in_db.language, message="test_message")
    bot.send_message(message.chat.id, mes)


@bot.on_message(filters.command("show_my_lang") & filters.private)
def show_my_lang(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()

    bot.send_message(message.chat.id, user_in_db.language)


@bot.on_message(filters.command("change_my_lang") & filters.private)
def change_my_lang(bot, message):
    inline_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("RU", callback_data="change_lang_ru"),
                InlineKeyboardButton("UA", callback_data="change_lang_ua")
            ],
            [InlineKeyboardButton("EN", callback_data="change_lang_en")],
        ]
    )

    # Отправка сообщения с встроенной клавиатурой
    bot.send_message(
        chat_id=message.chat.id,
        text="Выберите язык:",
        reply_markup=inline_keyboard,
    )


@bot.on_message(filters.command("id") & filters.private)
def send_my_id(bot, message):
    bot.send_message(message.chat.id, message.chat.id)


# =====================================


@bot.on_callback_query()
def handle_callback_query(client, callback_query):
    # Получение колбэк-даты
    callback_data = callback_query.data

    # Обработка колбэк-даты
    if callback_data[:11] == "change_lang":
        lang = "en"
        if callback_data[12:] == "ru":
            response_text = "Язык вашего аккаунта изменен на RU"
            lang = "ru"
        elif callback_data[12:] == "ua":
            response_text = "Мова вашого облікового запису змінена на UA"
            lang = "ua"
        else:
            response_text = "Your account language has been changed to EN"

        update_user(tg_id=callback_query.from_user.id, language=lang)

    else:
        response_text = "Неизвестная кнопка"

    # Отправка ответа на колбэк-запрос
    # bot.answer_callback_query(
    #     callback_query.id,
    #     text=response_text,
    #     # show_alert=True,  # Отображение ответа во всплывающем окне ебААААть круто но и без него пиздец круто
    # )

    bot.send_message(callback_query.from_user.id, text=response_text)


if __name__ == '__main__':
    print('I AM ALIVE')
    bot.run()
