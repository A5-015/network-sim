import matplotlib.pyplot as plt
import csv
import numpy as np
import collections
import seaborn as sns

def plot(data_path, xlabel, ylabel, title, column):
    fig, ax = plt.subplots()

    axis_font = {'size':'15'}
    title_font = {'size':'20'}
    ax.tick_params(labelsize=12)

    ax.set_xlabel(xlabel, **axis_font)
    ax.set_ylabel(ylabel, **axis_font)
    ax.set_title(title, **title_font)

    data = np.loadtxt(data_path, delimiter=',', skiprows=1)

    sns.distplot(data[:,column], ax=ax, kde=False, bins=None)

    plt.show()

data_path = '../averagesFiftyRuns.csv'

plot(data_path = data_path, xlabel = 'Average Degree', ylabel = 'Frequency', title = "Average Degree in a Scale-Free Network \n with 5000 Nodes and 2n Edges", column = 2)

plot(data_path = data_path, xlabel = 'Average Degree', ylabel = 'Frequency', title = "Average Degree in a Random Network \n with 5000 Nodes and 2n Edges", column = 6)

plot(data_path = data_path, xlabel = 'Average Distance', ylabel = 'Frequency', title = "Average Distance in a Scale-Free Network \n with 5000 Nodes and 2n Edges", column = 5)

plot(data_path = data_path, xlabel = 'Average Distance', ylabel = 'Frequency', title = "Average Distance in a Random Network \n with 5000 Nodes and 2n Edges", column = 7)
