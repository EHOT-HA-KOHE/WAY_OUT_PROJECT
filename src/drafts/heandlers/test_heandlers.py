bot.start()
bot.set_bot_commands(
    [
        BotCommand("start", "Главное меню"),
        # BotCommand("send_text", "Отправить текст"),
        # BotCommand("show_my_lang", "Показать какой язык у меня установлен"),
        # BotCommand("change_my_lang", "Изменить язык"),
        # BotCommand("id", "Отправить tg_id"),
        # BotCommand("show_my_profile", "show_my_profile"),
        # BotCommand("edit_profile", "edit_profile"),
        BotCommand("del_my_account", "del_my_account"),
    ]
)
bot.stop()

@bot.on_message(filters.command("send_text") & filters.private)
def send_text(bot, message):
    mes = return_local_text(user_id=message.chat.id, text="test_message", locales_dir=PATH_TO_LOCALES)
    bot.send_message(message.chat.id, mes)


@bot.on_message(filters.command("send_photo_mes") & filters.private)
def send_photo_mes(bot, message):
    message = bot.send_photo(
        chat_id=message.chat.id,
        photo="AgACAgIAAxkBAAIFwWRt4KSe5O284zko1v3teK2caWUTAAJLxTEbTWFxS0qyGrww6LnfAAgBAAMCAAN4AAceBA",
        caption="Исходный текст"
    )
    time.sleep(2)
    # Измените текст сообщения без картинки
    # bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Новый текст")
    # bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Новый текст", photo=None)
    # Отправьте новое сообщение без картинки
    # bot.send_message(chat_id=message.chat.id, text="Новый текст")
    message_2 = bot.edit_message_media(
        chat_id=message.chat.id,
        message_id=message.id,
        # media=InputMediaPhoto("images/photo_2023-05-23_18-49-02.jpg", caption="Новый текст"),
        media=InputMediaPhoto("AgACAgIAAxkBAAIF12Rt5HxhBQUquP7V96-CF7VJuHu2AAICxTEbTWFxS4URztu12qW5AAgBAAMCAAN4AAceBA", caption="Новый текст")
    )

    # Удалите исходное сообщение с картинкой
    # bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)

    time.sleep(2)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Новый новый текст")


@bot.on_message(filters.command("show_my_profile") & filters.private)
def show_my_profile_command(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()

    bot.send_photo(
        chat_id=message.chat.id,
        photo=user_in_db.photo,
        caption=f"{user_in_db}",
    )


@bot.on_message(filters.command("show_my_lang") & filters.private)
def show_my_lang(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    bot.send_message(message.chat.id, user_in_db.language)


@bot.on_message(filters.command("edit_profile") & filters.private)  # todo edit callback "registration_start"
def edit_profile(bot, message):
    response_text = return_local_text(
        user_id=message.chat.id,
        text="edit_user_ask_name",
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

    edit_statuses_in_database(status=False, reason="user", message=mes, db_session=db_session, user=User)


@bot.on_message(filters.command("change_my_lang") & filters.private)
def change_my_lang(bot, message):
    mes, inline_keyboard = choose_language_for_user_command(message=message, path_to_locales=PATH_TO_LOCALES)

    bot.send_message(
        chat_id=message.chat.id,
        text=mes,
        reply_markup=inline_keyboard,
    )


@bot.on_message(filters.command("id") & filters.private)
def send_my_id(bot, message):
    bot.send_message(message.chat.id, message.chat.id)


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
