from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, BotCommand)

from locales.locales_texts import return_local_text


def update_user(tg_id: int, language: str, db_session, user):
    user_in_db = db_session.query(user).filter(user.tg_id == tg_id).first()

    if user_in_db is None:
        new_user = user(tg_id=tg_id, language=language)
        db_session.add(new_user)
        db_session.commit()

        user_in_db = db_session.query(user).filter(user.tg_id == tg_id).first()

    if language != user_in_db.language:
        user_in_db.language = language
        db_session.commit()


def choose_language_for_user_command(message, path_to_locales):
    inline_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("RU", callback_data="change_lang_ru"),
                InlineKeyboardButton("UA", callback_data="change_lang_ua")
            ],
            [InlineKeyboardButton("EN", callback_data="change_lang_en")],
        ]
    )

    mes = return_local_text(user_id=message.chat.id, text="select_language", locales_dir=path_to_locales)

    return mes, inline_keyboard


def change_user_language(callback_query, lang, db_session, user, path_to_locales):
    update_user(tg_id=callback_query.from_user.id, language=lang, db_session=db_session, user=user)
    response_text = return_local_text(
        user_id=callback_query.from_user.id,
        text="language_was_changed",
        locales_dir=path_to_locales
    )

    return response_text
