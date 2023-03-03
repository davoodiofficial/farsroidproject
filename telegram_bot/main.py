from telethon.sync import TelegramClient
from telethon import events
import requests
from urllib.parse import quote
import json

api_id = 9774361
api_hash = 'd77b4befd171e96f29e47c6f2d2daa35'
bot_token = '5634331533:AAHEvxg6W7Egs3qV2XkJIe8_KOvmNF6K29U'

bot = TelegramClient('bot', api_id, api_hash, proxy=(
    "socks5", '127.0.0.1', 9150)).start(bot_token=bot_token)


@bot.on(events.NewMessage(incoming=True))
async def say_hi(event):
    response = ''
    message_text = event.raw_text
    print(message_text)
    if message_text.startswith('https://'):  # message is a link
        r = requests.get(
            f'http://127.0.0.1:8000/url/?url={quote(message_text)}')
        print(r.status_code)
        apps_data = json.loads(r.text)['app']
        await event.reply(json.dumps(apps_data, ensure_ascii=False))

print('bot is running')
bot.run_until_disconnected()
print('bot is stoped')
