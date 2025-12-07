import numpy as np
import tkinter as tk
from tkinter import ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def update():
    print("updating")
    root.update()
    root.update_idletasks()
    print("updated")

def render(t, yn, labels = [], shocks=[]):
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
    for s in shocks:
        ax.axvline(x=s, linestyle='dotted',color='black')
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

def procure(form):
    if form[1] == bool:
        x = form[2].get()
        return bool(x)
    else:
        return form[1](form[0].get())

"""
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
"""
class Parameters(object):
    def __init__(self):
        self.times = []
        self.timeparameters = []
    def add(self, time, parameters):
        self.times.append(time)
        self.timeparameters.append(parameters)
        print(self.times, self.timeparameters)
    def param(self, name, time):
        stime = max([t for t in self.times if t <= time])
        index = self.times.index(stime)
        p = self.timeparameters[index][name]
        return p
    def vary(self, degrees, distance = 4):
        degrees_keys = list(degrees.keys())
        mods = [-distance for i in range(len(degrees) * len(self.times))]
        skipchange = True
        for i in range(len(degrees) * len(self.times) * (distance * 2 + 1)):
            if not skipchange:
                for j in range(len(mods)):
                    if mods[j] == distance:
                        mods[j] = - distance
                        continue
                    mods[j] += 1
                    break
            skipchange = False
            newparams = Parameters()
            for timeindex in range(len(self.times)):
                newparam = {}
                for k, name in enumerate(degrees_keys):
                    _ = self.timeparameters[timeindex][name] + (mods[timeindex * len(self.times) + k] * degrees[name] / distance)
                    _ = max(0, min(1, _))
                    newparam[name] = _
                newparams.add(self.times[timeindex], newparam)
            yield newparams
def calc(C0, D0, parameters, tdur, step = 0.01):
    U0 = 1 - C0 - D0
    U = [U0]
    C = [C0]
    D = [D0]
    T = [0]
    for i in range(1, round(tdur / step)):
        t = i * step
        T.append(t)
        Cexp = parameters.param("Cexp", t)
        Dexp = parameters.param("Dexp", t)
        reach = parameters.param("reach", t)
        nice = parameters.param("nice", t)
        evil = 1 - nice
        gamma = (Cexp * C[i-1]) + (Dexp * D[i-1]) + reach
        dUdt = - gamma * U[i-1]
        dCdt = nice * gamma * U[i-1]
        dDdt = evil * gamma * U[i-1]
        U.append(U[i-1] + (dUdt * step))
        C.append(C[i-1] + (dCdt * step))
        D.append(D[i-1] + (dDdt * step))
    return T, U, C, D

def modify(x, xoff, n = 1):
    return [max(0, x + xoff * (i/n)) for i in range(-n, n)]

def percent(x):
    return str(round(x * 100, 4)) + "%"

def onclick():
    step = 0.01
    for i in timeplot_area.winfo_children(): i.destroy()
    C0 = procure(input_C0)
    D0 = procure(input_D0)
    Cexp = procure(input_Cexp)
    Dexp = procure(input_Dexp)
    nice = procure(input_nice)
    reach = procure(input_reach)
    tdur = procure(input_tdur)
    #T, U, C, D = calc(C0, D0, Cexp, Dexp, nice, reach, tdur)
    parameters = Parameters()
    parameters.add(0, {"Cexp": Cexp, "Dexp": Dexp, "nice": nice, "reach": reach})
    shocks = []
    if procure(input_doshock):
        shock_t = procure(input_shocktime)
        shock_Cexp = procure(input_shockCexp)
        shock_Dexp = procure(input_shockDexp)
        shock_nice = procure(input_shocknice)
        shockreach = procure(input_shockreach)
        parameters.add(shock_t, {"Cexp": shock_Cexp, "Dexp": shock_Dexp, "nice": shock_nice, "reach": shockreach})
        shocks.append(shock_t)
    T, U, C, D = calc(C0, D0, parameters, tdur)
    fig = render(T, [U, C, D], labels = ["Unreached", "Converts", "Deniers"], shocks = shocks)
    timeplot = FigureCanvasTkAgg(fig, master=timeplot_area)
    timeplot_widget = timeplot.get_tk_widget()
    timeplot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    _U, _C, _D = U[-1], C[-1], D[-1] # we need this
    poolU = []
    poolC = []
    poolD = []
    for params in parameters.vary({"Cexp": 0.01, "Dexp": 0.01, "nice": 0.1, "reach": 0.05}):
        T, U, C, D = calc(C0, D0, params, tdur)
        poolU.append(U[-1])
        poolC.append(C[-1])
        poolD.append(D[-1])
    U = np.array(U)
    C = np.array(C)
    D = np.array(D)
    for i in boxplot_area.winfo_children(): i.destroy()
    fig = render_boxplots([poolU, poolC, poolD], ["Unreached", "Converts", "Deniers"])
    boxplot = FigureCanvasTkAgg(fig, master=boxplot_area)
    boxplot_widget = boxplot.get_tk_widget()
    boxplot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    arrays = [U,C,D]
    expect = [_U,_C,_D]
    update()
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

"""
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
                            parameters = Parameters()
                            parameters.add(0, {"Cexp": Cexp_, "Dexp": Dexp_, "nice": nice_, "reach": reach_})
                            T, U, C, D = calc(C0_, D0_, parameters, tdur)
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
"""

def clonetoshock():
    pass

def inputter(root, label, default = None, variant = float):
    labelnode = tk.Label(root, text = label)
    labelnode.pack()
    entry = None
    var = None
    if variant == float or variant == str:
        entry = tk.Entry(root)
        if default != None:
            entry.insert(0, str(default))
    elif variant == bool:
        var = tk.BooleanVar()
        entry = tk.Checkbutton(root, variable = var)
    entry.pack()
    return (entry, variant, var)

root = tk.Tk()  
root.title("Viral spread calculator")

tab_x = ttk.Notebook()
tab_x.pack(side = "left", expand=True, fill=tk.Y)

controls = tk.Frame()
input_C0 = inputter(controls, "Starting Converts", default = 0.001)
input_D0 = inputter(controls, "Starting Deniers", default = 0.001)
input_Cexp = inputter(controls, "Convert Exposure Coefficient", default = 0.01)
input_Dexp = inputter(controls, "Denier Exposure Coefficient", default = 0.01)
input_nice = inputter(controls, "Fondness Rate", default = 0.6)
input_reach = inputter(controls, "Advertisement Reach Rate", default = 0.01)
input_tdur = inputter(controls, "Time duration", 365)
tk.Button(controls, text="Plot", command=onclick).pack()
tab_x.add(controls, text = "Basic Controls")

advanced = tk.Frame()
input_doshock = inputter(advanced, "Use Shock", default = False, variant = bool)
input_shocktime = inputter(advanced, "Shock Time", default = 182)
tk.Button(advanced, text="Clone Parameters To Shock", command=clonetoshock).pack()
input_shockCexp = inputter(advanced, "Post-Shock Convert Exposure Coefficient", default = 0.1)
input_shockDexp = inputter(advanced, "Post-Shock Denier Exposure Coefficient", default = 0.1)
input_shocknice = inputter(advanced, "Post-Shock Fondness Rate", default = 0.8)
input_shockreach = inputter(advanced, "Post-Shock Advertisement Reach Rate", default = 0.05)
tab_x.add(advanced, text = "Advanced Controls")

tab_y = ttk.Notebook()
tab_y.pack(side = "right", expand=True, fill=tk.BOTH)

timeplot_area = tk.Frame()
#timeplot_area.pack(side = "right", expand=True, fill=tk.BOTH)
tab_y.add(timeplot_area, text = "Time plot")

boxplot_area = tk.Frame()
#boxplot_area.pack(side = "right", expand=True, fill=tk.BOTH)
tab_y.add(boxplot_area, text = "Box plot")

summary_area = tk.Text(wrap='word', height=10, width=40)
summary_area.insert(tk.END, "No content rendered.")
summary_area.config(state='disabled')
#summary_area.pack(side = "right", expand=True, fill=tk.BOTH)
tab_y.add(summary_area, text = "Summary")

def run_on_start(*args):
    root.unbind('<Visibility>')
    onclick() # pre render
root.bind('<Visibility>', run_on_start)

root.mainloop()  


