from pyrogram import Client

# Создаем экземпляр клиента Pyrogram
api_id = 22791055
api_hash = 'cc2abc27d2cf4a60cd560253709e2767'
client = Client('my_session', api_id, api_hash)

# Вход в аккаунт Telegram
client.start()

# Создание новой группы
group = client.create_group(title='New Group', users=['kirshine',])

# Получение идентификатора созданной группы
group_id = group.id

# Приглашение участников в группу
users_to_invite = ['vanchouz',]
client.add_chat_members(chat_id=group_id, user_ids=users_to_invite)

# Остановка клиента
client.stop()
