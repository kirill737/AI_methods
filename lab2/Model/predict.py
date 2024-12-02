"""
    Model file
"""
import torch
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer

np.random.seed(737)
torch.manual_seed(737)

def continue_text(text_to_continue: str,  max_length: int, top_k: int, top_p: float, temperature: float, no_repeat: int) -> str:
    """
        Параметры функции generate из ruGpt: <br>
        - prompt - исходная промпт-строка<br>
        - max_length - максимальная длина генерируемой последовательности токенов<br>
        - temperature - температура (модуляция вероятности следующего токена)<br>
        - top_k - топ по вероятности токенов для использования<br>
        - top_p - для генерации используются токены с кумулятивной вероятностью topp и более<br>
        - num_return_sequences - количество генерируемых последовательностей<br>
        - no_repeat_ngram_size - минимальная длина неповторяющейся последовательности слов<br>
        - repetition_penalty - Штраф за повторение слов. Чем выше значение, тем меньше модель будет повторять одинаковые слова. <br>
        - do_sample - флаг, несущий информацию о необходимости семплирования<br>

        Возвращаемое значение: <br>
        Функция возвращает список сгенерированных текстов. Размер списка равен num_return_sequences
    """

    model_name_or_path = "sberbank-ai/rugpt3medium_based_on_gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
    model = GPT2LMHeadModel.from_pretrained(model_name_or_path)
    input_ids = tokenizer.encode(text_to_continue, return_tensors="pt")
    out = model.generate(
        input_ids,
        max_length=max_length, # 100
        top_k=top_k, # 5
        top_p=top_p, # 0.9
        temperature=temperature, # 0.9
        repetition_penalty=5.0,
        no_repeat_ngram_size=no_repeat, # 3
        do_sample=True
    )
    generated_text = list(map(tokenizer.decode, out))[0]
    return generated_text

