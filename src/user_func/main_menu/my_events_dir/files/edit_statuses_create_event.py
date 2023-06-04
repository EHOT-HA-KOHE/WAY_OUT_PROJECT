import json


def edit_statuses_create_event_in_database(status: bool, message, db_session, user):
    data = {
        "mes_id": message.id,
        # "categories": status,
        "date": status,
        "description": status,
        "title": status,
        "city": status,
        "photo": status,
        "location": status,
    }

    json_data = json.dumps(data)
    user_in_db = db_session.query(user).filter(user.tg_id == message.chat.id).first()
    user_in_db.statuses_edit_user = json_data
    db_session.commit()
