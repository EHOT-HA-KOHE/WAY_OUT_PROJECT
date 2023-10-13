import json
import time

from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ChatPrivileges)

from src.db.models import Category, Event
from src.user_func.show_events import return_event_info_and_photo
from src.user_func.add_or_del_user_on_or_from_event import add_or_del_user_on_or_from_event


def publish_or_reject_user_event(action, event_id, db_session, bot, client_chat_creator, bot_name, path_to_locales):
    if action == "publish":
        event = db_session.query(Event).filter_by(id=event_id).first()
        from_json_data = json.loads(event.temp_info)

        category = db_session.query(Category).filter_by(name=from_json_data["category_name"]).first()
        if category is None:
            category = Category(name=from_json_data["category_name"])
            db_session.add(category)

        if from_json_data["make_group"] == "yes":
            # client_chat_creator.start()
            print(client_chat_creator)
            # group = client_chat_creator.create_supergroup(title=f'WAY_OUT {from_json_data["title"]}')
            group = client_chat_creator.create_supergroup(title=f'WAY_OUT {from_json_data["title"]}')
            group_id = group.id
            print(group_id)

            # client_chat_creator.send_message(group_id, "hey")
            # client_chat_creator.send_message(bot_name, "hey")

            time.sleep(3)

            users_to_invite = [bot_name]
            client_chat_creator.add_chat_members(chat_id=group_id, user_ids=users_to_invite)  # todo

            invite_link = client_chat_creator.export_chat_invite_link(group_id)
            print(invite_link)
            client_chat_creator.send_message(group_id, invite_link)
            event.group_link = invite_link

            client_chat_creator.promote_chat_member(chat_id=group_id, user_id=bot_name,
                                                    privileges=ChatPrivileges(
                                                        can_delete_messages=True,
                                                        can_restrict_members=True,
                                                        can_post_messages=True,
                                                        can_edit_messages=True,
                                                        can_invite_users=True,
                                                        can_pin_messages=True,
                                                    ))

            # client_chat_creator.stop()

        else:
            group_id = None

        event.title = from_json_data["title"]
        event.language = 'ru'
        event.description = from_json_data["description"]
        event.city = from_json_data["city"]
        event.max_amount_of_people = from_json_data["max_amount_of_people"]
        event.date = from_json_data["date"]
        event.photo = from_json_data["photo"]
        event.location = from_json_data["location"]
        event.group_id = group_id
        event.temp_info = ""

        db_session.add(event)
        # db_session.add_all([event, creator])
        event.categories.append(category)

        add_or_del_user_on_or_from_event(
            action="add",
            client_chat_creator=client_chat_creator,
            user_id=from_json_data["creator"],
            event_id=event.id,
            db_session=db_session,
            path_to_locales=path_to_locales
        )
        # user_in_db = db_session.query(user).filter_by(tg_id=from_json_data["creator"]).first()
        # event.attendees.append(user_in_db)

        response_text = f"Event {event.id} was published"

        db_session.commit()

        if group_id is not None:
            event_info, photo, amount_of_people, location = return_event_info_and_photo(db_session, event_id)
            temp_keyboard = [
                [InlineKeyboardButton(f"WAY_OUT_BOT", url="https://t.me/WAY_OUT_EVENTS_BOT")],
            ]
            if location[:8] == "location":
                temp_keyboard.insert(0, [InlineKeyboardButton(f"LOCATION", callback_data=f"show_event_location_{event_id}")])

            keyboard = InlineKeyboardMarkup(temp_keyboard)

            message = bot.send_photo(
                chat_id=group_id,
                photo=photo,
                caption=event_info,
                reply_markup=keyboard
            )

            bot.pin_chat_message(group_id, message.id)

    else:
        event = db_session.query(Event).filter_by(id=event_id).first()
        db_session.delete(event)

        response_text = f"Event {event.id} was deleted"
        db_session.commit()
    return response_text
