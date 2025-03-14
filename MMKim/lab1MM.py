import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class TDynamicModel:
    def f(self, t, X):
        raise NotImplementedError

class TSpaceCraft(TDynamicModel):
    def __init__(self, mu=3.98603e14):
        self.mu = mu
    
    def f(self, t, X):
        r = np.array([X[0], X[1], X[2]])
        v = np.array([X[3], X[4], X[5]])
        r_norm = np.linalg.norm(r)
        a = -self.mu * r / r_norm**3
        return [v[0], v[1], v[2], a[0], a[1], a[2]]

class TAbstractIntegrator:
    def __init__(self, model, t0, tk, h):
        self.model = model
        self.t0 = t0
        self.tk = tk
        self.h = h
        self.t_eval = np.arange(t0, tk, h)
    
    def MoveTo(self, X0):
        raise NotImplementedError

class EulerIntegrator(TAbstractIntegrator):
    def MoveTo(self, X0):
        return solve_ivp(self.model.f, [self.t0, self.tk], X0, method='RK23', t_eval=self.t_eval)

class RungeKutta4Integrator(TAbstractIntegrator):
    def MoveTo(self, X0):
        return solve_ivp(self.model.f, [self.t0, self.tk], X0, method='RK45', t_eval=self.t_eval)

def open_plot_window():
    X0 = np.array([float(entries[name].get()) for name in ["x", "y", "z", "Vx", "Vy", "Vz"]])
    h = float(entries["h"].get())
    T = float(entries["T"].get())
    
    model = TSpaceCraft()
    euler = EulerIntegrator(model, 0, T, h)
    rk4 = RungeKutta4Integrator(model, 0, T, h)
    
    sol_euler = euler.MoveTo(X0)
    sol_rk4 = rk4.MoveTo(X0)
    
    plot_window = tk.Toplevel()
    plot_window.title("График движения КА")
    
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(sol_euler.y[0], sol_euler.y[1], sol_euler.y[2], label="Euler (RK23)")
    ax.plot(sol_rk4.y[0], sol_rk4.y[1], sol_rk4.y[2], label="Runge-Kutta 4 (RK45)")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("3D Траектория движения КА")
    ax.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, plot_window)
    toolbar.update()
    canvas.get_tk_widget().pack()
    canvas.draw()
    
    open_variable_plot(sol_rk4.t, sol_rk4.y, "Эволюция координат и скоростей по Рунге-Кутту")
    open_variable_plot(sol_euler.t, sol_euler.y, "Эволюция координат и скоростей по Эйлеру")

def open_variable_plot(time, data, type):
    var_window = tk.Toplevel()
    var_window.title(type)
    
    fig, axes = plt.subplots(3, 2, figsize=(10, 8))
    labels = ["X", "Y", "Z", "Vx", "Vy", "Vz"]
    for i, ax in enumerate(axes.flat):
        ax.plot(time, data[i])
        ax.set_xlabel("Время (с)")
        ax.set_ylabel(labels[i])
        ax.set_title(f"{labels[i]} от времени")
        ax.grid()
    
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=var_window)
    canvas.get_tk_widget().pack()
    canvas.draw()

# Создание основного окна
root = tk.Tk()
root.title("Настройки параметров движения КА")

entries = {}
for name in ["x", "y", "z", "Vx", "Vy", "Vz", "h", "T"]:
    frame = tk.Frame(root)
    frame.pack()
    label = tk.Label(frame, text=name)
    label.pack(side=tk.LEFT)
    entry = tk.Entry(frame)
    entry.pack(side=tk.RIGHT)
    entry.insert(0, "0")
    entries[name] = entry

button = tk.Button(root, text="Построить график", command=open_plot_window)
button.pack()

root.mainloop()