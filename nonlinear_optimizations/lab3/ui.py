import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, 
                             QTableWidget, QTableWidgetItem, QTextEdit, QSizePolicy,
                             QGroupBox, QRadioButton, QButtonGroup, QSplitter)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from algorithm_multidimensional import cyclic_coordinate_descend_nolog
import math
from matplotlib.patches import Rectangle

class PenaltyMethodUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_rectangle = None
        self.points_history = []
        self.annotation = None
        self.contour = None
        self.constraint_line = None
        self.constraint_area = None

    def initUI(self):
        self.setWindowTitle('Метод штрафных функций')
        self.setMinimumSize(1000, 800)
        
        # Основной макет с разделителем
        main_splitter = QSplitter(Qt.Vertical)
        
        # Верхняя часть - ввод данных и таблица
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        
        # Левая панель - элементы ввода
        left_panel = QVBoxLayout()
        left_panel.setContentsMargins(5, 5, 5, 5)
        
        # Ввод функции
        func_group = QGroupBox("Целевая функция и ограничения")
        func_layout = QVBoxLayout()
        self.function_input = QLineEdit("(x[0] - 1)**2 + (x[1] + 5)**2")
        self.constraint_input = QLineEdit("x[0]**2 - x[1] <= 0")
        func_layout.addWidget(QLabel("Минимизировать:"))
        func_layout.addWidget(self.function_input)
        func_layout.addWidget(QLabel("При ограничении:"))
        func_layout.addWidget(self.constraint_input)
        func_group.setLayout(func_layout)
        left_panel.addWidget(func_group)

        # Параметры
        param_group = QGroupBox("Параметры метода")
        param_layout = QVBoxLayout()
        
        self.start_point_input = QLineEdit("[0, -4]")
        self.epsilon_input = QLineEdit("0.01")
        
        param_layout.addWidget(QLabel("Начальная точка:"))
        param_layout.addWidget(self.start_point_input)
        param_layout.addWidget(QLabel("Точность (ε):"))
        param_layout.addWidget(self.epsilon_input)
        
        # Стратегии штрафов
        strategy_group = QGroupBox("Стратегия изменения μ")
        strategy_layout = QVBoxLayout()
        self.strategy_a = QRadioButton("a) μ₁=0.1 → μ₂=100")
        self.strategy_b = QRadioButton("b) μ=100 из (1,-5)")
        self.strategy_c = QRadioButton("c) μ=0.1,1,10,100")
        self.strategy_d = QRadioButton("d) μ=100 из X₁")
        self.strategy_a.setChecked(True)
        
        strategy_layout.addWidget(self.strategy_a)
        strategy_layout.addWidget(self.strategy_b)
        strategy_layout.addWidget(self.strategy_c)
        strategy_layout.addWidget(self.strategy_d)
        strategy_group.setLayout(strategy_layout)
        param_layout.addWidget(strategy_group)
        
        param_group.setLayout(param_layout)
        left_panel.addWidget(param_group)
        
        # Кнопка запуска и результаты
        self.run_button = QPushButton('Выполнить оптимизацию')
        self.run_button.clicked.connect(self.run_optimization)
        left_panel.addWidget(self.run_button)
        
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(80)
        left_panel.addWidget(self.results_text)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['K', 'μk', 'Xk+1=Xμk', 'F(Xk+1)', 'α(Xμk)', 'Θ(μk)', 'μkα(Xμk)', 'Шаги'])
        self.table.verticalHeader().setVisible(False)
        self.table.cellClicked.connect(self.highlight_point)
        
        # Добавление виджетов в верхний макет
        top_layout.addLayout(left_panel, stretch=1)
        top_layout.addWidget(self.table, stretch=2)
        
        # Нижняя часть - график
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(5, 0, 5, 5)
        
        # Фигура с компактной панелью инструментов
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        
        # Создание компактной панели инструментов
        toolbar = NavigationToolbar(self.canvas, self)
        toolbar.setIconSize(toolbar.iconSize() * 0.8)
        
        # Макет графика с панелью инструментов сверху
        plot_layout = QVBoxLayout()
        plot_layout.setSpacing(2)
        plot_layout.addWidget(toolbar)
        plot_layout.addWidget(self.canvas)
        
        bottom_layout.addLayout(plot_layout)
        
        # Добавление в основной разделитель
        main_splitter.addWidget(top_widget)
        main_splitter.addWidget(bottom_widget)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)
        
        # Основной макет окна
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)

    def run_optimization(self):
        try:
            # Получение входных данных
            func_str = self.function_input.text()
            constraint_str = self.constraint_input.text()
            start_point = eval(self.start_point_input.text())
            epsylon = float(self.epsilon_input.text())
            
            def penalty_function(x, mu):
                f = eval(func_str, {'x': x, 'math': math})
                constraint = eval(constraint_str.split('<=')[0], {'x': x, 'math': math})
                return f + mu * max(constraint, 0)
            
            self.points_history = []
            table_data = []
            
            if self.strategy_a.isChecked():
                # Стратегия a
                x1 = cyclic_coordinate_descend_nolog(
                    lambda x: penalty_function(x, 0.1), epsylon, start_point, [-10, 10])
                x2 = cyclic_coordinate_descend_nolog(
                    lambda x: penalty_function(x, 100), epsylon, x1, [-10, 10])
                
                self.points_history.extend([('μ=0.1', start_point, x1), ('μ=100', x1, x2)])
                
                table_data.extend([
                    self.create_table_row(1, 0.1, x1, func_str, constraint_str, penalty_function, 'X₁ → X₂'),
                    self.create_table_row(2, 100, x2, func_str, constraint_str, penalty_function, 'X₂ → X₃')
                ])
                
            elif self.strategy_b.isChecked():
                # Стратегия b
                x_opt = cyclic_coordinate_descend_nolog(
                    lambda x: penalty_function(x, 100), epsylon, [1, -5], [-10, 10])
                self.points_history.append(('μ=100', [1, -5], x_opt))
                
                table_data.append(
                    self.create_table_row(1, 100, x_opt, func_str, constraint_str, penalty_function, '(1,-5) → X₁')
                )
                
            elif self.strategy_c.isChecked():
                # Стратегия c
                x_current = start_point
                mus = [0.1, 1, 10, 100]
                
                for i, mu in enumerate(mus):
                    x_next = cyclic_coordinate_descend_nolog(
                        lambda x: penalty_function(x, mu), epsylon, x_current, [-10, 10])
                    self.points_history.append((f'μ={mu}', x_current, x_next))
                    
                    table_data.append(
                        self.create_table_row(
                            i+1, mu, x_next, func_str, constraint_str, penalty_function, f'X{i+1} → X{i+2}')
                    )
                    x_current = x_next
                    
            elif self.strategy_d.isChecked():
                # Стратегия d
                x_opt = cyclic_coordinate_descend_nolog(
                    lambda x: penalty_function(x, 100), epsylon, start_point, [-10, 10])
                self.points_history.append(('μ=100', start_point, x_opt))
                
                table_data.append(
                    self.create_table_row(1, 100, x_opt, func_str, constraint_str, penalty_function, 'X₁ → X₂')
                )
            
            self.fill_table(table_data)
            self.plot_results()
            
            final_point = self.points_history[-1][2]
            final_value = eval(func_str, {'x': final_point, 'math': math})
            constraint_violation = max(eval(constraint_str.split('<=')[0], {'x': final_point, 'math': math}), 0)
            
            self.results_text.setText(
                f"Финальная точка: {np.round(final_point, 4)}\n"
                f"Значение функции: {np.round(final_value, 4)}\n"
                f"Нарушение ограничения: {np.round(constraint_violation, 6)}\n"
                f"Количество шагов: {len(self.points_history)}"
            )
            
        except Exception as e:
            self.results_text.setText(f"Ошибка: {str(e)}")

    def create_table_row(self, k, mu, x, func_str, constraint_str, penalty_func, steps):
        x_rounded = [round(val, 6) for val in x]  # Округление координат
        f_val = round(eval(func_str, {'x': x, 'math': math}), 6)
        alpha = round(max(eval(constraint_str.split('<=')[0], {'x': x, 'math': math}), 0), 6)
        theta = round(penalty_func(x, mu), 6)
        mu_alpha = round(mu * alpha, 6)
        
        return {
            'K': k, 
            'μk': mu, 
            'Xk+1': x_rounded,
            'F(Xk+1)': f_val,
            'α(Xμk)': alpha,
            'Θ(μk)': theta,
            'μkα(Xμk)': mu_alpha,
            'Steps': steps
        }

    def fill_table(self, data):
        self.table.setRowCount(len(data))
        
        for row, entry in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(entry['K'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(entry['μk'])))
            self.table.setItem(row, 2, QTableWidgetItem(f"[{entry['Xk+1'][0]:.6f}, {entry['Xk+1'][1]:.6f}]"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{entry['F(Xk+1)']:.6f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{entry['α(Xμk)']:.6f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{entry['Θ(μk)']:.6f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{entry['μkα(Xμk)']:.6f}"))
            self.table.setItem(row, 7, QTableWidgetItem(entry['Steps']))
            
            for col in range(8):
                item = self.table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

    def plot_results(self):
        # Полная очистка осей
        self.ax.clear()
        
        # Сброс графических объектов
        self.contour = None
        self.constraint_line = None
        self.constraint_area = None
        self.current_rectangle = None
        if self.annotation:
            self.annotation.remove()
            self.annotation = None
        
        # Получение данных для построения
        func_str = self.function_input.text()
        constraint_str = self.constraint_input.text()
        
        # Сбор всех точек
        all_points = []
        for _, start, end in self.points_history:
            all_points.append(start)
            all_points.append(end)
        
        if not all_points:
            all_points = [[0, -4], [1, -5]]
        
        # Вычисление границ
        x_coords = [p[0] for p in all_points]
        y_coords = [p[1] for p in all_points]
        
        x_padding = max(1, (max(x_coords) - min(x_coords)) * 0.3)
        y_padding = max(1, (max(y_coords) - min(y_coords)) * 0.3)
        
        x_min, x_max = min(x_coords)-x_padding, max(x_coords)+x_padding
        y_min, y_max = min(y_coords)-y_padding, max(y_coords)+y_padding
        
        # Создание сетки с повышенной точностью
        x = np.linspace(x_min, x_max, 200)
        y = np.linspace(y_min, y_max, 200)
        X, Y = np.meshgrid(x, y)
        
        # Вычисление функций
        try:
            Z_func = np.vectorize(lambda x, y: eval(func_str, {'x': [x, y], 'math': math}))(X, Y)
            Z_constraint = np.vectorize(lambda x, y: eval(constraint_str.split('<=')[0], {'x': [x, y], 'math': math}))(X, Y)
        except Exception as e:
            self.results_text.setText(f"Ошибка вычисления: {str(e)}")
            return
        
        # Построение контуров функции
        self.contour = self.ax.contour(X, Y, Z_func, levels=20, cmap='viridis')
        self.figure.colorbar(self.contour, ax=self.ax, label='Значение функции')
        
        # Построение ограничений
        self.constraint_line = self.ax.contour(X, Y, Z_constraint, levels=[0], colors='red', linewidths=2)
        self.constraint_area = self.ax.fill_between(x, x**2, y_max, color='red', alpha=0.1, label='Недопустимая область')
        
        # Построение путей оптимизации с точными метками
        colors = plt.cm.plasma(np.linspace(0, 1, len(self.points_history)))
        legend_handles = []
        legend_labels = []
        
        for i, (label, start, end) in enumerate(self.points_history):
            # Линия пути
            line = self.ax.plot([start[0], end[0]], [start[1], end[1]], 
                            'o-', color=colors[i], markersize=6, linewidth=2)[0]
            
            # Метка начальной точки для первого шага
            if i == 0:
                self.ax.text(start[0], start[1], 'X₁', ha='center', va='center',
                            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
            
            # Метка конечной точки
            self.ax.text(end[0], end[1], f'X{i+2}', ha='center', va='center',
                        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
            
            # Добавление в легенду
            if label not in legend_labels:
                legend_handles.append(line)
                legend_labels.append(label)
        
        # Настройка легенды
        if legend_handles:
            self.ax.legend(legend_handles, legend_labels,
                        bbox_to_anchor=(1.05, 1),
                        loc='upper left',
                        title="Стратегии",
                        fontsize='small')
        
        # Настройка осей
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_xlabel('X1', fontsize=10)
        self.ax.set_ylabel('X2', fontsize=10)
        self.ax.set_title('Метод штрафных функций', fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.5)
        
        # Обновление графика
        self.figure.tight_layout()
        self.canvas.draw()
        self.canvas.flush_events()

    def highlight_point(self, row):
        if row >= len(self.points_history):
            return
            
        point_str = self.table.item(row, 2).text()
        point = [float(x) for x in point_str[1:-1].split(',')]
        
        if self.current_rectangle:
            self.current_rectangle.remove()
        if self.annotation:
            self.annotation.remove()
        
        self.current_rectangle = Rectangle(
            (point[0]-0.2, point[1]-0.2), 0.4, 0.4,
            edgecolor='blue', facecolor='none', linewidth=2
        )
        self.ax.add_patch(self.current_rectangle)
        
        self.annotation = self.ax.annotate(
            f"X{row+1}", xy=(point[0], point[1]), xytext=(10, 10),
            textcoords='offset points', 
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->'))
        
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PenaltyMethodUI()
    ex.show()
    sys.exit(app.exec_())