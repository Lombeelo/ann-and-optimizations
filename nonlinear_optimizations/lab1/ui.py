from tkinter import *
from tkinter import ttk
import algorithms as alg
from math import cos, sin, pi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ast


def clear_table():
    for item in tree.get_children():
        tree.delete(item)


def solve():
    clear_table()
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
        if min_max_combobox.get() == 'MIN':
            solution = alg.dichotomy_solver(a, b, epsylon, l, eval(function_str))
        elif min_max_combobox.get() == 'MAX':
            solution = alg.dichotomy_solver(a, b, epsylon, l, eval(f"lambda x: -({function_entry.get()})"))
        dichotomy_calc = Label(frame_input, text=f'Кол-во расчетов ф-ции (Дихотомический поиск): {solution['f_calculated_counter']}')
        dichotomy_calc.pack()
        dichotomy_arg = Label(frame_input, text=f'Оптимальный аргумент (Дихотомический поиск): {(solution['a_end'] + solution['b_end'])/2}')
        dichotomy_arg.pack()
        dichotomy_f = Label(frame_input, text=f'Оптимальный аргумент (Дихотомический поиск): {(solution['f_a_end'] + solution['f_b_end'])/2}')
        dichotomy_f.pack()
    elif alg_combobox.get() == 'Золотое сечение':
        if min_max_combobox.get() == 'MIN':
            solution = alg.golden_ratio_solver(a, b, '-', l, eval(function_str))
        elif min_max_combobox.get() == 'MAX':
            solution = alg.golden_ratio_solver(a, b, '-', l, eval(f"lambda x: -({function_entry.get()})"))
        golden_calc = Label(frame_input, text=f'Кол-во расчетов ф-ции (Золотое сечение): {solution['f_calculated_counter']}')
        golden_calc.pack()
        golden_arg = Label(frame_input, text=f'Оптимальный аргумент (Золотое сечение): {(solution['a_end'] + solution['b_end'])/2}')
        golden_arg.pack()
        golden_f = Label(frame_input, text=f'Оптимальный аргумент (Золотое сечение): {(solution['f_a_end'] + solution['f_b_end'])/2}')
        golden_f.pack()
    elif alg_combobox.get() == 'Метод Фибоначчи':
        if min_max_combobox.get() == 'MIN':
            solution = alg.fibonacchi_solver(a, b, epsylon, l, eval(function_str))
        elif min_max_combobox.get() == 'MAX':
            solution = alg.fibonacchi_solver(a, b, epsylon, l, eval(f"lambda x: -({function_entry.get()})"))
        golden_calc = Label(frame_input, text=f'Кол-во расчетов ф-ции (Метод Фибоначчи): {solution['f_calculated_counter']}')
        golden_calc.pack()
        golden_arg = Label(frame_input, text=f'Оптимальный аргумент (Метод Фибоначчи): {(solution['a_end'] + solution['b_end'])/2}')
        golden_arg.pack()
        golden_f = Label(frame_input, text=f'Оптимальный аргумент (Метод Фибоначчи): {(solution['f_a_end'] + solution['f_b_end'])/2}')
        golden_f.pack()

    # Предполагаем, что solution["solution_log"] содержит данные каждой итерации
    for step in solution["solution_log"]:
        tree.insert("", "end", values=(step['solver_type'], step['k'], step['a'], step['b'], step['lam'], step['mu'], step['f_lam'], step['f_mu']))


    # plot_function(eval(function_str), a, b)




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
   
    # plot_function(eval(function_str), a, b)





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
    # Очищаем текущую фигуру
    plt.clf()
    
    # Создаем массив значений x
    x = np.linspace(a, b, 100)
    # Вычисляем значения функции
    y = func(x)

    # Отрисовываем график
    plt.plot(x, y, label='Функция')
    
    # Добавляем метки на оси
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('График функции')

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
    k = int(values[0])
    a = float(values[1])
    b = float(values[2])
    lam = float(values[3])
    mu = float(values[4])

    # Обновляем график с новыми значениями
    function_str = f"lambda x: {function_entry.get()}"
    plot_function(eval(function_str), a, b, lam, mu)

# Обновляем график с новыми значениями
tree.bind("<<TreeviewSelect>>", on_table_select)

root.mainloop()

