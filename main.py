from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommand, ReplyKeyboardMarkup)
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio
import time
from pyrogram.handlers import MessageHandler

api_id = 21405010
api_hash = 'f02ca9c4a50a86708d782b83682c2327'
bot_token = '5901674172:AAFd0jb3ovdT4lZSuH7Fs3bOVXJcCxhur7I'
STATUS = "Не доставлен"

bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def dump(client, message):
    print(message)


bot.add_handler(MessageHandler(dump))

bot.start()

bot.set_bot_commands(
    [
        BotCommand("start", "Первый запуск"),
        BotCommand("curyr", "Посмотреть пример сообщения для курьера"),
        BotCommand("scaner", "scaner"),
    ]
)

bot.stop()


@bot.on_message(filters.command("scaner") & filters.private)
def scaner(bot, message):
    if len(message.command) > 1:
        # print(message)
        bot.send_message(message.chat.id, f"Товар {message.command[1]}")
    else:
        bot.send_message(
            message.chat.id,
            "Выберите жижу",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Выбрать 🔥", url="https://telegra.ph/Hey-02-14-123")
                    ]
                ]
            )
        )


@bot.on_message(filters.command("id") & filters.private)
def send_mi_id(bot, message):
    bot.send_message(message.chat.id, message.chat.id)


@bot.on_message(filters.command("start") & filters.private)
def start_message(bot, message):
    if len(message.command) > 1:
        # send_mi_id(bot, message)
        # print(message)
        bot.send_message(message.chat.id, f"Вы первый {message.command[1]}")
    else:
        bot.send_photo(
            message.chat.id,
            "800.jpeg",
            caption="**Выбор товара в магазине**\n\n"
            "На данный момент работает только один путь --1000-- - --Ананас-- - --Назад-- - --Назад--"
            " + 'Показать пример сообщения для курьера'"
            "\n\n"
            "**Выберите желаемое количество затяжек** 👇👇👇",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("1000 🔥", callback_data="1"),
                        InlineKeyboardButton("2000", callback_data="2")
                    ],
                    [
                        InlineKeyboardButton("3000", callback_data="2"),
                        InlineKeyboardButton("4000", callback_data="2")
                    ],
                    [
                        InlineKeyboardButton("5000", callback_data="2"),
                        InlineKeyboardButton("6000", callback_data="2")
                    ],
                    [
                        InlineKeyboardButton("Просмотреть корзину", callback_data="basket")
                    ]
                ]
            )
        )


@bot.on_message(filters.command("curyr") & filters.private)
def send_curyr_message_example(bot, message):
    # global STATUS
    bot.send_message(
        message.chat.id,
        f"Заказ №**1408** - {STATUS}\n\n"
        f"- ElfBar Ананас - 3шт\n"
        f"- ElfBar Киви - 1шт\n\n"
        f"Анна: +420777777777\n\n"
        f"@mmshhy\n\n"
        f"Адрес: `Senovážné nám. 977/24`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Доставлен", callback_data="status"),
                    InlineKeyboardButton("Удалить", callback_data="del")
                ]
            ]
        )
    )


@bot.on_callback_query()
def change_menu(bot, callback_query):
    global STATUS

    # if callback_query.data == "1":
    #     bot.send_message(
    #         callback_query.message.chat.id,
    #         "Выберите один из 6ти вкусов",
    #         reply_markup=ReplyKeyboardMarkup(
    #             [
    #                 ["Ананас 🍍"],
    #                 ["Цитрус 🍊"],
    #                 ["Лимонад 🍋"],
    #                 ["Малина 🍓"],
    #                 ["Кокос 🥥"],
    #                 ["Дыня 🍈"]
    #             ],
    #             resize_keyboard=True
    #         )
            # reply_markup=InlineKeyboardMarkup(
            #     [
            #         [
            #             [InlineKeyboardButton("Назад 🔙", callback_data="back")]
            #         ]
            #     ]
            # )
        # )

    if callback_query.data == "1":
        callback_query.edit_message_text(
            "Выберите один из 6ти вкусов:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Ананас 🍍", callback_data="A"),
                    ],
                    [InlineKeyboardButton("Цитрус 🍊", callback_data="2")],
                    [InlineKeyboardButton("Лимонад 🍋", callback_data="2")],
                    [InlineKeyboardButton("Малина 🍓", callback_data="2")],
                    [InlineKeyboardButton("Кокос 🥥", callback_data="2")],
                    [InlineKeyboardButton("Дыня 🍈", callback_data="2")],
                    [InlineKeyboardButton("Назад 🔙", callback_data="back")]
                ]
            )
        )

    elif callback_query.data == "back":
        callback_query.edit_message_text(
            "**Выбор товара в магазине**\n\n"
            "На данный момент работает только один путь --1000-- - --Ананас-- - --Назад-- - --Назад--"
            " + 'Показать пример сообщения для курьера'"
            "\n\n"
            "**Выберите желаемое количество затяжек** 👇👇👇",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("1000 🔥", callback_data="1"),
                        InlineKeyboardButton("2000", callback_data="2")
                    ],
                    [
                        InlineKeyboardButton("3000", callback_data="2"),
                        InlineKeyboardButton("4000", callback_data="2")
                    ],
                    [
                        InlineKeyboardButton("5000", callback_data="2"),
                        InlineKeyboardButton("6000", callback_data="2")
                    ],
                    [
                        InlineKeyboardButton("Просмотреть корзину", callback_data="basket")
                    ]
                ]
            )
        )

    # await Bot_IzzyNfts.edit_message_media(
    #     chat_id=query.from_user.username,
    #     message_id=query.message.id,
    #     media=message,
    #     reply_markup=InlineKeyboardMarkup(
    #         keyboards.get_nft_list_keys(
    #
    #         )
    #     )
    # )

    elif callback_query.data == "A":
        mes = InputMediaPhoto(
            media="900.jpg",
            caption="Выберите хотите вы увидеть описание или добавить товар в корзину"
        )
        bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.id,
            media=mes,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Описание ℹ️", callback_data="2"),
                        InlineKeyboardButton("В корзину", callback_data="2")
                    ],
                    [
                        InlineKeyboardButton("Назад 🔙", callback_data="back_taste")
                    ]
                ]
            )
        )

    elif callback_query.data == "back_taste":
        # bot.delete_messages(callback_query.message.chat.id, callback_query.message.id)
        mes = InputMediaPhoto(
            media="800.jpeg",
            caption="Выберите один из 6ти вкусов:"
        )
        bot.edit_message_media(
            callback_query.message.chat.id,
            message_id=callback_query.message.id,
            media=mes,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Ананас 🍍", callback_data="A"),
                    ],
                    [InlineKeyboardButton("Цитрус 🍊", callback_data="2")],
                    [InlineKeyboardButton("Лимонад 🍋", callback_data="2")],
                    [InlineKeyboardButton("Малина 🍓", callback_data="2")],
                    [InlineKeyboardButton("Кокос 🥥", callback_data="2")],
                    [InlineKeyboardButton("Дыня 🍈", callback_data="2")],
                    [InlineKeyboardButton("Назад 🔙", callback_data="back")]
                ]
            )
        )
    elif callback_query.data == "2":
        x = bot.send_message(callback_query.message.chat.id, "Эта функция **не подключена**")
        time.sleep(1.5)
        bot.delete_messages(x.chat.id, x.id)

    elif callback_query.data == "status":
        # global STATUS
        STATUS = "Доставлен"
        callback_query.edit_message_text(
            f"Заказ №**1408** - {STATUS}\n\n"
            f"- ElfBar Ананас - 3шт\n"
            f"- ElfBar Киви - 1шт\n\n"
            f"Анна: +420777777777\n\n"
            f"@mmshhy\n\n"
            f"Адрес: `Senovážné nám. 977/24`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Доставлен", callback_data="status_no"),
                        InlineKeyboardButton("Удалить", callback_data="del")
                    ]
                ]
            )
        )

    elif callback_query.data == "status_no":
        STATUS = "Не доставлен"
        callback_query.edit_message_text(
            f"Заказ №**1408** - {STATUS}\n\n"
            f"- ElfBar Ананас - 3шт\n"
            f"- ElfBar Киви - 1шт\n\n"
            f"Анна: +420777777777\n\n"
            f"@mmshhy\n\n"
            f"Адрес: `Senovážné nám. 977/24`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Доставлен", callback_data="status"),
                        InlineKeyboardButton("Удалить", callback_data="del")
                    ]
                ]
            )
        )

    elif callback_query.data == "del":
        bot.delete_messages(callback_query.message.chat.id, callback_query.message.id)

    elif callback_query.data == "basket":
        callback_query.edit_message_text(
            f"**Сейчас в вашей корзине:**\n\n"
            "Banan 🍌 1500 - --3шт--\n"
            "Ananas 🍍 2500 - --1шт--\n\n",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Очистить корзину", callback_data="back")
                    ],
                    [
                        InlineKeyboardButton("Назад", callback_data="back"),
                        InlineKeyboardButton("Оформить заказ", callback_data="make_order")
                    ]
                ]
            )
        )

    elif callback_query.data == "make_order":
        callback_query.edit_message_text(
            "Ваш заказ **№1408** был успешно отправлен\n\n"
            "Banan 🍌 1500 - --3шт--\n"
            "Ananas 🍍 2500 - --1шт--\n\n"
            "Курьер доставит ваш заказ в течении 90 минут\n\n"
            "В случае каких либо вопросов нажмите на кнопку связаться👇👇👇",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Связаться", url="https://t.me/your_administrator")
                    ]
                ]
            )
        )

# url="https://t.me/your_administrator" / user_id=5016887224


if __name__ == '__main__':
    print('I AM ALIVE')
    bot.run()
