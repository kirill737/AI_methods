from dotenv import load_dotenv
import aiohttp
import os
import logging

# Загрузка переменных окружения из файла .env
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")  # Токен API для доступа к Hugging Face
API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"

class GPTHandler:
    def __init__(self):
        # Заголовки для авторизации в Hugging Face API
        self.headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        # Системное сообщение для настройки контекста модели
        self.system = """
        I am an assistant for creating interesting facts about the Dota 2 game.
        All my facts from the Dota 2 game are correlating with real dota 2 information.
        """

    async def generate_text(self, user_input: str) -> str:
        logging.info(f"Enter gen_text: {user_input}")
        # Создание текста-запроса для модели
        prompt = f"{self.system} Here is a fact {user_input}: "
        payload = {
            "inputs": prompt,
            "parameters": {
                "do_sample": True,
                "max_new_tokens": 250,
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 0.9
            }
        }

        # Использование aiohttp для асинхронного HTTP-запроса
        async with aiohttp.ClientSession() as session:
            try:
                # Логирование запроса
                logging.info(f"Sending request to {API_URL} with prompt: {prompt}")
                # Асинхронная отправка POST-запроса
                async with session.post(API_URL, headers=self.headers, json=payload) as response:
                    if response.status == 200:  # Успешный запрос
                        result = await response.json()

                        # Получение сгенерированного текста из ответа
                        generated_text = result[0].get("generated_text", "Нет сгенерированного текста")
                        logging.info(f"Generated text: {generated_text}")

                        # Удаление исходного запроса из текста
                        return generated_text[len(prompt):].strip()
                    else:
                        error_message = f"Error {response.status}: {await response.text()}"
                        logging.error(error_message)
                        return error_message
            except Exception as e:
                error_message = f"Ошибка при работе с GPT: {e}"
                logging.error(error_message)
                return error_message
