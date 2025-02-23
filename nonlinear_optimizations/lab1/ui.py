from tkinter import *
from tkinter import ttk
import algorithms as alg

root = Tk()
root.title("lab1")
root.geometry("500x600")

epsilon = 0.1
l = 2,15

def solve():
    if alg_combobox.get() == 'Дихотомический поиск':
        print(alg.dichotomy_solver(int(left_entry.get()), int(right_entry.get()), epsilon, l, eval(f"lambda x: {function_entry.get()}")))  #a,b,epsilon,l,func
    elif alg_combobox.get() == 'Золотое сечение':
        print('whh')
    elif alg_combobox.get() == 'Метод Фибоначчи':
        print('huseeei')


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

min_max_label = Label(text='Что ищем')
min_max_label.place(x=20, y=80)
min_max = ['MIN', 'MAX']
min_max_combobox = ttk.Combobox(values = min_max)
min_max_combobox.place(x=100, y=80)

alg_options = ['Дихотомический поиск', 'Золотое сечение', 'Метод Фибоначчи']
alg_combobox = ttk.Combobox(values=alg_options)
alg_combobox.place(x=20, y=110)

solve_btn = Button(text='Решить', command=solve)
solve_btn.place(x=20, y=140)


root.mainloop()



