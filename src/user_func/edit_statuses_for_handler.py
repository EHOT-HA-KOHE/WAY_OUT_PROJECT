import json


def edit_statuses_in_database(status: bool, reason, message, db_session, user):
    if reason == "user":
        data = {
            "mes_id": message.id,
            "name": status,
            "sex": status,
            "age": status,
            "city": status,
            "info": status,
            "photo": True,
        }

        json_data = json.dumps(data)
        user_in_db = db_session.query(user).filter(user.tg_id == message.chat.id).first()
        user_in_db.statuses_edit_user = json_data

    elif reason == "event":
        data = {
            "mes_id": message.id,
            "category_name": status,
            "creator": status,
            "title": status,
            "description": status,
            "city": status,
            "max_amount_of_people": status,
            "date": status,
            "location": True,
            "photo": True,
            "make_group": True
        }

        json_data = json.dumps(data)
        user_in_db = db_session.query(user).filter(user.tg_id == message.chat.id).first()
        user_in_db.statuses_edit_event = json_data

    db_session.commit()
