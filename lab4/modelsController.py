from models.gpt_handler import GPTHandler
from models.llama_handler import LLaMAHandler

# Инициализация обработчиков для моделей GPT и LLaMA
gpt_handler = GPTHandler()
llama_handler = LLaMAHandler()

# Асинхронная функция для генерации текста с использованием выбранной модели
async def generate_completion(model: str, user_input: str) -> str:
    # Переменная для хранения результата
    result = "No result"
    # Проверка выбранной модели и вызов соответствующего обработчика
    if model == "GPT":
        print("Gpt обрабатывается")
        result = await gpt_handler.generate_text(user_input)
    elif model == "LLaMA":
        print("Lama обрабатывается")
        result = await llama_handler.generate_text(user_input)
    else:
        raise ValueError("Некорректная модель: выберите 'GPT' или 'LLaMA'.")
    return result
