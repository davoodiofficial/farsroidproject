from telethon.sync import TelegramClient
from telethon import events
import requests
from urllib.parse import quote, urlsplit, parse_qs
import json

api_id = 9774361
api_hash = 'd77b4befd171e96f29e47c6f2d2daa35'
bot_token = '5634331533:AAHEvxg6W7Egs3qV2XkJIe8_KOvmNF6K29U'

API_HOST = 'myfastapi'
API_PORT = '80'

MAX_MESSAGE_SIZE = 4096

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


@bot.on(events.NewMessage(incoming=True))
async def say_hi(event):
    response: str = ''
    message_text: str = event.raw_text
    print("it's working")
    if message_text.startswith('https://'):  # message is a link
        query = urlsplit(message_text).query
        params = parse_qs(query)
        id_ = params.get('id')
        if id_ is None:
            response = 'cann not get id from given URL'
        else:
            id_ = id_[0]
            app_url = f'https://play.google.com/store/apps/details?id={id_}'
            r = requests.get(
                f'http://{API_HOST}:{API_PORT}/url/?url={quote(app_url)}')
            if r.status_code != 200:
                response = 'API does not respond'
            else:
                apps_data = json.loads(r.text)['app']
                for app in apps_data:
                    response += f"farsi name: {app['fa_name']}\n"
                    response += f"english name: {app['en_name']}\n"
                    for info in app['download_box']:
                        response += f"{info}: {app['download_box'][info]}\n"
                    response += f"farsroid link : {app['farsroid_link']}\n"
                    for download_link in app['download_links']:
                        response += f"{download_link}: {app['download_links'][download_link]}\n"
    else:
        app_name = message_text
        r = requests.get(
            f'http://{API_HOST}:{API_PORT}/name/?fa_name={quote(app_name)}&en_name={quote(app_name)}')
        if r.status_code != 200:
            response = 'API does not respond'
        else:
            apps_data = json.loads(r.text)['app']
            if not apps_data:
                response = f'apps with name {app_name} did not found'
            else:
                for app in apps_data:
                    response += f"farsi name: {app['fa_name']}\n"
                    response += f"english name: {app['en_name']}\n"
                    for info in app['download_box']:
                        response += f"{info}: {app['download_box'][info]}\n"
                    response += f"farsroid link : {app['farsroid_link']}\n"
                    for download_link in app['download_links']:
                        response += f"{download_link}: {app['download_links'][download_link]}\n"

    index = 0
    response_len = len(response)
    if response_len > MAX_MESSAGE_SIZE:
        for i in range(0, response_len // MAX_MESSAGE_SIZE, 1):
            await event.reply(response[i * MAX_MESSAGE_SIZE:(i + 1) * MAX_MESSAGE_SIZE])
        await event.reply(response[(i + 1) * MAX_MESSAGE_SIZE::])
    else:
        await event.reply(response)

print('bot is running')
bot.run_until_disconnected()
print('bot is stoped')
