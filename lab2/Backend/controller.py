"""
    Controller file
"""
from Model import predict

def continue_text(text_to_continue: str, max_length: int, top_k: int, top_p: float,
                  temperature: float, no_repeat: int) -> str:
    """
        Функция для взаимодействия между Model и View. 
    """
    return predict.continue_text(
        text_to_continue=text_to_continue,
        max_length=max_length,
        top_k=top_k,
        top_p=top_p,
        temperature=temperature,
        no_repeat=no_repeat
    )


