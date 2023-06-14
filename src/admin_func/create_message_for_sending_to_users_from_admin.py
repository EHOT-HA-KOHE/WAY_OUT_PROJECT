# import json
#
#
# def change_json_with_data_to_send_mes_to_users_from_admin(key, key_data):
#     # Открываем JSON-файл для чтения
#     with open("data_for_sending_mes_to_users_from_admin.json", "r") as file:
#         data = json.load(file)
#
#     # Изменяем часть JSON-данных
#     data[f"{key}"] = f"{key_data}"
#
#     # Открываем JSON-файл для записи
#     with open("data_for_sending_mes_to_users_from_admin.json", "w") as file:
#         json.dump(data, file, indent=4)
#
#
# def return_data_to_send_mes_to_users_from_admin(key, key_data):
#     return response_text, photo, link