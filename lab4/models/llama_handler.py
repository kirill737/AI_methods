from dotenv import load_dotenv
from huggingface_hub import AsyncInferenceClient
import os


# Загрузка переменных окружения из файла .env
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

class LLaMAHandler:
    def __init__(self):
        # Инициализация асинхронного клиента Hugging Face
        self.client = AsyncInferenceClient(api_key=HF_API_TOKEN)
        self.headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        # Системное сообщение для определения поведения модели
        self.system = """
        Ты помощник для создания интересных фактов по игре Dota 2.
        Удостоверься, что факт соответствуют реальной информации из игры Dota 2.
        Все факты должны соответствовать теме, указанной пользователем.
        От тебя я жду ответ строго на русском языке, английский можешь использовать
        только для игровых терминов.
        Перед ответом удостоверься, что твой ответ корректен и соответствует 
        реальным фактам из игры Dota 2.
        Если вопрос не связан с Dota 2, то выведи "Мне кажется, что ваш вопрос 
        не относится к Dota 2. Попробуйте сформулировать его ещё раз"
        """

    async def generate_text(self, user_input: str) -> str:
        # Асинхронный метод для генерации текста на основе входных данных пользователя
        try:
            messages = [
                {
                    "role": "system",
                    "content": self.system
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            # Вызов метода создания чата с использованием Hugging Face API
            output = await self.client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct",
                messages=messages, 
                max_tokens=200,
                temperature=0.6,
                top_p=0.9,
            )
        except Exception as e:
            return f"Ошибка при работе с LLaMA: {e}"
        return output.choices[0].message.content
