import json
import time

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, InputMediaPhoto

from src.db.models import User, Event
from src.db.connection import Session, first_db_connect

from src.admin_func.publish_or_reject_user_event import publish_or_reject_user_event
from src.admin_func.send_mes_to_all_users_from_admin import (
    text_handler_to_data_to_send_mes_to_users_from_admin,
    photo_handler_to_data_to_send_mes_to_users_from_admin,
    callback_handler_to_data_to_send_mes_to_users_from_admin,
    start_creating_mes_to_send_users_from_admin
)

from src.user_func.start_command import start_register_new_user, return_main_menu
from src.user_func.show_event_location import show_event_location
from src.user_func.show_events import delete_event_from_db
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


api_id_bot = 21405010
api_hash_bot = 'f02ca9c4a50a86708d782b83682c2327'
bot_token = '6039441521:AAElNiHFFTEu8nM9EWqtdnu17FuSOyUz-40'
# print(bot.get_me())
BOT_NAME = "WAY_OUT_EVENTS_BOT"

api_id_client = 22791055
api_hash_client = 'cc2abc27d2cf4a60cd560253709e2767'

CHAT_ID_FOR_VERIF = -1001989835657
CHAT_ID_FOR_SENDING_MES_FROM_ADMIN = -4030011503
PATH_TO_LOCALES = "locales/mo_files"
PHOTO_MAIN_MENU = "AgACAgIAAxkBAAIFwWRt4KSe5O284zko1v3teK2caWUTAAJLxTEbTWFxS0qyGrww6LnfAAgBAAMCAAN4AAceBA"

update_locales_texts(path_to_locale_dir=PATH_TO_LOCALES, path_to_texts_dir='locales/texts')
bot = Client("my__bot", api_id=api_id_bot, api_hash=api_hash_bot, bot_token=bot_token)
client_chat_creator = Client('client_chat_creator_session', api_id_client, api_hash_client)

first_db_connect()
db_session = Session()


# ============================================


bot.start()
bot.set_bot_commands(
    [
        BotCommand("start", "Главное меню"),
        BotCommand("del_my_account", "del_my_account"),
        BotCommand("create_test_chat", "create_test_chat"),
    ]
)
bot.stop()


@bot.on_message(filters.command("send_mes_to_users"))
def send_mes_to_all_users_from_admin_handler(bot, message):
    # print(message)
    if message.chat.id == CHAT_ID_FOR_SENDING_MES_FROM_ADMIN:
        # send_mes_to_all_users_from_admin(bot, db_session, User, PATH_TO_LOCALES)
        response_text, keyboard = start_creating_mes_to_send_users_from_admin()

        bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=keyboard,
            disable_notification=True,
        )


@bot.on_message(filters.command("send_info"))
def send_mes_to_all_users_from_admin_handler(bot, message):
    # print(message)
    bot.send_message(
        chat_id=message.chat.id,
        text=message
    )


@bot.on_message(filters.command("test") & filters.private)
def send_mes_to_all_users_from_admin_handler(bot, message):
    # print(message)
    # group = client_chat_creator.create_supergroup(title="POP")
    # group_id = group.id
    client_chat_creator.send_message(691259064, "group_id")
    bot.send_message(691259064, "group_id")
    print(f"{bot}\n\n{client_chat_creator}")


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

    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()

    temp_mes = bot.send_photo(
        chat_id=message.chat.id,
        photo=PHOTO_MAIN_MENU,
        caption=response_text,
        reply_markup=keyboard
    )

    user_in_db.start_mes_id = temp_mes.id
    db_session.commit()


@bot.on_message(filters.command("del_my_account") & filters.private)
def del_my_account(bot, message):
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    event_ids = db_session.query(Event.id).filter_by(creator_id=user_in_db.tg_id).all()
    events_ids = [event_id[0] for event_id in event_ids]

    for event_id in events_ids:
        delete_event_from_db(
            user_id=user_in_db.tg_id,
            event_id=event_id,
            path_to_locales=PATH_TO_LOCALES,
            db_session=db_session,
        )

    db_session.delete(user_in_db)
    db_session.commit()
    bot.send_message(message.chat.id, f"User {message.chat.id} del from db")


@bot.on_message(filters.command("create_test_chat") & filters.private)
def del_my_account(bot, message):
    # bot.send_message(-995522785, "heya!")
    # client_chat_creator.start()

    # print(bot.get_me())

    group = client_chat_creator.create_group(title='New Group', users=['kirshine', ])
    print(group)
    group_id = group.id

    # users_to_invite = ['vanchouz', ]
    # client_chat_creator.add_chat_members(chat_id=group_id, user_ids=users_to_invite)

    # client_chat_creator.send_message(chat_id='kirshine', text="hey")

    # client_chat_creator.stop()


# =====================================


# @bot.on_message(filters.new_chat_members)
# def auto_approve_join_requests(client, message):
#     print("filters.new_chat_members")
#     chat_id = message.chat.id
#     user_ids = [member.user.id for member in message.new_chat_members]
#
#     # Принятие заявок на вступление
#     for user_id in user_ids:
#         client.promote_chat_member(chat_id, user_id, can_invite_users=True)

@bot.on_message(filters.new_chat_members)
def auto_approve_join_requests(client, message):
    print("Новый участник в чате:", message.new_chat_members)

# =====================================


@bot.on_message(filters.text & filters.private)
def text_handle(bot, message):
    # print(message)
    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()

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


@bot.on_message(filters.text)
def text_handler_to_data_to_send_mes_to_users_from_admin_main(bot, message):
    # print(message.chat.id)
    if message.chat.id == CHAT_ID_FOR_SENDING_MES_FROM_ADMIN or message.chat.id == CHAT_ID_FOR_VERIF:
        response_text, keyboard, mes_id = text_handler_to_data_to_send_mes_to_users_from_admin(text=message.text, bot=bot, message=message)
        bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)

        if keyboard is None:
            send_dont_understand_mes(user_id=message.chat.id, bot=bot, path_to_locales=PATH_TO_LOCALES, )

        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=mes_id,
                text=response_text,
                reply_markup=keyboard,
            )


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
    chat_member = bot.get_users(callback_query.from_user.id)
    # print(chat_member)

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

    # event = db_session.query(Event).filter_by(id=callback_data[37:]).first()

    # invite_link = client_chat_creator.export_chat_invite_link(event.group_id)
    # invite_link = bot.export_chat_invite_link(chat_id=event.group_id)

    # invite_link = bot.create_chat_invite_link(chat_id=event.group_id, creates_join_request=True)
    # print(invite_link.invite_link)

    response_text, keyboard = add_or_del_user_on_or_from_event(
        action=callback_data[33:36],
        client_chat_creator=client_chat_creator,
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
        bot=bot,
        path_to_locales=PATH_TO_LOCALES,
        chat_id_for_verif=CHAT_ID_FOR_VERIF,
    )

    bot.edit_message_media(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.id,
        media=InputMediaPhoto(photo, caption=response_text),
        reply_markup=keyboard,
    )


@bot.on_callback_query(filters.regex(r'verif_event_.*'))
def handle_edit_event(client, callback_query):
    # temp_bot_info = bot.get_me()
    # bot_id = temp_bot_info.id
    # print(f"bot_id = {bot_id}")

    callback_data = callback_query.data
    # print(callback_query)
    time.sleep(2)
    # client_chat_creator.send_message(BOT_NAME, "hey")

    response_text = publish_or_reject_user_event(
        action=callback_data[12:19],
        event_id=callback_data[20:],
        db_session=db_session,
        bot=bot,
        client_chat_creator=client_chat_creator,
        bot_name=BOT_NAME,
        path_to_locales=PATH_TO_LOCALES
    )

    bot.delete_messages(chat_id=CHAT_ID_FOR_VERIF, message_ids=callback_query.message.id)
    bot.send_message(
        chat_id=CHAT_ID_FOR_VERIF,
        text=response_text,
        disable_notification=True,
    )


@bot.on_callback_query(filters.regex(r'show_event_location_.*'))
def handle_show_event_location(client, callback_query):
    callback_data = callback_query.data
    show_event_location(
        chat_id=callback_query.message.chat.id,
        id_for_locales=callback_query.from_user.id,
        message_id=callback_query.message.id,
        event_id=callback_data[20:],
        db_session=db_session,
        bot=bot,
        path_to_locales=PATH_TO_LOCALES,
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


@bot.on_callback_query(filters.regex(r'creating_message_to_send_to_all_users_.*'))
def callback_handle_to_data_to_send_mes_to_users_from_admin(client, callback_query):
    # callback_data = callback_query.data
    callback_handler_to_data_to_send_mes_to_users_from_admin(
        callback=callback_query,
        bot=bot,
        db_session=db_session,
        db_user=User,
        path_to_locales=PATH_TO_LOCALES
    )


@bot.on_callback_query()
def handle_callback_query(client, callback_query):
    print(callback_query)
    response_text = return_local_text(
        user_id=callback_query.from_user.id,
        text=f"unknown_button\n\ncallback_data = {callback_query.data}",
        locales_dir=PATH_TO_LOCALES
    )

    mes_to_del = bot.send_message(callback_query.from_user.id, text=response_text)
    time.sleep(1.5)
    bot.delete_messages(chat_id=mes_to_del.chat.id,message_ids=mes_to_del.id)


# =====================================


@bot.on_message(filters.photo & filters.private)
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


@bot.on_message(filters.photo)
def handle_photo_to_data_to_send_mes_to_users_from_admin(client, message):
    photo_handler_to_data_to_send_mes_to_users_from_admin(chat_id=message.chat.id, photo=message.photo.file_id, bot=bot, message=message)


# =====================================

@bot.on_message(filters.location | filters.venue)
def handle_location(client, message):
    # print(message)

    user_in_db = db_session.query(User).filter(User.tg_id == message.chat.id).first()
    from_json_data = json.loads(user_in_db.statuses_edit_event)
    cancel_mes = return_local_text(user_id=message.chat.id, text="cancel", locales_dir=PATH_TO_LOCALES)

    if not from_json_data["location"]:
        if message.venue is None:
            latitude = message.location.latitude
            longitude = message.location.longitude
            title = "nodata"
            address = "nodata"

        else:
            latitude = message.venue.location.latitude
            longitude = message.venue.location.longitude
            title = message.venue.title
            address = message.venue.address

        # print(type(latitude))
        # print(latitude)

        print("location")
        from_json_data["location"] = f"location_{latitude}_{longitude}_{title}_{address}"
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
    # print(message.chat.id)
    # print(message.message_id)
    if message.chat.id == CHAT_ID_FOR_SENDING_MES_FROM_ADMIN or message.chat.id == CHAT_ID_FOR_VERIF:
        send_dont_understand_mes(user_id=message.chat.id, bot=bot, path_to_locales=PATH_TO_LOCALES)
        bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)


# =====================================


if __name__ == '__main__':
    print('I AM ALIVE BOT')
    client_chat_creator.start()
    bot.run()
