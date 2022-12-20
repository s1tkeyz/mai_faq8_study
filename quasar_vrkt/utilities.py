import json
from matplotlib import pyplot as plt
from matplotlib import style

def load_simulation_config(_path):
    """Returns configuration dictionary"""
    with open(_path, "r") as config:
        data = json.load(config)
        return data

def draw_graph(arr_x, arr_y, lab_x, lab_y, name):
    """Draws a plot using Matplotlib"""
    style.use("ggplot")
    plt.plot(arr_x, arr_y)
    plt.title(name)
    plt.ylabel(lab_y)
    plt.xlabel(lab_x) 
    plt.show()