from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, BotCommand)

from locales.locales_texts import return_local_text_for_user


def change_user_language(bot, message):
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