import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def update():
    print("updating")
    root.update()
    root.update_idletasks()
    print("updated")

def render(t, yn, labels = []):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    colors = "rgb"
    mid = int(len(t)*2/3)
    for i in range(len(yn)):
        y = yn[i]
        label = ":3"
        if len(labels) > i:
            label = labels[i]
        ax.text(t[mid], y[mid], label, fontsize=10, va='center')
        ax.plot(t, y, colors[i] + "-", label = label)
    
    ax.set_title('Projections')
    ax.set_xlabel('Time')
    ax.set_ylabel('Proportions')
    ax.legend()
    ax.grid(True)
    
    return fig

def render_boxplots(datasets, labels):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.boxplot(datasets, labels = labels)
    return fig

def procure_num(form):
    return float(form.get())

def calc(C0, D0, Cexp, Dexp, nice, reach, tdur, step = 0.01):
    U0 = 1 - C0 - D0
    evil = 1 - nice
    U = [U0]
    C = [C0]
    D = [D0]
    T = [0]
    for i in range(1, round(tdur / step)):
        t = i * step
        T.append(t)
        gamma = (Cexp * C[i-1]) + (Dexp * D[i-1]) + reach
        dUdt = - gamma * U[i-1]
        dCdt = nice * gamma * U[i-1]
        dDdt = evil * gamma * U[i-1]
        #print(gamma, dUdt, dCdt, dDdt)
        U.append(U[i-1] + (dUdt * step))
        C.append(C[i-1] + (dCdt * step))
        D.append(D[i-1] + (dDdt * step))
    print(":3")
    return T, U, C, D

def modify(x, xoff, n = 1):
    return [max(0, x + xoff * (i/n)) for i in range(-n, n)]

def percent(x):
    return str(round(x * 100, 4)) + "%"

def onclick():
    step = 0.01
    for i in timeplot_area.winfo_children(): i.destroy()
    C0 = procure_num(input_C0)
    D0 = procure_num(input_D0)
    Cexp = procure_num(input_Cexp)
    Dexp = procure_num(input_Dexp)
    nice = procure_num(input_nice)
    reach = procure_num(input_reach)
    tdur = procure_num(input_tdur)
    T, U, C, D = calc(C0, D0, Cexp, Dexp, nice, reach, tdur)
    fig = render(T, [U, C, D], labels = ["Unreached", "Converts", "Deniers"])
    timeplot = FigureCanvasTkAgg(fig, master=timeplot_area)
    timeplot_widget = timeplot.get_tk_widget()
    timeplot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    _U, _C, _D = U[-1], C[-1], D[-1] # preserve it!!
    update()
    # well look
    # the main spectacle is the graph
    # we can handle the advanced math™ subsequently, see
    C0_off = 0.005
    D0_off = 0.005
    Cexp_off = 0.005
    Dexp_off = 0.005
    nice_off = 0.03
    reach_off = 0.01
    poolU = []
    poolC = []
    poolD = []
    for C0_ in modify(C0, C0_off):
        for D0_ in modify(D0, D0_off):
            for Cexp_ in modify(Cexp, Cexp_off):
                for Dexp_ in modify(Dexp, Dexp_off):
                    for nice_ in modify(nice, nice_off):
                        for reach_ in modify(reach, reach_off):
                            T, U, C, D = calc(C0_, D0_, Cexp_, Dexp_, nice_, reach_, tdur)
                            poolU.append(U[-1])
                            poolC.append(C[-1])
                            poolD.append(D[-1])
    for i in boxplot_area.winfo_children(): i.destroy()
    fig = render_boxplots([poolU, poolC, poolD], ["Unreached", "Converts", "Deniers"])
    boxplot = FigureCanvasTkAgg(fig, master=boxplot_area)
    boxplot_widget = boxplot.get_tk_widget()
    boxplot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    U = np.array(U)
    C = np.array(C)
    D = np.array(D)
    arrays = [U,C,D]
    expect = [_U,_C,_D]
    labels = ["Unreached", "Converts", "Deniers"]
    summary = ""
    for i in range(3):
        summary += "We expect the proportion of the population who are " + labels[i] + " to cumulate as " + percent(expect[i]) + ". Across the distribution of simulations, the mean was " + percent(arrays[i].mean()) + " and a standard deviation of " + percent(arrays[i].std()) + ".\n\n"
    summary_area.config(state='normal')
    summary_area.delete(1.0, tk.END)
    summary_area.insert(tk.END, summary)
    summary_area.config(state='disabled')
    print(summary)
    update()

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
input_C0 = inputter(controls, "Starting Converts", default = 0.001)
input_D0 = inputter(controls, "Starting Deniers", default = 0.001)
input_Cexp = inputter(controls, "Convert Exposure Coefficient", default = 0.05)
input_Dexp = inputter(controls, "Denier Exposure Coefficient", default = 0.05)
input_nice = inputter(controls, "Fondness Rate", default = 0.7)
input_reach = inputter(controls, "Advertisement Reach Rate", default = 0.01)
input_tdur = inputter(controls, "Time duration", 365)
tk.Button(controls, text="Plot", command=onclick).pack()
controls.pack(side = "left")

timeplot_area = tk.Frame()
timeplot_area.pack(side = "right", expand=True, fill=tk.BOTH)

boxplot_area = tk.Frame()
boxplot_area.pack(side = "right", expand=True, fill=tk.BOTH)

summary_area = tk.Text(wrap='word', height=10, width=40)
summary_area.insert(tk.END, "No content rendered.")
summary_area.config(state='disabled')
summary_area.pack(side = "right", expand=True, fill=tk.BOTH)

def run_on_start(*args):
    root.unbind('<Visibility>')
    onclick() # pre render
root.bind('<Visibility>', run_on_start)

root.mainloop()  


