import random
import os

def task_1():
    a = [-1, 21, 992, 3, -85, 80, 123, 98, 112, 5, 66]
    b = [-1, -52, -63, 44, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    common_elements = list(set(a) & set(b))
    a.sort()
    b.sort()
    a = [x for x in a if x >= 0]
    b = [x for x in b if x >= 0]
    return common_elements, a, b

def task_2():
    s = input("Введите строку: ")
    if len(s) > 10:
        print("Предупреждение: строка длиннее 10 символов!")
    else:
        print(s.ljust(10, '*'))

def task_3():
    numbers = [float(input(f"Введите число {i + 1}: ")) for i in range(6)]
    min_num, max_num = numbers[0], numbers[0]
    for num in numbers[1:]:
        if num < min_num:
            min_num = num
        if num > max_num:
            max_num = num
    print(f"Минимальное: {round(min_num, 2)}, Максимальное: {round(max_num, 2)}")

def task_4():
    s = input("Введите строку: ").replace(" ", "").lower()
    print("Палиндром" if s == s[::-1] else "Не палиндром")

def task_5():
    even_number = random.randrange(6, 13, 2)
    multiple_of_five = random.randrange(5, 101, 5)
    print(f"Случайное четное число: {even_number}, число кратное 5: {multiple_of_five}")

def task_6():
    start = float(input("Введите начало диапазона: "))
    end = float(input("Введите конец диапазона: "))
    number_type = input("Введите 'int' для целого числа или 'float' для вещественного: ")
    if number_type == 'int':
        print(random.randint(int(start), int(end)))
    else:
        print(random.uniform(start, end))

def task_7():
    numbers = [random.uniform(0, 100) for _ in range(100)]
    def print_list(lst):
        for i in range(0, len(lst), 10):
            print(*lst[i:i+10])
    print_list(numbers)
    numbers.sort()
    print("\nОтсортированный список:")
    print_list(numbers)

def task_8():
    while True:
        a = input("Введите первое число: ")
        b = input("Введите второе число: ")
        if a.isdigit() and b.isdigit():
            print(f"Сумма: {int(a) + int(b)}")
            break
        else:
            print("Ошибка ввода, попробуйте снова.")

def task_9():
    numbers_map = {"one": "один", "two": "два", "three": "три", "four": "четыре", "five": "пять"}
    
    if not os.path.exists("data.txt"):
        print("Ошибка: Файл 'data.txt' не найден.")
        return

    with open("data.txt", "r") as infile, open("dataRu.txt", "w") as outfile:
        for line in infile:
            for eng, rus in numbers_map.items():
                line = line.replace(eng, rus)
            outfile.write(line)
    print("Файл 'dataRu.txt' успешно создан.")

def task_10():
    total = 0
    while True:
        num = int(input("Введите число (0 для завершения): "))
        if num == 0:
            break
        total += num
    print(f"Сумма: {total}")

# Вызовы функций для тестирования
if __name__ == "__main__":
    print("Task 1:", task_1())
    print("Task 2:")
    task_2()
    print("Task 3:")
    task_3()
    print("Task 4:")
    task_4()
    print("Task 5:")
    task_5()
    print("Task 6:")
    task_6()
    print("Task 7:")
    task_7()
    print("Task 8:")
    task_8()
    print("Task 9:")
    task_9()
    print("Task 10:")
    task_10()