from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests

def update_b1_label(event):
    code = base1_combobox.get()
    name = currencies.get(code, "")
    b1_label.config(text=name)


def update_b2_label(event):
    code = base2_combobox.get()
    name = currencies.get(code, "")
    b2_label.config(text=name)

def update_t_label(event):
    code = target_combobox.get()
    name = currencies[code]
    t_label.config(text=name)

def exchange():
    target_code = target_combobox.get()
    base1_code = base1_combobox.get()
    base2_code = base2_combobox.get()

    if not (target_code and base1_code and base2_code):
        mb.showwarning("Внимание", "Выберите все коды валют")
        return

    try:
        # Запрос курсов для первой базовой валюты
        response1 = requests.get(
            f'https://open.er-api.com/v6/latest/{base1_code}'
        )
        response1.raise_for_status()
        data1 = response1.json()

        # Запрос курсов для второй базовой валюты
        response2 = requests.get(
            f'https://open.er-api.com/v6/latest/{base2_code}'
        )
        response2.raise_for_status()
        data2 = response2.json()

        result_lines = []

        if target_code in data1['rates']:
            rate1 = data1['rates'][target_code]
            base1_name = currencies[base1_code]
            target_name = currencies[target_code]
            result_lines.append(
                f"1 {base1_name} = {rate1:.2f} {target_name}"
            )
        else:
            result_lines.append(
                f"Валюта {target_code} не найдена для {base1_code}"
            )

        if target_code in data2['rates']:
            rate2 = data2['rates'][target_code]
            base2_name = currencies[base2_code]
            target_name = currencies[target_code]
            result_lines.append(
                f"1 {base2_name} = {rate2:.2f} {target_name}"
            )
        else:
            result_lines.append(
                f"Валюта {target_code} не найдена для {base2_code}"
            )

        mb.showinfo("Курсы обмена", "\n".join(result_lines))

    except Exception as e:
        mb.showerror("Ошибка", f"Ошибка: {e}")

# Словарь кодов валют и их полных названий
currencies = {
    "USD": "Американский доллар",
    "EUR": "Евро",
    "JPY": "Японская йена",
    "GBP": "Британский фунт стерлингов",
    "AUD": "Австралийский доллар",
    "CAD": "Канадский доллар",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "RUB": "Российский рубль",
    "KZT": "Казахстанский тенге",
    "UZS": "Узбекский сум"
}

# Создание графического интерфейса
window = Tk()
window.title("Курс обмена валюты")
window.geometry("380x460")

# --- Первая базовая валюта ---
Label(text="Базовая валюта 1:").pack(padx=10, pady=5)
base1_combobox = ttk.Combobox(values=list(currencies.keys()))
base1_combobox.pack(padx=10, pady=5)
base1_combobox.bind("<<ComboboxSelected>>", update_b1_label)

b1_label = ttk.Label()
b1_label.pack(padx=10, pady=5)

# --- Вторая базовая валюта ---
Label(text="Базовая валюта 2:").pack(padx=10, pady=5)
base2_combobox = ttk.Combobox(values=list(currencies.keys()))
base2_combobox.pack(padx=10, pady=5)
base2_combobox.bind("<<ComboboxSelected>>", update_b2_label)

b2_label = ttk.Label()
b2_label.pack(padx=10, pady=5)

# --- Целевая валюта ---
Label(text="Целевая валюта:").pack(padx=10, pady=5)
target_combobox = ttk.Combobox(values=list(currencies.keys()))
target_combobox.pack(padx=10, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=5)

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=15)

window.mainloop()
