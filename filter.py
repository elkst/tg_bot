from aiogram import Bot, Dispatcher
from aiogram.filters import Filter
from aiogram.types import Message

#Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = ''


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class CustomFilter(Filter):
    def __init__(self, arg: str):
        self.arg = arg

    async def __call__(self, message: Message) -> bool:
        return message.text.startswith(self.arg)

async def custom_filter_handler(message: Message, arg: str):
    await message.answer(f"Аргумент: {arg}")

dp.message.register(custom_filter_handler, CustomFilter("/hello"))

if __name__ == '__main__':
    dp.run_polling(bot)
