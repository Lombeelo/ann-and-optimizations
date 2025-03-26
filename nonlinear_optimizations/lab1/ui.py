import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QScrollArea, QHeaderView
)
from PyQt5.QtCore import Qt
import algorithms as alg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import ast


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab1 - Nonlinear Optimization")
        self.setGeometry(100, 100, 1200, 800)

        # Основной виджет и layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Левая панель для ввода данных
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.layout.addWidget(self.left_panel, stretch=1)

        # Правая панель для таблиц и графика
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.layout.addWidget(self.right_panel, stretch=3)

        # Элементы ввода (сжатые поля)
        self.function_label = QLabel("Введите функцию:")
        self.function_entry = QLineEdit()
        self.left_layout.addWidget(self.function_label)
        self.left_layout.addWidget(self.function_entry)

        self.left_limit_label = QLabel("Левый предел:")
        self.left_entry = QLineEdit()
        self.left_layout.addWidget(self.left_limit_label)
        self.left_layout.addWidget(self.left_entry)

        self.right_limit_label = QLabel("Правый предел:")
        self.right_entry = QLineEdit()
        self.left_layout.addWidget(self.right_limit_label)
        self.left_layout.addWidget(self.right_entry)

        self.epsilon_label = QLabel("Эпсилон:")
        self.epsilon_entry = QLineEdit()
        self.left_layout.addWidget(self.epsilon_label)
        self.left_layout.addWidget(self.epsilon_entry)

        self.l_label = QLabel("Минимально допустимый промежуток (l):")
        self.l_entry = QLineEdit()
        self.left_layout.addWidget(self.l_label)
        self.left_layout.addWidget(self.l_entry)

        self.algorithm_label = QLabel("Выберите алгоритм:")
        self.algorithm_combobox = QComboBox()
        self.algorithm_combobox.addItems(["Дихотомический поиск", "Золотое сечение", "Метод Фибоначчи"])
        self.left_layout.addWidget(self.algorithm_label)
        self.left_layout.addWidget(self.algorithm_combobox)

        self.min_max_label = QLabel("Минимум или максимум:")
        self.min_max_combobox = QComboBox()
        self.min_max_combobox.addItems(["MIN", "MAX"])
        self.left_layout.addWidget(self.min_max_label)
        self.left_layout.addWidget(self.min_max_combobox)

        self.solve_button = QPushButton("Решить")
        self.solve_button.clicked.connect(self.solve)
        self.left_layout.addWidget(self.solve_button)

        self.solve_all_button = QPushButton("Решить все")
        self.solve_all_button.clicked.connect(self.solve_all)
        self.left_layout.addWidget(self.solve_all_button)

        self.export_button = QPushButton("Экспорт в CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        self.left_layout.addWidget(self.export_button)

        # Виджет для вывода результатов
        self.results_label = QLabel()
        self.left_layout.addWidget(self.results_label)

        # Таблицы и график
        self.tables = []
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)  # Добавляем панель инструментов
        self.right_layout.addWidget(self.toolbar)
        self.right_layout.addWidget(self.canvas)

        # Прокрутка для таблиц
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.right_layout.addWidget(self.scroll_area)

        # Значения по нашему заданию из лабораторной работы
        self.set_default_values()
    
    def set_default_values(self):
        """Устанавливает значения по умолчанию"""
        self.function_entry.setText("3/x**3")
        self.left_entry.setText("-3")
        self.right_entry.setText("0")
        self.epsilon_entry.setText("0.001")
        self.l_entry.setText("0.1")
        self.algorithm_combobox.setCurrentText("Дихотомический поиск")
        self.min_max_combobox.setCurrentText("MIN")

    def solve(self):
        """Решает задачу выбранным методом и обновляет таблицу и график."""
        self.clear_tables()

        function_str = f"lambda x: {self.function_entry.text()}"
        try:
            a = round(ast.literal_eval(self.left_entry.text()), 4)
            b = round(ast.literal_eval(self.right_entry.text()), 4)
            epsylon = round(ast.literal_eval(self.epsilon_entry.text()), 4)
            l = round(ast.literal_eval(self.l_entry.text()), 4)
        except (ValueError, SyntaxError):
            print("Ошибка ввода. Проверьте значения.")
            return

        method_name = self.algorithm_combobox.currentText()
        if method_name == 'Дихотомический поиск':
            solver = alg.dichotomy_solver
        elif method_name == 'Золотое сечение':
            solver = alg.golden_ratio_solver
        elif method_name == 'Метод Фибоначчи':
            solver = alg.fibonacchi_solver
        else:
            return

        function_eval = eval(function_str)
        if self.min_max_combobox.currentText() == 'MAX':
            function_eval = eval(f"lambda x: -({self.function_entry.text()})")

        if solver == alg.golden_ratio_solver:
            solution = solver(a, b, '-', l, function_eval)
        else:
            solution = solver(a, b, epsylon, l, function_eval)

        # Вывод результатов
        self.results_label.setText(
            f'Кол-во расчетов ф-ции ({method_name}): {solution["f_calculated_counter"]}\n'
            f'Оптимальный аргумент ({method_name}): {round((solution["a_end"] + solution["b_end"]) / 2, 4)}\n'
            f'Оптимальное значение функции ({method_name}): {round(solution["f_opt"], 4) if self.min_max_combobox.currentText() == "MIN" else round(-solution["f_opt"], 4)}'
        )

        # Создание таблицы
        self.create_method_table(method_name, solution["solution_log"])

        # Отрисовка графика
        self.plot_function(eval(function_str), a, b)

    def solve_all(self):
        """Решает задачу всеми методами и создает отдельные таблицы для каждого метода."""
        self.clear_tables()

        function_str = f"lambda x: {self.function_entry.text()}"
        try:
            a = round(ast.literal_eval(self.left_entry.text()), 4)
            b = round(ast.literal_eval(self.right_entry.text()), 4)
            epsylon = round(ast.literal_eval(self.epsilon_entry.text()), 4)
            l = round(ast.literal_eval(self.l_entry.text()), 4)
        except (ValueError, SyntaxError):
            print("Ошибка ввода. Проверьте значения.")
            return

        solvers = {
            'Дихотомический поиск': alg.dichotomy_solver,
            'Золотое сечение': alg.golden_ratio_solver,
            'Метод Фибоначчи': alg.fibonacchi_solver
        }

        function_eval = eval(function_str)
        if self.min_max_combobox.currentText() == 'MAX':
            function_eval = eval(f"lambda x: -({self.function_entry.text()})")

        results_text = ""
        for method_name, solver in solvers.items():
            if solver == alg.golden_ratio_solver:
                solution = solver(a, b, '-', l, function_eval)
            else:
                solution = solver(a, b, epsylon, l, function_eval)

            # Вывод результатов
            results_text += (
                f'Кол-во расчетов ф-ции ({method_name}): {solution["f_calculated_counter"]}\n'
                f'Оптимальный аргумент ({method_name}): {round((solution["a_end"] + solution["b_end"]) / 2, 4)}\n'
                f'Оптимальное значение функции ({method_name}): {round(solution["f_opt"], 4) if self.min_max_combobox.currentText() == "MIN" else round(-solution["f_opt"], 4)}\n\n'
            )

            # Создание таблицы
            self.create_method_table(method_name, solution["solution_log"])

        # Вывод всех результатов
        self.results_label.setText(results_text)

        # Отрисовка графика
        self.plot_function(eval(function_str), a, b)

    def create_method_table(self, method_name, solution_log):
        """Создает таблицу для метода."""
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(['k', 'a', 'b', 'lam', 'mu', 'f_lam', 'f_mu'])
        table.setRowCount(len(solution_log))

        # Убираем первый столбец с номерами строк
        table.verticalHeader().setVisible(False)

        # Центрирование текста в ячейках
        for i in range(table.rowCount()):
            for j in range(table.columnCount()):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j, item)

        for i, step in enumerate(solution_log):
            table.setItem(i, 0, QTableWidgetItem(str(step['k'])))
            table.setItem(i, 1, QTableWidgetItem(str(round(step['a'], 4))))
            table.setItem(i, 2, QTableWidgetItem(str(round(step['b'], 4))))
            table.setItem(i, 3, QTableWidgetItem(str(round(step['lam'], 4))))
            table.setItem(i, 4, QTableWidgetItem(str(round(step['mu'], 4))))
            table.setItem(i, 5, QTableWidgetItem(str(round(step['f_lam'], 4))))
            table.setItem(i, 6, QTableWidgetItem(str(round(step['f_mu'], 4))))

        # Жирный шрифт для заголовков столбцов
        table.setStyleSheet("QHeaderView::section { font-weight: bold; }")

        # Устанавливаем ширину столбцов
        table.setColumnWidth(0, 80)  # Ширина столбца 'k'
        table.setColumnWidth(1, 120)  # Ширина столбца 'a'
        table.setColumnWidth(2, 120)  # Ширина столбца 'b'
        table.setColumnWidth(3, 120)  # Ширина столбца 'lam'
        table.setColumnWidth(4, 120)  # Ширина столбца 'mu'
        table.setColumnWidth(5, 120)  # Ширина столбца 'f_lam'
        table.setColumnWidth(6, 120)  # Ширина столбца 'f_mu'

        # Включаем возможность изменения ширины столбцов
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        # Заголовок таблицы (название метода)
        header = QLabel(method_name)
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        header.setAlignment(Qt.AlignLeft)  # Выравнивание влево
        self.scroll_layout.addWidget(header)
        self.scroll_layout.addWidget(table)
        self.tables.append((header, table))

        # Обработка кликов по таблице
        table.itemClicked.connect(lambda item, table=table: self.on_table_click(table))

    def on_table_click(self, table):
        """Обрабатывает клик по таблице."""
        selected_row = table.currentRow()
        if selected_row >= 0:
            a = float(table.item(selected_row, 1).text())
            b = float(table.item(selected_row, 2).text())
            lam = float(table.item(selected_row, 3).text())
            mu = float(table.item(selected_row, 4).text())

            # Обновляем график
            function_str = f"lambda x: {self.function_entry.text()}"
            self.plot_function(eval(function_str), a, b, lam, mu)

    def plot_function(self, func, a, b, lam=None, mu=None):
        """Отрисовывает график функции."""
        self.ax.clear()
        x = np.linspace(a, b, 100)
        y = func(x)

        self.ax.plot(x, y, label='Функция')
        self.ax.scatter([a, b], [func(a), func(b)], color='blue', label='A и B', zorder=3)

        if lam is not None and mu is not None:
            self.ax.plot([lam], [func(lam)], 'ro', label='lam', markersize=8)
            self.ax.plot([mu], [func(mu)], 'go', label='mu', markersize=8)

        self.ax.axhline(y=0, color='k')
        self.ax.axvline(x=0, color='k')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.set_title('График функции')
        self.ax.legend()
        self.ax.grid()
        self.canvas.draw()

    def clear_tables(self):
        """Очищает таблицы."""
        for header, table in self.tables:
            header.setParent(None)
            table.setParent(None)
        self.tables.clear()

    def export_to_csv(self):
        """Экспортирует данные таблицы в CSV."""
        if not self.tables:
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить CSV", "", "CSV Files (*.csv)")
        if file_name:
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for header, table in self.tables:
                    # Записываем заголовок метода
                    writer.writerow([header.text()])
                    # Записываем заголовки столбцов
                    writer.writerow([table.horizontalHeaderItem(i).text() for i in range(table.columnCount())])
                    # Записываем данные
                    for row in range(table.rowCount()):
                        writer.writerow([table.item(row, col).text() for col in range(table.columnCount())])
                    writer.writerow([])  # Пустая строка между таблицами


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())