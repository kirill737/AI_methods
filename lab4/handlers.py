from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Message
from modelsController import generate_completion
import logging
import enum

# Настройка логирования для отслеживания работы приложения
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Перечисление доступных команд
class Commands(enum.Enum):
    start = "/start"
    stop = "/stop"
    
# Перечисление возможных стадий взаимодействия с ботом
class Stages(enum.Enum):
    start = "starting"
    choose_model = "choosing_model"
    enter_topic = "entering_topic"
    generate_fact = "generating_fact"

# Перечисление доступных опций
class Options(enum.Enum):
    choose_topic_text = "Выбрать тему"
    choose_model_text = "Выбрать модель"

# Клавиатуры для взаимодействия с пользователем
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=Commands.start.value)]],
    resize_keyboard=True
)

choose_model_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="GPT"), KeyboardButton(text="LLaMA")],
        [KeyboardButton(text=Commands.stop.value)]
    ],
    resize_keyboard=True
)

regenerate_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Options.choose_topic_text.value)],
        [KeyboardButton(text=Options.choose_model_text.value), KeyboardButton(text=Commands.stop.value)]
    ],
    resize_keyboard=True
)

switch_model_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Options.choose_model_text.value)],
        [KeyboardButton(text=Commands.stop.value)]
    ],
    resize_keyboard=True
)

# Переменные для отслеживания текущего состояния
current_stage = Stages.start.value
current_model = None
current_topic = None

# Обработчик команды /start
async def start_handler(message: Message) -> None:
    global current_stage
    current_stage = Stages.choose_model.value
    logging.info(f"Команда {Commands.start.value} от пользователя с ID: {message.from_user.id}")
    await message.answer(
        "Привет! Это бот для генерации фактов.\n\nВыберите модель для генерации:",
        reply_markup=choose_model_keyboard
    )

# Обработчик команды /stop
async def stop_handler(message: Message) -> None:
    global current_stage
    current_stage = Stages.start.value
    logging.info(f"Команда /stop от пользователя с ID: {message.from_user.id}")
    await message.answer("Работа завершена. Введите /start для начала заново.", reply_markup=start_keyboard)

# Обработчик команды смены модели
async def change_model_handler(message: Message) -> None:
    global current_stage
    current_stage = Stages.choose_model.value
    logging.info(f"Команда смены модели от пользователя с ID: {message.from_user.id}")
    await message.answer("Выберите новую модель:", reply_markup=choose_model_keyboard)

# Основной обработчик взаимодействия
async def handle_interaction(message: Message) -> None:
    global current_stage, current_model, current_topic
    user_input = message.text.strip()

    if current_stage == Stages.choose_model.value:
        if user_input in ["GPT", "LLaMA"]:
            current_model = user_input
            current_stage = Stages.enter_topic.value
            await message.answer(
                f"Вы выбрали модель {current_model}.\nВведите тему, чтобы сгенерировать интересный факт.",
                reply_markup=ReplyKeyboardRemove()
            )
        elif user_input == Commands.stop.value:
            await stop_handler(message)
        else:
            await message.answer("Пожалуйста, выберите модель: GPT или LLaMA.", reply_markup=choose_model_keyboard)

    elif current_stage == Stages.enter_topic.value:
        if user_input:
            current_topic = user_input
            current_stage = Stages.generate_fact.value
            await generate_fact_handler(message, current_topic)
        else:
            await message.answer("Введите корректную тему.")

    elif current_stage == Stages.generate_fact.value:
        await regenerate_or_switch_handler(message)
    else:
        await message.answer("Введите /start для начала работы.", reply_markup=start_keyboard)

# Генерация факта и предоставление опций
async def generate_fact_handler(message: Message, topic: str) -> None:
    global current_model
    try:
        await message.answer(
            f"Запрос обрабатывается...\nПока можете выбрать другую тему.",
            reply_markup=regenerate_keyboard
        )
        result = await generate_completion(current_model, topic)
        await message.answer(
            f"Сгенерированный факт:\n{result}",
            reply_markup=regenerate_keyboard
        )
    except Exception as e:
        logging.error(f"Ошибка генерации: {e}")
        await message.answer(f"Ошибка генерации: {e}")

# Обработчик повторной генерации и смены модели
async def regenerate_or_switch_handler(message: Message) -> None:
    global current_stage
    user_input = message.text.strip()

    if user_input == Options.choose_topic_text.value:
        current_stage = Stages.enter_topic.value
        await message.answer("Введите новую тему для генерации факта:", reply_markup=ReplyKeyboardRemove())
    elif user_input == Options.choose_model_text.value:
        current_stage = Stages.choose_model.value
        await message.answer("Выберите новую модель:", reply_markup=choose_model_keyboard)
    elif user_input == Commands.stop.value:
        await stop_handler(message)
    else:
        logging.info(f"Неверное действие от пользователя с ID: {message.from_user.id}")
        await message.answer("Пожалуйста, выберите действие.", reply_markup=regenerate_keyboard)

# Регистрация обработчиков
def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(stop_handler, commands=["stop"])
    dp.register_message_handler(change_model_handler, lambda message: message.text == Options.choose_model_text.value)
    dp.register_message_handler(handle_interaction)
