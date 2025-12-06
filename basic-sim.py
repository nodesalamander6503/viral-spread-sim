import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def estimate_inner(c, r, times):
    y = 1 / np.exp(c - r * times)
    return y
def estimate(y_0, rmin, rmax, ravg, tdur):
    c = np.log(1/y_0 - 1)
    times = np.arange(0, round(tdur), 0.01)
    estimates = [estimate_inner(c, r, times) for r in (rmin, rmax, ravg)]
    return estimates, times

def render(y_0, rmin, rmax, ravg, tdur):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    yn, x = estimate(y_0, rmin, rmax, ravg, tdur)
    # (0.01, 0.01, 0.03, 0.02, 50)
    for y in yn:
        ax.plot(x, y)
    
    ax.set_title('Projections')
    ax.set_xlabel('Time')
    ax.set_ylabel('Proportion Affected')
    ax.grid(True)
    
    return fig

def onclick():
    for i in imagery.winfo_children():
        i.destroy()
    y_0 = float(input_y0.get())
    rmin = float(input_rmin.get())
    rmax = float(input_rmax.get())
    ravg = float(input_ravg.get())
    tdur = float(input_tdur.get())
    fig = render(y_0, rmin, rmax, ravg, tdur)
    chart = FigureCanvasTkAgg(fig, master=imagery)
    chart_widget = chart.get_tk_widget()
    chart_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def inputter(root, label, default = None):
    labelnode = tk.Label(root, text = label)
    labelnode.pack()
    entry = tk.Entry(root)
    if default != None:
        entry.insert(0, str(default))
    entry.pack()
    return entry

root = tk.Tk()  
root.title("Viral spread calculator")

controls = tk.Frame()
input_y0 = inputter(controls, "Starting rate", default = 0.01)
input_rmin = inputter(controls, "Min conversion rate", default = 0.01)
input_rmax = inputter(controls, "Max conversion rate", default = 0.03)
input_ravg = inputter(controls, "Average conversion rate", default = 0.02)
input_tdur = inputter(controls, "Time duration", 100)
tk.Button(controls, text="Solve", command=onclick).pack()
controls.pack(side = "left")

imagery = tk.Frame()
imagery.pack(side = "right", expand=True, fill=tk.BOTH)

onclick() # pre render

root.mainloop()  


