from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram import F



# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '6991693139:AAG17hXLvCa_uNym25JCdsrvXri4J7zYAug'


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()




# Этот хэндлер будет срабатывать на команду "/start"
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут volte_bot!\nНапиши мне что-нибудь')




# Этот хэндлер будет срабатывать на команду "/help"
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )




# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
async def send_echo(message: Message):
    await message.reply(text=message.text)



# Этот хэндлер будет срабатывать на отправку боту фото
async def send_photo_echo(message: Message):
    print(message)
    await message.reply_photo(message.photo[0].file_id)


# Обработчик для стикеров
async def sand_sticker_echo(message: types.Message):
    # Отправляем стикер обратно пользователю
    await bot.send_sticker(message.chat.id, message.sticker.file_id)

# Обработчик для видео
async def sand_video_echo(message: types.Message):
    # Отправляем видео обратно пользователю
    await bot.send_video(message.chat.id, message.video.file_id)


async def sand_audio_echo(message: types.Message):
    # Отправляем видео обратно пользователю
    await bot.send_video(message.chat.id, message.audio.file_id)



# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)
dp.message.register(sand_sticker_echo, F.content_type == ContentType.STICKER)
dp.message.register(sand_video_echo, F.content_type == ContentType.VIDEO)
dp.message.register(sand_audio_echo, F.content_type == ContentType.AUDIO)
dp.message.register(send_echo)


if __name__ == '__main__':
    dp.run_polling(bot)
