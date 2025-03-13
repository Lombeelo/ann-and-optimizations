from tkinter import *
from tkinter import ttk
import algorithms as alg
from math import cos, sin, pi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ast

# Список для хранения виджетов с результатами
result_labels = []
tables = []

def clear_results():
    """Удаляет старые результаты перед обновлением новых значений."""
    global result_labels
    for label in result_labels:
        label.destroy()
    result_labels.clear()

def clear_tables():
    """Удаляет старые таблицы перед обновлением новых значений."""
    global tables
    for table in tables:
        table.destroy()
    tables.clear()

def solve():
    """Решает задачу выбранным методом и обновляет таблицу и результаты."""
    clear_tables()
    clear_results()

    function_str = f"lambda x: {function_entry.get()}"
    try:
        a = round(ast.literal_eval(left_entry.get()), 4)
        b = round(ast.literal_eval(right_entry.get()), 4)
        epsylon = round(ast.literal_eval(epsylon_entry.get()), 4)
        l = round(ast.literal_eval(l_entry.get()), 4)
    except (ValueError, SyntaxError):
        print("Ошибка ввода. Проверьте значения.")
        return

    method_name = alg_combobox.get()
    if method_name == 'Дихотомический поиск':
        solver = alg.dichotomy_solver
    elif method_name == 'Золотое сечение':
        solver = alg.golden_ratio_solver
    elif method_name == 'Метод Фибоначчи':
        solver = alg.fibonacchi_solver
    else:
        return

    function_eval = eval(function_str)
    if min_max_combobox.get() == 'MAX':
        function_eval = eval(f"lambda x: -({function_entry.get()})")

    if solver == alg.golden_ratio_solver:
        solution = solver(a, b, '-', l, function_eval)
    else:
        solution = solver(a, b, epsylon, l, function_eval)

    # Вывод результатов
    result_labels.append(Label(frame_input, text=f'Кол-во расчетов ф-ции ({method_name}): {solution["f_calculated_counter"]}'))
    result_labels.append(Label(frame_input, text=f'Оптимальный аргумент ({method_name}): {round((solution["a_end"] + solution["b_end"]) / 2, 4)}'))
    opt_value = round(solution["f_opt"], 4) if min_max_combobox.get() == 'MIN' else round(-solution["f_opt"], 4)
    result_labels.append(Label(frame_input, text=f'Оптимальное значение функции ({method_name}): {opt_value}'))

    for label in result_labels:
        label.pack()

    # Создание таблицы
    create_method_table(method_name, solution["solution_log"])
    
    plot_function(eval(function_str), a, b)


def solve_all():
    """Решает задачу всеми методами и создает отдельные таблицы для каждого метода."""
    clear_tables()
    clear_results()

    function_str = f"lambda x: {function_entry.get()}"
    try:
        a = round(ast.literal_eval(left_entry.get()), 4)
        b = round(ast.literal_eval(right_entry.get()), 4)
        epsylon = round(ast.literal_eval(epsylon_entry.get()), 4)
        l = round(ast.literal_eval(l_entry.get()), 4)
    except (ValueError, SyntaxError):
        print("Ошибка ввода. Проверьте значения.")
        return

    solvers = {
        'Дихотомический поиск': alg.dichotomy_solver,
        'Золотое сечение': alg.golden_ratio_solver,
        'Метод Фибоначчи': alg.fibonacchi_solver
    }

    function_eval = eval(function_str)
    if min_max_combobox.get() == 'MAX':
        function_eval = eval(f"lambda x: -({function_entry.get()})")

    for method_name, solver in solvers.items():
        if solver == alg.golden_ratio_solver:
            solution = solver(a, b, '-', l, function_eval)
        else:
            solution = solver(a, b, epsylon, l, function_eval)

        # Вывод результатов
        result_labels.append(Label(frame_input, text=f'Кол-во расчетов ф-ции ({method_name}): {solution["f_calculated_counter"]}'))
        result_labels.append(Label(frame_input, text=f'Оптимальный аргумент ({method_name}): {round((solution["a_end"] + solution["b_end"]) / 2, 4)}'))
        opt_value = round(solution["f_opt"], 4) if min_max_combobox.get() == 'MIN' else round(-solution["f_opt"], 4)
        result_labels.append(Label(frame_input, text=f'Оптимальное значение функции ({method_name}): {opt_value}'))

        for label in result_labels:
            label.pack()

        # Создание таблицы
        create_method_table(method_name, solution["solution_log"])

    plot_function(eval(function_str), a, b)

def create_method_table(method_name, solution_log):
    """Создает отдельную таблицу для каждого метода."""
    method_frame = Frame(root)
    method_frame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
    tables.append(method_frame)

    method_label = Label(method_frame, text=method_name, font=("Arial", 12, "bold"))
    method_label.pack()

    columns = ['k', 'a', 'b', 'lam', 'mu', 'f_lam', 'f_mu']
    tree = ttk.Treeview(method_frame, columns=columns, show='headings', style="Custom.Treeview")
    tree.pack(fill=BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center", width=100)

    for step in solution_log:
        tree.insert("", "end", values=(
            step['k'], round(step['a'], 4), round(step['b'], 4), round(step['lam'], 4),
            round(step['mu'], 4), round(step['f_lam'], 4), round(step['f_mu'], 4)
        ))



# Стилизация таблиц
style = ttk.Style()
style.configure("Custom.Treeview", rowheight=25)
style.configure("Custom.Treeview.Heading", font=("Arial", 10, "bold"))

# Запуск GUI

root = Tk()
root.title("lab1")
root.geometry("900x600")

# Создание фрейма для ввода данных и кнопок
frame_input = Frame(root)
frame_input.pack(side=LEFT, fill=Y, padx=10, pady=10)

# UI элементы
function_label = Label(frame_input, text='Введите функцию:')
function_label.pack()

function_entry = Entry(frame_input)
function_entry.pack()

left_label = Label(frame_input, text='Левый предел:')
left_label.pack()

left_entry = Entry(frame_input)
left_entry.pack()

right_label = Label(frame_input, text='Правый предел:')
right_label.pack()

right_entry = Entry(frame_input)
right_entry.pack()

epsylon_label = Label(frame_input, text='Эпсилон:')
epsylon_label.pack()

epsylon_entry = Entry(frame_input)
epsylon_entry.pack()

l_label = Label(frame_input, text='Минимально допустимый промежуток (l):')
l_label.pack()

l_entry = Entry(frame_input)
l_entry.pack()

alg_label = Label(frame_input, text='Выберите алгоритм:')
alg_label.pack()

alg_combobox = ttk.Combobox(frame_input, values=['Дихотомический поиск', 'Золотое сечение', 'Метод Фибоначчи'])
alg_combobox.pack()

min_max_label = Label(frame_input, text='Минимум или максимум:')
min_max_label.pack()

min_max_combobox = ttk.Combobox(frame_input, values=['MIN', 'MAX'])
min_max_combobox.pack()

solve_button = Button(frame_input, text='Решить', command=solve)
solve_button.pack(pady=5)

solve_all_button = Button(frame_input, text='Решить все', command=solve_all)
solve_all_button.pack(pady=5)

# Создание фрейма для таблицы
frame_table = Frame(root)
frame_table.pack(side=TOP, fill=BOTH, expand=True)

# Создание таблицы
columns = ['k', 'a', 'b', 'lam', 'mu', 'f_lam', 'f_mu']
tree = ttk.Treeview(frame_table, columns=columns, show='headings')
tree.pack(side=LEFT, fill=BOTH, expand=True)

# Добавление заголовков
for col in columns:
    tree.heading(col, text=col)

# Добавление прокрутки для таблицы
scrollbar = Scrollbar(frame_table, orient="vertical", command=tree.yview)
scrollbar.pack(side=RIGHT, fill=Y)
tree.configure(yscroll=scrollbar.set)

# Обновленная функция для отрисовки графика
def plot_function(func, a, b, lam=None, mu=None):
    plt.clf()
    
    x = np.linspace(a, b, 100)
    y = func(x)

    plt.plot(x, y, label='Функция')

    # Добавляем точки A и B
    plt.scatter([a, b], [func(a), func(b)], color='blue', label='A и B', zorder=3)

    # # Подсветка выбранного отрезка
    # if lam is not None and mu is not None:
    #     plt.plot([lam, mu], [func(lam), func(mu)], color='purple', linewidth=3, label='Выбранный отрезок')

    # Добавляет отображение осей
    ax = plt.gca()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('График функции')
    plt.legend()
    plt.grid() # Добавление сетки
    plt.draw()
    plt.pause(0.001)

    # Отображаем точки lam и mu, если они есть
    if lam is not None and mu is not None:
        plt.plot([lam], [func(lam)], 'ro', label='lam', markersize=8)
        plt.plot([mu], [func(mu)], 'go', label='mu', markersize=8)

    # Добавляем легенду
    plt.legend()

    # Обновляем график
    plt.draw()
    plt.pause(0.001)  # Позволяет обновить график

# Функция для обработки выбора в таблице
def on_table_select(event):
    selected_item = tree.selection()[0]  # Получаем выбранный элемент
    values = tree.item(selected_item, 'values')  # Получаем значения выбранного элемента

    # Извлекаем необходимые значения из таблицы
    k = int(values[1])
    a = float(values[2])
    b = float(values[3])
    lam = float(values[4])
    mu = float(values[5])

    # Обновляем график с новыми значениями
    function_str = f"lambda x: {function_entry.get()}"
    plot_function(eval(function_str), a, b, lam, mu)

# Обновляем график с новыми значениями
tree.bind("<<TreeviewSelect>>", on_table_select)

root.mainloop()

# Нынешний мой код выглядит так и в нем есть проблемы:
# Отрисовывается одна лишняя таблица в начале независимо от того какая нажата кнопка: Решить все или Решить. Также при клике на строку из любого метода - обновление графика и отрисовка не происходит. При старте программы появляется пустое лишнее окно. и все также нет у таблицы границ выделяемых визуальной линией столбцы и строки.
