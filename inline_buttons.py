from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command

# Токен бота
BOT_TOKEN = ''  # Замените на ваш токен

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
async def start_command(message: types.Message):
    web_app_url = "https://your-app-name.glitch.me/"  # Web App на Glitch

    # Создаем кнопку Web App
    web_app_button = InlineKeyboardButton(text="Открыть Web App", web_app=WebAppInfo(url=web_app_url))

    # Создаем разметку для клавиатуры с кнопкой
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])

    # Отправляем сообщение с клавиатурой
    await bot.send_message(chat_id=message.chat.id, text="Нажми на кнопку ниже, чтобы открыть веб-приложение:",
                           reply_markup=inline_kb)


# Регистрация хендлера
dp.message.register(start_command, Command("start"))

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)
