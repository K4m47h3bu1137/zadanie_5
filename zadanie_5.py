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
    base_code = base_combobox.get()

    if target_code and base_code:
        try:
            response = requests.get(f'https://open.er-api.com/v6/latest/{base_code}')
            response.raise_for_status()

            data = response.json()

            if target_code in data['rates']:
                exchange_rate = data['rates'][target_code]
                base = currencies[base_code]
                target = currencies[target_code]
                mb.showinfo("Курс обмена", f"Курс {exchange_rate:.1f} {target} за 1 {base}")
            else:
                mb.showerror("Ошибка", f"Валюта {target_code} не найдена")
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning("Внимание", "Выберите коды валют")

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
