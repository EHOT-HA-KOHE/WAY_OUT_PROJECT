from pyrogram import Client, filters


api_id_client = 22791055
api_hash_client = 'cc2abc27d2cf4a60cd560253709e2767'

client_chat_creator = Client('client_chat_creator_session', api_id_client, api_hash_client)


@client_chat_creator.on_message(filters.new_chat_members)
def auto_approve_join_requests(client, message):
    # client_chat_creator.send_message(691259064, "Hey!")
    # approve_chat_join_request()

    # client_chat_creator.get_chat_join_requests(chat_id=)
    # client_chat_creator.approve_chat_join_request(chat_id=, user_id=)

    print("Новый участник в чате:", message.new_chat_members)


if __name__ == '__main__':
    print('I AM ALIVE USER')
    client_chat_creator.run()
