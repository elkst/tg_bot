from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import logging

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Токен бота
BOT_TOKEN = '6991693139:AAGOoRXqVOq42sfrYA0oyYDCc42uQGiHZAI'  # Замените на ваш токен

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализируем билдер
kb_builder = ReplyKeyboardBuilder()

# Создаем кнопки
survey_btn = KeyboardButton(text='Пройти опрос')
quiz_btn = KeyboardButton(text='Пройти викторину')

# Добавляем кнопки в билдер
kb_builder.row(survey_btn, quiz_btn, width=2)

# Создаем объект клавиатуры
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

# Опросные вопросы и варианты ответов
survey_questions = [
    ("Какой ваш любимый цвет?", ["Красный", "Синий", "Зеленый"]),
    ("Какой ваш любимый сезон?", ["Весна", "Лето", "Осень"]),
    ("Какой ваш любимый спорт?", ["Футбол", "Теннис", "Баскетбол"]),
]

# Викторинные вопросы, варианты ответов и правильные ответы
quiz_questions = [
    ("Какая планета самая большая в Солнечной системе?", ["Земля", "Юпитер", "Марс"], "Юпитер"),
    ("Какой элемент химической таблицы обозначается символом 'O'?", ["Золото", "Кислород", "Натрий"], "Кислород"),
    ("Какой океан самый глубокий?", ["Тихий", "Атлантический", "Индийский"], "Тихий"),
]

# Переменные для хранения состояния пользователя
user_data = {}

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Выберите, что хотите сделать:", reply_markup=keyboard)

# Обработчик кнопки "Пройти опрос"
@dp.message(lambda message: message.text == 'Пройти опрос')
async def start_survey(message: Message):
    user_data[message.from_user.id] = {"survey_step": 0}
    await ask_survey_question(message)

async def ask_survey_question(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["survey_step"]
    question, options = survey_questions[step]
    kb_builder = ReplyKeyboardBuilder()
    for option in options:
        kb_builder.button(text=option)
    keyboard = kb_builder.as_markup(resize_keyboard=True)
    await message.answer(question, reply_markup=keyboard)

@dp.message(lambda message: message.text in [option for q, o in survey_questions for option in o])
async def handle_survey_answer(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["survey_step"]
    user_data[user_id].setdefault("survey_answers", []).append(message.text)

    # Если есть еще вопросы
    if step + 1 < len(survey_questions):
        user_data[user_id]["survey_step"] += 1
        await ask_survey_question(message)
    else:
        await message.answer("Спасибо за участие в опросе!", reply_markup=keyboard)

# Обработчик кнопки "Пройти викторину"
@dp.message(lambda message: message.text == 'Пройти викторину')
async def start_quiz(message: Message):
    user_data[message.from_user.id] = {"quiz_step": 0}
    await ask_quiz_question(message)

async def ask_quiz_question(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["quiz_step"]
    question, options, _ = quiz_questions[step]
    kb_builder = ReplyKeyboardBuilder()
    for option in options:
        kb_builder.button(text=option)
    keyboard = kb_builder.as_markup(resize_keyboard=True)
    await message.answer(question, reply_markup=keyboard)

@dp.message(lambda message: message.text in [option for q, o, a in quiz_questions for option in o])
async def handle_quiz_answer(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["quiz_step"]
    _, _, correct_answer = quiz_questions[step]

    if message.text == correct_answer:
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {correct_answer}")

    # Если есть еще вопросы
    if step + 1 < len(quiz_questions):
        user_data[user_id]["quiz_step"] += 1
        await ask_quiz_question(message)
    else:
        await message.answer("Викторина окончена!", reply_markup=keyboard)

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)
