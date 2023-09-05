from time import sleep

from pyrogram import Client, filters
from pyrogram.errors import FloodWait


api_id_client = 21405010
api_hash_client = 'f02ca9c4a50a86708d782b83682c2327'

client_chat_fun_mes = Client('client_chat_fun_mes_session', api_id_client, api_hash_client)


# Команда type
@client_chat_fun_mes.on_message(filters.command("t", prefixes=".") & filters.me)
def type(_, msg):
    orig_text = msg.text.split(".t ", maxsplit=1)[1]
    text = orig_text
    tbp = ""  # to be printed
    typing_symbol = "▒"
    # typing_symbol = "🙀"

    while (tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.04)  # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.05)

        except FloodWait as e:
            sleep(e.x)
        
            
if __name__ == '__main__':
    print('I AM ALIVE FUN MESSAGE MODE')
    client_chat_fun_mes.run()

