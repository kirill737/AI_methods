import http.client
import json
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

sys.stdout.reconfigure(encoding='utf-8')

# dotend
# Функция для теста Microsoft Translator
def testMicrosoftAPI(textToTranslate:str, fromLanguage:str, toLanguage:str)->str:
    conn = http.client.HTTPSConnection("microsoft-translator-text.p.rapidapi.com")

    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "e3b15f62f3mshcdfd2a7a42b9a8ep102506jsn6f3828de672f",
        'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com"
    }

    body = json.dumps([{"Text": textToTranslate}])
    params = f"/translate?api-version=3.0&from={fromLanguage}&to={toLanguage}"

    # Выполняем запрос
    conn.request("POST", params, body, headers)
    res = conn.getresponse()
    data = res.read()
    translated_text = json.loads(data.decode("utf-8"))
    
    result = translated_text[0]['translations'][0]['text']
    return result

# Функция для теста Google Translate
def testGoogleAPI(textToTranslate, fromLanguage, toLanguage):
    conn = http.client.HTTPSConnection("google-translator9.p.rapidapi.com")

    payload = json.dumps({
        "q": textToTranslate,
        "source": fromLanguage,
        "target": toLanguage
    })

    headers = {
        'x-rapidapi-key': "e3b15f62f3mshcdfd2a7a42b9a8ep102506jsn6f3828de672f",
        'x-rapidapi-host': "google-translator9.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    
    conn.request("POST", "/v2", payload, headers)
    res = conn.getresponse()
    data = res.read()
    translated_text = json.loads(data.decode("utf-8"))

    result = translated_text['data']['translations'][0]['translatedText']
    return result

# Функция для тестирования
def testBySequence(textToTranslate, sequence, translateFunc):
    tmpTextToTranslate = textToTranslate

    for lanIndex in range(1, len(sequence)):
        tmpTextToTranslate = translateFunc(tmpTextToTranslate, sequence[lanIndex - 1], sequence[lanIndex])
        print(f"{sequence[lanIndex - 1]} -> {sequence[lanIndex]}: {tmpTextToTranslate}")

    print(f"Final result:   {tmpTextToTranslate}")
    return tmpTextToTranslate

def run_tests():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Предупреждение", "Введите текст в первое окно.")
        return

    languageSequence = ["ru", "en", "fr", "de", "en", "es", "kk", "en", "ru"]

    # Получение результатов тестов
    microsoft_result = testBySequence(input_text, languageSequence, testMicrosoftAPI)
    google_result = testBySequence(input_text, languageSequence, testGoogleAPI)

    # Вывод результатов в соответствующие окна
    result_microsoft.config(state=tk.NORMAL)
    result_microsoft.delete("1.0", tk.END)
    result_microsoft.insert(tk.END, microsoft_result)

    result_google.config(state=tk.NORMAL)
    result_google.delete("1.0", tk.END)
    result_google.insert(tk.END, google_result)

def run_pre_tests():
    test_text = "Начиная жизнеописание героя моего, Алексея Федоровича Карамазова, нахожусь в некотором недоумении. А именно: хотя я и называю Алексея Федоровича моим героем, но, однако, сам знаю, что человек он отнюдь не великий, а посему и предвижу неизбежные вопросы вроде таковых: чем же замечателен ваш Алексей Федорович, что вы выбрали его своим героем? Что сделал он такого? Кому и чем известен? Почему я, читатель, должен тратить время на изучение фактов его жизни?"
    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, test_text)
    run_tests()

# UI
root = tk.Tk()
root.title("Переводчик")
root.geometry("600x500")
gray = "#262626"
root.configure(bg="black")

text_input = scrolledtext.ScrolledText(root, height=4, width=50, bg=gray, fg="white", bd=0, font=("Arial", 12), highlightthickness=1, highlightbackground=gray)
text_input.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

microsoft_label = tk.Label(root, text="Microsoft", bg="black", fg="white", font=("Arial", 12, "bold"))
microsoft_label.grid(row=1, column=0, padx=10, pady=5)

result_microsoft = scrolledtext.ScrolledText(root, height=10, width=25, bg=gray, fg="white", bd=0, font=("Arial", 12), highlightthickness=1, highlightbackground=gray)
result_microsoft.grid(row=2, column=0, padx=10, pady=10)


google_label = tk.Label(root, text="Google", bg="black", fg="white", font=("Arial", 12, "bold"))
google_label.grid(row=1, column=1, padx=10, pady=5)

result_google = scrolledtext.ScrolledText(root, height=10, width=25, bg=gray, fg="white", bd=0, font=("Arial", 12), highlightthickness=1, highlightbackground=gray)
result_google.grid(row=2, column=1, padx=10, pady=10)


run_button = tk.Button(root, text=" Запуск тестов ", command=run_tests, bg=gray, fg="white", bd=2, font=("Arial", 12))
run_button.grid(row=3, column=0, columnspan=2, pady=10)

run_pre_button = tk.Button(root, text=" Запуск предварительных тестов ", command=run_pre_tests, bg=gray, fg="white", bd=2, font=("Arial", 12))
run_pre_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()