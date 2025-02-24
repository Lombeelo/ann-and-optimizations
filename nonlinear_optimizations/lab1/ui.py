from tkinter import *
from tkinter import ttk
import algorithms as alg
from math import cos, sin, pi


root = Tk()
root.title("lab1")
root.geometry("500x600")


def solve():
    if alg_combobox.get() == 'Дихотомический поиск':
        if min_max_combobox.get() == 'MIN':
            print(alg.dichotomy_solver(eval(left_entry.get()), eval(right_entry.get()), eval(epsylon_entry.get()), eval(l_entry.get()), eval(f"lambda x: {function_entry.get()}")))  #a,b,epsilon,l,func
        elif min_max_combobox.get() == 'MAX':
            print(alg.dichotomy_solver(eval(left_entry.get()), eval(right_entry.get()), eval(epsylon_entry.get()), eval(l_entry.get()), eval(f"lambda x: -({function_entry.get()})")))  #a,b,epsilon,l,func
    elif alg_combobox.get() == 'Золотое сечение':
        if min_max_combobox.get() == 'MIN':
            print(alg.golden_ratio_solver(eval(left_entry.get()), eval(right_entry.get()), '-', eval(l_entry.get()), eval(f"lambda x: {function_entry.get()}")))  #a,b,l,func
        elif min_max_combobox.get() == 'MAX':
            print(alg.golden_ratio_solver(eval(left_entry.get()), eval(right_entry.get()), '-', eval(l_entry.get()), eval(f"lambda x: -({function_entry.get()})")))  #a,b,l,func
    elif alg_combobox.get() == 'Метод Фибоначчи':
        if min_max_combobox.get() == 'MIN':
            print(alg.fibonacchi_solver(eval(left_entry.get()), eval(right_entry.get()), eval(epsylon_entry.get()), eval(l_entry.get()), eval(f"lambda x: {function_entry.get()}")))  #a,b,epsilon,l,func
        elif min_max_combobox.get() == 'MAX':
            print(alg.fibonacchi_solver(eval(left_entry.get()), eval(right_entry.get()), eval(epsylon_entry.get()), eval(l_entry.get()), eval(f"lambda x: -({function_entry.get()})")))  #a,b,epsilon,l,func


def solve_all():
    solvers = [alg.dichotomy_solver, alg.golden_ratio_solver, alg.fibonacchi_solver]
    for solver in solvers:
        if solver == alg.golden_ratio_solver:
            if min_max_combobox.get() == 'MIN':
                solution = solver(eval(left_entry.get()), eval(right_entry.get()), '-', eval(l_entry.get()), eval(f"lambda x: {function_entry.get()}"))
            elif min_max_combobox.get() == 'MAX':
                solution = solver(eval(left_entry.get()), eval(right_entry.get()), '-', eval(l_entry.get()), eval(f"lambda x: -({function_entry.get()})"))
        else:
            if min_max_combobox.get() == 'MIN':
                solution = solver(eval(left_entry.get()), eval(right_entry.get()), eval(epsylon_entry.get()), eval(l_entry.get()), eval(f"lambda x: {function_entry.get()}"))
            elif min_max_combobox.get() == 'MAX':
                solution = solver(eval(left_entry.get()), eval(right_entry.get()), eval(epsylon_entry.get()), eval(l_entry.get()), eval(f"lambda x: -({function_entry.get()})"))
        for step in solution["solution_log"]:
            print(step)


function_label = Label(text='Введите функцию')
function_label.place(x=20, y=20)
function_entry = Entry()
function_entry.place(x=150, y=20)

left_label = Label(text='[')
left_label.place(x=20, y=50)
left_entry = Entry()
left_entry.place(x=30, y=50)
devide_label = Label(text=';')
devide_label.place(x=150, y=50)
right_entry = Entry()
right_entry.place(x=160, y=50)
right_label = Label(text=']')
right_label.place(x=280, y=50)

epsylon_label = Label(text='Константа различимости')
epsylon_label.place(x=20, y=80)
epsylon_entry = Entry()
epsylon_entry.place(x=180, y=80)

l_label = Label(text='Допустимая конечная длина l')
l_label.place(x=20, y=110)
l_entry = Entry()
l_entry.place(x=200, y=110)

min_max_label = Label(text='Что ищем')
min_max_label.place(x=20, y=140)
min_max = ['MIN', 'MAX']
min_max_combobox = ttk.Combobox(values = min_max)
min_max_combobox.place(x=100, y=140)

alg_options = ['Дихотомический поиск', 'Золотое сечение', 'Метод Фибоначчи']
alg_combobox = ttk.Combobox(values=alg_options)
alg_combobox.place(x=20, y=170)

solve_btn = Button(text='Решить', command=solve)
solve_btn.place(x=20, y=200)

solve_all_btn = Button(text='Решить всеми методами', command=solve_all)
solve_all_btn.place(x=20, y=230)



root.mainloop() # сделать графики


