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

def clear_results():
    """Удаляет старые результаты перед обновлением новых значений."""
    global result_labels
    for label in result_labels:
        label.destroy()
    result_labels.clear()

def clear_table():
    for item in tree.get_children():
        tree.delete(item)


def clear_results():
    """Удаляет старые результаты перед обновлением новых значений."""
    global result_labels
    for label in result_labels:
        label.destroy()
    result_labels.clear()

def solve():
    clear_table()
    clear_results()  # Очищаем старые результаты

    function_str = f"lambda x: {function_entry.get()}"
    try:
        a = ast.literal_eval(left_entry.get())
        b = ast.literal_eval(right_entry.get())
        epsylon = ast.literal_eval(epsylon_entry.get())
        l = ast.literal_eval(l_entry.get())
    except (ValueError, SyntaxError):
        print("Ошибка ввода. Пожалуйста, проверьте значения.")
        return

    if alg_combobox.get() == 'Дихотомический поиск':
        solution = alg.dichotomy_solver(a, b, epsylon, l, eval(function_str)) if min_max_combobox.get() == 'MIN' else alg.dichotomy_solver(a, b, epsylon, l, eval(f"lambda x: -({function_entry.get()})"))
        method_name = "Дихотомический поиск"
    elif alg_combobox.get() == 'Золотое сечение':
        solution = alg.golden_ratio_solver(a, b, '-', l, eval(function_str)) if min_max_combobox.get() == 'MIN' else alg.golden_ratio_solver(a, b, '-', l, eval(f"lambda x: -({function_entry.get()})"))
        method_name = "Золотое сечение"
    elif alg_combobox.get() == 'Метод Фибоначчи':
        solution = alg.fibonacchi_solver(a, b, epsylon, l, eval(function_str)) if min_max_combobox.get() == 'MIN' else alg.fibonacchi_solver(a, b, epsylon, l, eval(f"lambda x: -({function_entry.get()})"))
        method_name = "Метод Фибоначчи"
    else:
        return

    # Добавляем результаты
    result_labels.append(Label(frame_input, text=f'Кол-во расчетов ф-ции ({method_name}): {solution["f_calculated_counter"]}'))
    result_labels.append(Label(frame_input, text=f'Оптимальный аргумент ({method_name}): {(solution["a_end"] + solution["b_end"]) / 2}'))
    result_labels.append(Label(frame_input, text=f'Оптимальное значение функции ({method_name}): {-(solution["f_opt"])}'))

    for label in result_labels:
        label.pack()

    # Заполняем таблицу
    for step in solution["solution_log"]:
        f_lam = f"{step['f_lam']} ★" if step.get('f_calculated', False) else step['f_lam']
        f_mu = f"{step['f_mu']} ★" if step.get('f_calculated', False) else step['f_mu']

        tree.insert("", "end", values=(step['solver_type'], step['k'], step['a'], step['b'], step['lam'], step['mu'], f_lam, f_mu))
        
    plot_function(eval(function_str), a, b)

def solve_all():

    clear_table()

    function_str = f"lambda x: {function_entry.get()}"
    all_solved = [] #для хранения информации обо всех алгоритмах, а не только о последнем
    try:
        a = ast.literal_eval(left_entry.get())
        b = ast.literal_eval(right_entry.get())
        epsylon = ast.literal_eval(epsylon_entry.get())
        l = ast.literal_eval(l_entry.get())                             
    except (ValueError, SyntaxError):
        print("Ошибка ввода. Пожалуйста, проверьте значения.")
        return

    solvers = [alg.dichotomy_solver, alg.golden_ratio_solver, alg.fibonacchi_solver]
    for solver in solvers:
        if solver == alg.golden_ratio_solver:
            if min_max_combobox.get() == 'MIN':
                solution = solver(a, b, '-', l, eval(function_str))
                all_solved.append(solution)
            elif min_max_combobox.get() == 'MAX':
                solution = solver(a, b, '-', l, eval(f"lambda x: -({function_entry.get()})"))
                all_solved.append(solution)
        else:
            if min_max_combobox.get() == 'MIN':
                solution = solver(a, b, epsylon, l, eval(function_str))
                all_solved.append(solution)
            elif min_max_combobox.get() == 'MAX':
                solution = solver(a, b, epsylon, l, eval(f"lambda x: -({function_entry.get()})"))
                all_solved.append(solution)

        for step in solution["solution_log"]:
            tree.insert("", "end", values=(step['solver_type'], step['k'], step['a'], step['b'], step['lam'], step['mu'], step['f_lam'], step['f_mu']))

    print(all_solved)
   
    plot_function(eval(function_str), a, b)

# Запуск GUI

root = Tk()
root.title("lab1")
root.geometry("800x600")

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
columns = ['Метод', 'k', 'a', 'b', 'lam', 'mu', 'f_lam', 'f_mu']
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

    # Подсветка выбранного отрезка
    if lam is not None and mu is not None:
        plt.plot([lam, mu], [func(lam), func(mu)], color='purple', linewidth=3, label='Выбранный отрезок')

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('График функции')
    plt.legend()
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