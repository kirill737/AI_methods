"""
    View file
"""
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from Backend import controller

def load_text_from_file() -> None:
    """
        Функция для загрузки исходного текста из файла.
    """
    file_path = filedialog.askopenfilename(
        title="Выберите текстовый файл",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                text = file.read()
                text_input_field.delete("1.0", tk.END)  # Очищаем текстовое поле
                text_input_field.insert(tk.END, text)  # Вставляем текст из файла
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")


def gen_result() -> None:
    """
        Получает данные из полей для ввода, обрабатывает их<br>
        и записывает сгенерированный текст в поле вывода.
    """

    # Заглушка для отображение процесса генерации текста
    output_field.delete("1.0", tk.END)
    output_field.insert(tk.END, "Текст генерируется...")

    # Получение значений из полей для ввода
    input_text = text_input_field.get("1.0", tk.END).strip()
    max_length = max_lenght_input_field.get().strip()
    no_repeat = no_repeat_input_field.get().strip()
    top_k = top_k_input_field.get().strip()
    top_p = top_p_input_field.get().strip()
    temperature = temp_input_field.get().strip()
    no_repeat = no_repeat_input_field.get().strip()

    max_length = 100 if not max_length else int(max_length)
    top_k = 5 if not top_k else int(top_k)
    top_p = 0.9 if not top_p else float(top_p)
    temperature = 0.9 if not temperature else float(temperature)
    no_repeat = 3 if not no_repeat else int(no_repeat)
    
    result = controller.continue_text(
        text_to_continue=input_text,
        max_length=max_length,
        top_k=top_k,
        top_p=top_p,
        temperature=temperature,
        no_repeat=no_repeat
    )
    output_field.delete("1.0", tk.END)
    output_field.insert(tk.END, result)

def show_UI() -> None:
    """
        Отображает интерфейс приложения.
    """
    root.mainloop()

# Создание интерфейса и его первоначальная настройка
root = tk.Tk()
root.title("Генератор текста на ruGPT")
root.geometry("1000x360")
gray = "#262626"
root.configure(bg="black")

# Вёрстка поле ввода текста
text_input_field = ScrolledText(
    root, height=5, width=60,
    bg=gray, fg="white", bd=0,
    font=("Arial", 12),
    highlightthickness=1, 
    highlightbackground=gray, 
    insertbackground="gray"
)

text_input_field.grid(
    row=0, column=0,
    columnspan=2, rowspan=3,
    pady=10, padx=10
)

# Вёрстка поля ввода максимальной длины получаемого текста
max_lenght_label = tk.Label(
    root, text="Макс. длина текста:",
    bg="black", fg="white", font=("Arial", 12, "bold")
    # insertbackground="gray"
)
max_lenght_label.grid(row=0, column=2, padx=2, pady=2)
max_lenght_input_field = tk.Entry(
    root, width=5,
    bg=gray, fg="white", bd=0,
    font=("Arial", 12),
    highlightthickness=1,
    highlightbackground=gray
)
max_lenght_input_field.grid(row=0, column=3, pady=2, padx=2)

# Вёрстка поля ввода длини без повторений получаемого текста
no_repeat_label = tk.Label(
    root, text="Размер неповторяемых n-грамм:",
    bg="black", fg="white", font=("Arial", 12, "bold")
)
no_repeat_label.grid(row=1, column=2, padx=2, pady=2)
no_repeat_input_field = tk.Entry(
    root, width=5, 
    bg=gray, fg="white", bd=0, 
    font=("Arial", 12), 
    highlightthickness=1, 
    highlightbackground=gray,
    insertbackground="gray"
)
no_repeat_input_field.grid(row=1, column=3, pady=2, padx=2)




# Вёрстка поля ввода длини без повторений получаемого текста
top_k_label = tk.Label(
    root, text="top k:",
    bg="black", fg="white", font=("Arial", 12, "bold")
)
top_k_label.grid(row=2, column=2, padx=2, pady=2)
top_k_input_field = tk.Entry(
    root, width=5, 
    bg=gray, fg="white", bd=0, 
    font=("Arial", 12), 
    highlightthickness=1, 
    highlightbackground=gray,
    insertbackground="gray"
)
top_k_input_field.grid(row=2, column=3, pady=2, padx=2)

# Вёрстка поля ввода длини без повторений получаемого текста
top_p_label = tk.Label(
    root, text="top p:",
    bg="black", fg="white", font=("Arial", 12, "bold")
)
top_p_label.grid(row=3, column=2, padx=2, pady=2)
top_p_input_field = tk.Entry(
    root, width=5, 
    bg=gray, fg="white", bd=0, 
    font=("Arial", 12), 
    highlightthickness=1, 
    highlightbackground=gray,
    insertbackground="gray"
)
top_p_input_field.grid(row=3, column=3, pady=2, padx=2)

# Вёрстка поля ввода длини без повторений получаемого текста
temp_label = tk.Label(
    root, text="Температура:",
    bg="black", fg="white", font=("Arial", 12, "bold")
)
temp_label.grid(row=4, column=2, padx=2, pady=2)
temp_input_field = tk.Entry(
    root, width=5, 
    bg=gray, fg="white", bd=0, 
    font=("Arial", 12), 
    highlightthickness=1, 
    highlightbackground=gray,
    insertbackground="gray"
)
temp_input_field.grid(row=4, column=3, pady=2, padx=2)


# Вёрстка поля с результатом
output_field = ScrolledText(
    root, height=10, width=60,
    bg=gray, fg="white", bd=0, 
    font=("Arial", 12), 
    highlightthickness=1, 
    highlightbackground=gray,
    insertbackground="gray"
)
output_field.grid(
    row=3, column=0,
    columnspan=2, rowspan=6,
    pady=10, padx=10
)

# Вёрстка кнопки загрзки файла 
file_button = tk.Button(
    root, 
    text="Загрузить текст из файла",
    command=load_text_from_file,
    bg=gray, fg="white", 
    bd=2, font=("Arial", 12)
)
file_button.grid(
    row=5, column=2, 
    rowspan=1,
    pady=10, padx=10
)

# Вёрстка кнопки запуска генерации
run_button = tk.Button(
    root, 
    text="Сгенерировать текст",
    command=gen_result,
    bg=gray, fg="white", 
    bd=2, font=("Arial", 12)
)
run_button.grid(
    row=6, column=2, 
    rowspan=1,
    pady=10, padx=10
)

