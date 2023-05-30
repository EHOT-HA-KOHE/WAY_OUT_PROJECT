import json


def change_statuses_in_database(status: bool, message, db_session, user):
    data = {
        "reg_mes_id": message.id,
        "name": status,
        "sex": status,
        "age": status,
        "city": status,
        "info": status,
        "photo": status,
    }

    json_data = json.dumps(data)
    user_in_db = db_session.query(user).filter(user.tg_id == message.chat.id).first()
    user_in_db.statuses = json_data
    db_session.commit()
