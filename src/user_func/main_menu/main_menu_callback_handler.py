from pyrogram.types import InputMediaPhoto

from src.user_func.main_menu.my_events_dir.my_events import return_my_events_buttons, start_register_user_event
from src.user_func.show_events import (
    show_events_created_by_user,
    delete_event,
    delete_event_from_db,
    show_events_the_user_joined
)
from src.user_func.main_menu.users_events_dir.users_events import pars_users_events_callback_data
from src.user_func.main_menu.user_profile_dir.user_profile import (
    show_my_profile,
    edit_user_data,
    change_interface_language
)
from src.user_func.send_dont_understand_mes import send_dont_understand_mes


def main_menu_callback_pars(
        callback_query, 
        db_session, 
        bot, 
        user, 
        path_to_locales,
        photo_main_menu,
):
    callback_data = callback_query.data

    if callback_data[10:19] == "my_events":

        if callback_data[20:32] == "create_event":
            response_text, keyboard = start_register_user_event(
                callback_query=callback_query,
                path_to_locales=path_to_locales,
                db_session=db_session,
                user=user
            )
            media = InputMediaPhoto(photo_main_menu, caption=response_text)

        elif callback_data[20:29] == "i_created":
            if callback_data[30:46] == "delete_event_del":
                response_text, keyboard = delete_event_from_db(
                    user_id=callback_query.from_user.id,
                    event_id=callback_data[47:],
                    path_to_locales=path_to_locales,
                    db_session=db_session
                )
                media = InputMediaPhoto(photo_main_menu, caption=response_text)

            elif callback_data[30:42] == "delete_event":
                response_text, keyboard, photo = delete_event(
                    user_id=callback_query.from_user.id,
                    event_id=callback_data[43:],
                    path_to_locales=path_to_locales,
                    db_session=db_session
                )
                media = InputMediaPhoto(photo, caption=response_text)

            else:
                response_text, keyboard, photo = show_events_created_by_user(
                    user_id=callback_query.from_user.id,
                    event_id=callback_data[30:],
                    path_to_locales=path_to_locales,
                    db_session=db_session,
                    photo=photo_main_menu,
                )
                media = InputMediaPhoto(photo, caption=response_text)

        elif callback_data[20:28] == "i_joined":
            response_text, keyboard, photo = show_events_the_user_joined(
                user_id=callback_query.from_user.id,
                event_id=callback_data[29:],
                path_to_locales=path_to_locales,
                db_session=db_session,
                photo=photo_main_menu,
            )
            media = InputMediaPhoto(photo, caption=response_text)

        else:
            response_text, keyboard = return_my_events_buttons(
                user_id=callback_query.from_user.id,
                path_to_locales=path_to_locales
            )
            media = InputMediaPhoto(photo_main_menu, caption=response_text)

    elif callback_data[10:24] == "way_out_events":
        return

    elif callback_data[10:22] == "users_events":
        response_text, keyboard, photo = pars_users_events_callback_data(
            user_id=callback_query.from_user.id,
            callback_data=callback_data,
            db_session=db_session,
            path_to_locales=path_to_locales,
            photo=photo_main_menu
        )
        media = InputMediaPhoto(photo, caption=response_text)

    elif callback_data[10:22] == "user_profile":

        if callback_data[23:] == "change_language":
            response_text, keyboard = change_interface_language(
                user_id=callback_query.from_user.id,
                path_to_locales=path_to_locales
            )
            media = InputMediaPhoto(photo_main_menu, caption=response_text)

        elif callback_data[23:] == "edit_profile":
            response_text, keyboard = edit_user_data(
                callback_query=callback_query,
                db_session=db_session,
                user=user,
                path_to_locales=path_to_locales
            )
            media = InputMediaPhoto(photo_main_menu, caption=response_text)

        else:
            user_in_db = db_session.query(user).filter(user.tg_id == callback_query.from_user.id).first()
            user_photo = user_in_db.photo

            response_text, keyboard = show_my_profile(
                user_id=callback_query.from_user.id,
                db_session=db_session,
                user=user,
                path_to_locales=path_to_locales
            )
            media = InputMediaPhoto(user_photo, caption=response_text)

    else:
        send_dont_understand_mes(user_id=callback_query.from_user.id, bot=bot, path_to_locales=path_to_locales)
        bot.delete_messages(chat_id=callback_query.from_user.id, message_ids=callback_query.message.id)
        return
    
    return keyboard, response_text, media
