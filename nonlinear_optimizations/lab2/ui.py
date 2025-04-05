import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, 
                             QTableWidget, QTableWidgetItem, QTextEdit, QSizePolicy)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from algorithm_multidimensional import rosenbrock_discrete
import math
from matplotlib.patches import Rectangle

class OptimizationUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_rectangle = None
        self.is_3d = False  # Флаг для определения 3D случая

    def initUI(self):
        self.setWindowTitle('Optimization Algorithm UI')
        self.setMinimumSize(1000, 800)  # Установка минимального размера окна

        # Main layouts
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        input_layout = QHBoxLayout()
        middle_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()

        # Input section - теперь в одну строку
        input_layout.setSpacing(10)
        
        # Создаем мини-группы для полей ввода с подписями
        def create_input_group(label, widget):
            group = QVBoxLayout()
            group.addWidget(QLabel(label))
            group.addWidget(widget)
            return group

        # Input fields
        self.function_input = QLineEdit(self)
        self.function_input.setMinimumWidth(200)
        self.extremum_type = QComboBox(self)
        self.extremum_type.addItems(['Минимум', 'Максимум'])
        self.start_point_input = QLineEdit(self)
        self.start_point_input.setMinimumWidth(100)
        self.epsilon_input = QLineEdit(self)
        self.epsilon_input.setFixedWidth(50)
        self.alpha_input = QLineEdit(self)
        self.alpha_input.setFixedWidth(50)
        self.beta_input = QLineEdit(self)
        self.beta_input.setFixedWidth(50)
        self.delta_input = QLineEdit(self)
        self.delta_input.setMinimumWidth(100)

        # Set test data
        self.function_input.setText("x[0]**4+2*x[0]**3+(x[1]-4)**2+2*x[2]**2+8*x[2]") # -6*x[0]-4*x[1]+x[0]**2+x[1]**2+18
        self.start_point_input.setText("[1, 0, 1]") # [0, 0, 0] # [1, 1]
        self.epsilon_input.setText("0.1")
        self.alpha_input.setText("2")
        self.beta_input.setText("-0.5")
        self.delta_input.setText("[0.1, 0.1, 0.1]")

        # Add input groups to layout
        input_layout.addLayout(create_input_group('Функция:', self.function_input))
        input_layout.addLayout(create_input_group('Тип экстремума:', self.extremum_type))
        input_layout.addLayout(create_input_group('Начальная точка:', self.start_point_input))
        input_layout.addLayout(create_input_group('Эпсилон:', self.epsilon_input))
        input_layout.addLayout(create_input_group('Альфа:', self.alpha_input))
        input_layout.addLayout(create_input_group('Бета:', self.beta_input))
        input_layout.addLayout(create_input_group('Дельты:', self.delta_input))

        # Button
        self.run_button = QPushButton('Запуск', self)
        self.run_button.clicked.connect(self.run_optimization)
        input_layout.addWidget(self.run_button)

        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['K', 'Xk F(Xk)', 'j', 'yj F(yj)', 'Δj', 'dj', 'yj+Δdj F(yj+Δdj)'])
        self.table.verticalHeader().setVisible(False)
        self.table.cellClicked.connect(self.highlight_area)
        
        # Make table stretch vertically
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Plot area
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Make canvas stretch to fill space
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Results text area (smaller)
        self.results_text = QTextEdit(self)
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(100)  # Ограничиваем высоту текстового поля

        # Layout organization
        main_layout.addLayout(input_layout)  # Вводные данные в одну строку сверху
        main_layout.addWidget(self.table)    # Таблица на всю ширину под ними
        
        # График и результаты
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        bottom_layout.addLayout(plot_layout)
        
        main_layout.addLayout(bottom_layout)
        main_layout.addWidget(self.results_text)

        self.setLayout(main_layout)

    def run_optimization(self):
        try:
            # Get input data
            func_str = self.function_input.text()
            func = lambda x: eval(func_str, {'x': x, 'math': math})
            start_point = eval(self.start_point_input.text())
            self.is_3d = len(start_point) > 2  # Проверяем размерность
            
            epsylon = float(self.epsilon_input.text())
            alpha = float(self.alpha_input.text())
            beta = float(self.beta_input.text())
            delta_starting = eval(self.delta_input.text())

            # Run algorithm
            log = rosenbrock_discrete(func, start_point, epsylon, alpha, beta, delta_starting)

            # Fill table
            self.fill_table(log)

            # Plot only for 2D cases
            if not self.is_3d:
                self.plot_results(log)
            else:
                self.ax.clear()
                self.ax.text(0.5, 0.5, '3D визуализация не поддерживается\nСмотрите табличные данные', 
                            ha='center', va='center', fontsize=12)
                self.canvas.draw()

            # Show results
            self.show_results(log)

        except Exception as e:
            print(f"Ошибка: {e}")
            self.results_text.setText(f"Ошибка: {str(e)}")

    def fill_table(self, log):
        self.table.setRowCount(len(log))
        prev_k = None
        start_row = 0

        for i, entry in enumerate(log):
            k = entry['k']
            
            # Format coordinates based on dimension
            if self.is_3d:
                xk = f"[{np.round(entry['xk'][0], 4)}, {np.round(entry['xk'][1], 4)}, {np.round(entry['xk'][2], 4)}] {np.round(entry['fxk'], 4)}"
                yj = f"[{np.round(entry['yj'][0], 4)}, {np.round(entry['yj'][1], 4)}, {np.round(entry['yj'][2], 4)}] {np.round(entry['fyj'], 4)}"
                yj_next = f"[{np.round(entry['yj_next'][0], 4)}, {np.round(entry['yj_next'][1], 4)}, {np.round(entry['yj_next'][2], 4)}] {np.round(entry['fyj_next'], 4)}"
            else:
                xk = f"[{np.round(entry['xk'][0], 4)}, {np.round(entry['xk'][1], 4)}] {np.round(entry['fxk'], 4)}"
                yj = f"[{np.round(entry['yj'][0], 4)}, {np.round(entry['yj'][1], 4)}] {np.round(entry['fyj'], 4)}"
                yj_next = f"[{np.round(entry['yj_next'][0], 4)}, {np.round(entry['yj_next'][1], 4)}] {np.round(entry['fyj_next'], 4)}"

            j = entry['j']
            deltaj = np.round(entry['deltaj'], 4)
            dj = np.round(entry['dj'], 4)

            # Merge cells for K and Xk columns
            if k == prev_k:
                self.table.setItem(i, 0, QTableWidgetItem(""))
                self.table.setItem(i, 1, QTableWidgetItem(""))
            else:
                if prev_k is not None:
                    self.table.setSpan(start_row, 0, i - start_row, 1)
                    self.table.setSpan(start_row, 1, i - start_row, 1)
                start_row = i
                self.table.setItem(i, 0, QTableWidgetItem(str(k + 1)))
                self.table.setItem(i, 1, QTableWidgetItem(xk))
                prev_k = k

            self.table.setItem(i, 2, QTableWidgetItem(str(j)))
            self.table.setItem(i, 3, QTableWidgetItem(yj))
            self.table.setItem(i, 4, QTableWidgetItem(str(deltaj)))
            self.table.setItem(i, 5, QTableWidgetItem(str(dj)))
            self.table.setItem(i, 6, QTableWidgetItem(yj_next))

            # Center align all cells
            for col in range(7):
                item = self.table.item(i, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

        # Merge last cells
        self.table.setSpan(start_row, 0, len(log) - start_row, 1)
        self.table.setSpan(start_row, 1, len(log) - start_row, 1)

    def plot_results(self, log):
        self.ax.clear()
        
        # Expand plot area
        x_min = min(entry['xk'][0] for entry in log) - 2
        x_max = max(entry['xk'][0] for entry in log) + 2
        y_min = min(entry['xk'][1] for entry in log) - 2
        y_max = max(entry['xk'][1] for entry in log) + 2
        
        x = np.linspace(x_min, x_max, 100)
        y = np.linspace(y_min, y_max, 100)
        X, Y = np.meshgrid(x, y)
        
        func_str = self.function_input.text()
        func = lambda x, y: eval(func_str, {'x': [x, y], 'math': math})
        Z = np.vectorize(func)(X, Y)
        
        self.ax.contour(X, Y, Z, levels=50)
        
        # Plot optimization path
        points_x = [entry['xk'][0] for entry in log]
        points_y = [entry['xk'][1] for entry in log]
        self.ax.plot(points_x, points_y, 'ro-', label='Основные точки итераций (xk)')

        # Colors for iterations
        num_iterations = max(entry['k'] for entry in log) + 1
        colors = plt.cm.viridis(np.linspace(0, 1, num_iterations))

        # Plot intermediate points
        for i, entry in enumerate(log):
            if entry['success']:
                self.ax.plot([entry['yj'][0], entry['yj_next'][0]], 
                            [entry['yj'][1], entry['yj_next'][1]], 
                            '--', color=colors[entry['k']], alpha=0.5)
                self.ax.plot(entry['yj_next'][0], entry['yj_next'][1], 
                            'o', color=colors[entry['k']], alpha=0.5)
            else:
                self.ax.plot(entry['yj_next'][0], entry['yj_next'][1], 
                            'x', color=colors[entry['k']], alpha=0.5,
                            label='Неудачные шаги' if i == 0 else "")

        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Основные точки (xk)', 
                  markerfacecolor='red', markersize=10),
            Line2D([0], [0], marker='x', color='gray', label='Неудачные шаги', 
                  markersize=10),
        ]
        for i in range(num_iterations):
            legend_elements.append(
                Line2D([0], [0], marker='o', color='w', label=f'Итерация {i+1}', 
                      markerfacecolor=colors[i], markersize=10)
            )

        self.ax.legend(handles=legend_elements, title="Легенда")
        self.canvas.draw()

    def show_results(self, log):
        optimal_point = log[-1]['xk']
        optimal_value = log[-1]['fxk']
        num_iterations = max(entry['k'] for entry in log) + 1

        results_text = (
            f"Оптимальное значение аргумента: {np.round(optimal_point, 4)}\n"
            f"Оптимальное значение функции: {np.round(optimal_value, 4)}\n"
            f"Количество итераций: {num_iterations}"
        )
        self.results_text.setText(results_text)

    def highlight_area(self, row):
        if self.is_3d:
            return  # Не выделяем области для 3D случая
            
        xk_item = self.table.item(row, 1)
        
        if xk_item is None or not xk_item.text().strip():
            for r in range(row, -1, -1):
                xk_item = self.table.item(r, 1)
                if xk_item and xk_item.text().strip():
                    break
        
        if xk_item and xk_item.text().strip():
            xk_text = xk_item.text().strip()
            try:
                xk_coords = xk_text.split()[0]
                if not xk_coords.startswith('[') or not xk_coords.endswith(']'):
                    raise ValueError("Некорректный формат координат")
                xk_coords = xk_coords[1:-1]
                if ',' not in xk_coords:
                    xk_coords = xk_coords.replace(' ', ',')
                xk = [float(val) for val in xk_coords.split(',')]
                if len(xk) != 2:
                    raise ValueError("Ожидалось два значения координат")
                
                if self.current_rectangle:
                    self.current_rectangle.remove()
                
                self.current_rectangle = Rectangle(
                    (xk[0] - 1, xk[1] - 1), 2, 2,
                    edgecolor='blue', facecolor='lightblue', alpha=0.5
                )
                self.ax.add_patch(self.current_rectangle)
                self.canvas.draw()
            except Exception as e:
                print(f"Ошибка при обработке координат: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OptimizationUI()
    ex.show()
    sys.exit(app.exec_())