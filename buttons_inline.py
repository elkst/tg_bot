from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = 'token'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

LEXICON: dict[str, str] = {
    'but_1': 'Кнопка 1',
    'but_2': 'Кнопка 2',
    'but_3': 'Кнопка 3',
    'but_4': 'Кнопка 4',
    'but_5': 'Кнопка 5',
    'back_to_main': 'Вернуться в главное меню',
    'proverb': 'Написать пословицу',
    'message': 'Напечатать сообщение',
}

BUTTONS: dict[str, str] = {
    'btn_1': '1',
    'btn_2': '2',
    'btn_3': '3',
    'btn_4': '4',
    'btn_5': '5',
    'btn_6': '6',
    'btn_7': '7',
    'btn_8': '8',
    'btn_9': '9',
    'btn_10': '10',
    'btn_11': '11'
}

# Функция для генерации инлайн-клавиатур "на лету"
def create_inline_kb(width: int,
                     *args: str,
                     last_btn: str | None = None,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'
        ))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Хэндлер для обработки команды "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    keyboard = create_inline_kb(2, 'but_1', 'but_2', 'but_3', 'but_4', 'but_5')
    await message.answer(
        text='Это главное меню с 5 кнопками.',
        reply_markup=keyboard
    )

# Хэндлер для обработки колбэков от первой кнопки
@dp.callback_query(lambda c: c.data in ['but_1', 'but_2', 'but_3', 'but_4', 'but_5'])
async def process_main_buttons(callback: CallbackQuery):
    # Генерация клавиатуры с 3 кнопками (подменю)
    keyboard = create_inline_kb(1, 'back_to_main', 'proverb', 'message')
    await callback.message.edit_text(
        text=f"Вы выбрали {LEXICON[callback.data]}.\nВот подменю:",
        reply_markup=keyboard
    )

# Хэндлер для возврата в главное меню
@dp.callback_query(lambda c: c.data == 'back_to_main')
async def process_back_to_main(callback: CallbackQuery):
    # Генерация клавиатуры для главного меню
    keyboard = create_inline_kb(2, 'but_1', 'but_2', 'but_3', 'but_4', 'but_5')
    await callback.message.edit_text(
        text="Вы вернулись в главное меню с 5 кнопками.",
        reply_markup=keyboard
    )

# Хэндлер для обработки пословицы
@dp.callback_query(lambda c: c.data == 'proverb')
async def process_proverb(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Вот пример пословицы: 'Без труда не выловишь и рыбку из пруда.'"
    )

# Хэндлер для печати сообщения
@dp.callback_query(lambda c: c.data == 'message')
async def process_message(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Напишите любое сообщение в ответ."
    )

if __name__ == '__main__':
    dp.run_polling(bot)
