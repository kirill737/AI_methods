import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv

from handlers import start_handler, stop_handler, handle_interaction

# Загрузка переменных окружения из файла .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Получение токена бота из переменных окружения

# Инициализация экземпляра бота
bot = Bot(token=BOT_TOKEN)
# Инициализация диспетчера для управления обработкой событий
dp = Dispatcher()

# Регистрация команд
dp.message.register(start_handler, Command("start"))
dp.message.register(stop_handler, Command("stop"))
dp.message.register(handle_interaction)

# Основная асинхронная функция запуска бота
async def main():
    print("Бот запущен")
    await dp.start_polling(bot)  # Запуск процесса получения и обработки обновлений

if __name__ == "__main__":
    asyncio.run(main())  # Асинхронный запуск основного цикла
