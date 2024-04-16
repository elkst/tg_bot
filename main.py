import requests
import time

API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '6991693139:AAG17hXLvCa_uNym25JCdsrvXri4J7zYAug'
ERROR_TEXT = 'ERROR_404'

offset = -2
counter = 0
cat_response: requests.Response
cat_link: str


def send_photo(chat_id, photo_url):
    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={photo_url}')


def send_message(chat_id, text):
    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')


def send_video(chat_id, video_url):
    requests.get(f'{API_URL}{BOT_TOKEN}/sendVideo?chat_id={chat_id}&video={video_url}')


def send_voice(chat_id, voice_url):
    requests.get(f'{API_URL}{BOT_TOKEN}/sendVoice?chat_id={chat_id}&voice={voice_url}')


while counter < 100:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            message_text = result['message'].get('text', '')

            # Обработчик текстовых сообщений
            if message_text:
                send_message(chat_id, f'Ты отправил мне текст: "{message_text}"')

            # Обработчик фото
            if 'photo' in result['message']:
                send_message(chat_id, 'Ого, ты мне прислал фото!')

            # Обработчик стикеров
            if 'sticker' in result['message']:
                send_message(chat_id, 'Ого, ты мне прислал стикер!')

            # Обработчик GIF
            if 'document' in result['message'] and result['message']['document']['mime_type'] == 'video/mp4':
                send_message(chat_id, 'Ого, ты мне прислал GIF!')

            # Обработчик видео
            if 'video' in result['message']:
                send_message(chat_id, 'Ого, ты мне прислал видео!')

            # Обработчик голосовых сообщений
            if 'voice' in result['message']:
                send_message(chat_id, 'Ого, ты мне прислал голосовое сообщение!')

            # Обработчик файлов
            if 'document' in result['message']:
                send_message(chat_id, 'Ого, ты мне прислал файл!')

            # Обработчик геопозиции
            if 'location' in result['message']:
                send_message(chat_id, 'Ого, ты мне прислал геопозицию!')

            # Обработчик музыки
            if 'audio' in result['message']:
                send_message(chat_id, 'Ого, ты мне прислал музыку!')

            # Обработчик контактов
            if 'contact' in result['message']:
                send_message(chat_id, 'Ого, ты мне прислал контакт!')


    time.sleep(1)
    counter += 1
