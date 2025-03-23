import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from algorithm_multidimensional import rosenbrock_discrete
import math
from matplotlib.patches import Rectangle  # Импортируем Rectangle для закрашивания области

class OptimizationUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_rectangle = None  # Текущий прямоугольник на графике

    def initUI(self):
        self.setWindowTitle('Optimization Algorithm UI')

        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Input fields
        self.function_input = QLineEdit(self)
        self.extremum_type = QComboBox(self)
        self.extremum_type.addItems(['Минимум', 'Максимум'])
        self.start_point_input = QLineEdit(self)
        self.epsilon_input = QLineEdit(self)
        self.alpha_input = QLineEdit(self)
        self.beta_input = QLineEdit(self)
        self.delta_input = QLineEdit(self)

        # Заполним поля тестовыми данными для удобства тестирования
        self.function_input.setText("(x[0] - 2)**4 + (x[0] - 2*x[1])**2")
        self.start_point_input.setText("[0, 3]")
        self.epsilon_input.setText("0.1")
        self.alpha_input.setText("2")
        self.beta_input.setText("-0.5")
        self.delta_input.setText("[0.1, 0.1]")

        # Labels
        input_layout.addWidget(QLabel('Функция:'))
        input_layout.addWidget(self.function_input)
        input_layout.addWidget(QLabel('Тип экстремума:'))
        input_layout.addWidget(self.extremum_type)
        input_layout.addWidget(QLabel('Начальная точка:'))
        input_layout.addWidget(self.start_point_input)
        input_layout.addWidget(QLabel('Эпсилон:'))
        input_layout.addWidget(self.epsilon_input)
        input_layout.addWidget(QLabel('Альфа:'))
        input_layout.addWidget(self.alpha_input)
        input_layout.addWidget(QLabel('Бета:'))
        input_layout.addWidget(self.beta_input)
        input_layout.addWidget(QLabel('Дельты:'))
        input_layout.addWidget(self.delta_input)

        # Button
        self.run_button = QPushButton('Запуск', self)
        self.run_button.clicked.connect(self.run_optimization)
        button_layout.addWidget(self.run_button)

        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['K', 'Xk F(Xk)', 'j', 'yj F(yj)', 'Δj', 'dj', 'yj+Δdj F(yj+Δdj)'])
        self.table.verticalHeader().setVisible(False)  # Убираем нумерацию строк
        self.table.cellClicked.connect(self.highlight_area)  # Обработчик клика по строке

        # Plot
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Добавляем панель инструментов для графика (масштабирование, перемещение и т.д.)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Text area for results
        self.results_text = QTextEdit(self)
        self.results_text.setReadOnly(True)

        # Add to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.toolbar)  # Добавляем панель инструментов
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(self.results_text)

        self.setLayout(main_layout)

    def run_optimization(self):
        try:
            # Получаем данные из UI
            func_str = self.function_input.text()
            func = lambda x: eval(func_str, {'x': x, 'math': math})
            start_point = eval(self.start_point_input.text())
            epsylon = float(self.epsilon_input.text())
            alpha = float(self.alpha_input.text())
            beta = float(self.beta_input.text())
            delta_starting = eval(self.delta_input.text())

            # Запуск алгоритма
            log = rosenbrock_discrete(func, start_point, epsylon, alpha, beta, delta_starting)

            # Заполнение таблицы
            self.table.setRowCount(len(log))
            prev_k = None
            prev_xk = None
            start_row = 0

            for i, entry in enumerate(log):
                k = entry['k']
                xk = f"[{np.round(entry['xk'][0], 4)}, {np.round(entry['xk'][1], 4)}] {np.round(entry['fxk'], 4)}"
                j = entry['j']
                yj = f"[{np.round(entry['yj'][0], 4)}, {np.round(entry['yj'][1], 4)}] {np.round(entry['fyj'], 4)}"
                deltaj = np.round(entry['deltaj'], 4)
                dj = np.round(entry['dj'], 4)
                yj_next = f"[{np.round(entry['yj_next'][0], 4)}, {np.round(entry['yj_next'][1], 4)}] {np.round(entry['fyj_next'], 4)}"

                # Объединение ячеек для столбцов K и Xk F(Xk)
                if k == prev_k:
                    self.table.setItem(i, 0, QTableWidgetItem(""))
                    self.table.setItem(i, 1, QTableWidgetItem(""))
                else:
                    if prev_k is not None:
                        self.table.setSpan(start_row, 0, i - start_row, 1)
                        self.table.setSpan(start_row, 1, i - start_row, 1)
                    start_row = i
                    self.table.setItem(i, 0, QTableWidgetItem(str(k)))
                    self.table.setItem(i, 1, QTableWidgetItem(xk))
                    prev_k = k
                    prev_xk = xk

                self.table.setItem(i, 2, QTableWidgetItem(str(j)))
                self.table.setItem(i, 3, QTableWidgetItem(yj))
                self.table.setItem(i, 4, QTableWidgetItem(str(deltaj)))
                self.table.setItem(i, 5, QTableWidgetItem(str(dj)))
                self.table.setItem(i, 6, QTableWidgetItem(yj_next))

                # Центрирование текста в ячейках
                for col in range(7):
                    item = self.table.item(i, col)
                    if item:
                        item.setTextAlignment(Qt.AlignCenter)

            # Объединение последних ячеек
            self.table.setSpan(start_row, 0, len(log) - start_row, 1)
            self.table.setSpan(start_row, 1, len(log) - start_row, 1)

            # Построение графика
            self.ax.clear()
            x = np.linspace(-5, 5, 100)
            y = np.linspace(-5, 5, 100)
            X, Y = np.meshgrid(x, y)
            Z = np.vectorize(lambda x, y: func([x, y]))(X, Y)
            self.ax.contour(X, Y, Z, levels=50)
            points_x = [entry['xk'][0] for entry in log]
            points_y = [entry['xk'][1] for entry in log]
            self.ax.plot(points_x, points_y, 'ro-', label='Точки итераций')
            self.ax.legend()
            self.canvas.draw()

            # Вывод результатов
            optimal_point = log[-1]['xk']
            optimal_value = log[-1]['fxk']
            num_iterations = len(log)

            results_text = (
                f"Оптимальное значение аргумента: {np.round(optimal_point, 4)}\n"
                f"Оптимальное значение функции: {np.round(optimal_value, 4)}\n"
                f"Количество итераций: {num_iterations}"
            )
            self.results_text.setText(results_text)

        except Exception as e:
            print(f"Ошибка: {e}")

    # ВНИМАНИЕ: ФУНКЦИОНАЛ НЕ РАБОЧИЙ, ПРИЧИНА ОШИБОК НЕИЗВЕСТНА. при клике на таблицу предполагалось что она будет подсвечиваться полупрозрачным прямоугольником
    def highlight_area(self, row):
        # Получаем координаты точки из таблицы
        xk_item = self.table.item(row, 1)  # Столбец "Xk F(Xk)"
        
        # Если ячейка пустая, ищем первую строку объединенного блока
        if xk_item is None or not xk_item.text().strip():
            # Ищем первую строку объединенного блока
            for r in range(row, -1, -1):
                xk_item = self.table.item(r, 1)
                if xk_item and xk_item.text().strip():
                    break
        
        if xk_item and xk_item.text().strip():
            xk_text = xk_item.text().strip()  # Убираем лишние пробелы
            try:
                # Извлекаем координаты из строки вида "[x, y] value"
                xk_coords = xk_text.split()[0]  # Берем первую часть строки (координаты)
                if not xk_coords.startswith('[') or not xk_coords.endswith(']'):
                    raise ValueError("Некорректный формат координат")
                xk_coords = xk_coords[1:-1]  # Убираем квадратные скобки
                # Добавляем запятую между координатами, если её нет
                if ',' not in xk_coords:
                    xk_coords = xk_coords.replace(' ', ',')
                xk = [float(val) for val in xk_coords.split(',')]  # Преобразуем в числа
                if len(xk) != 2:
                    raise ValueError("Ожидалось два значения координат")
                
                # Удаляем старый прямоугольник, если он есть
                if self.current_rectangle:
                    self.current_rectangle.remove()
                    self.current_rectangle = None
                
                # Создаем новый прямоугольник для выделения области
                rect_width = 2  # Ширина области (±1 по оси X)
                rect_height = 2  # Высота области (±1 по оси Y)
                self.current_rectangle = Rectangle(
                    (xk[0] - rect_width / 2, xk[1] - rect_height / 2),  # Левый нижний угол
                    rect_width, rect_height,  # Ширина и высота
                    edgecolor='blue', facecolor='lightblue', alpha=0.5  # Цвет и прозрачность
                )
                self.ax.add_patch(self.current_rectangle)  # Добавляем прямоугольник на график
                self.canvas.draw()  # Перерисовываем график
            except (ValueError, IndexError) as e:
                print(f"Ошибка при обработке координат: {e}")
        else:
            print("Нет данных в выбранной строке или объединенном блоке")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OptimizationUI()
    ex.show()
    sys.exit(app.exec_())