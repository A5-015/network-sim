import matplotlib.pyplot as plt
import csv
import numpy as np
import collections
import seaborn as sns
from scipy import stats
from scipy.stats import powerlaw


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

def calculateDistributionStatistics(data_path, type = "other"):
    if (type == "other"):
        column = 5
        df = np.loadtxt(data_path, delimiter=',', skiprows=1)
        mean = np.mean(df[:,column])
        var = np.var(df[:,column])
        print("Avg val: " + str(mean))
        print("Var: " + str(var))

    else:
        df = np.loadtxt(data_path)
        min = np.amin(df)
        max = np.amax(df)
        mean = np.mean(df)
        var = np.var(df)
        print("Min degree: " + str(min))
        print("Max degree: " + str(max))
        print("Avg degree: " + str(mean))
        print("Var degree: " + str(var))

        if (type == "sf" or type == "scalefree"):
            print("mode:" + str(stats.mode(df)))
            df = np.subtract(df, 1)
            gamma = powerlaw.fit(df)
            print("Gamma: " + str(gamma))
            sns.distplot(df, kde=False, fit=powerlaw)
            plt.show()



# data_path = '../averagesFiftyRuns.csv'
# plot(data_path = data_path, xlabel = 'Average Degree', ylabel = 'Frequency', title = "Average Degree in a Scale-Free Network \n with 5000 Nodes and 2n Edges", column = 2)
# plot(data_path = data_path, xlabel = 'Average Degree', ylabel = 'Frequency', title = "Average Degree in a Random Network \n with 5000 Nodes and 2n Edges", column = 6)
# plot(data_path = data_path, xlabel = 'Average Distance', ylabel = 'Frequency', title = "Average Distance in a Scale-Free Network \n with 5000 Nodes and 2n Edges", column = 5)
# plot(data_path = data_path, xlabel = 'Average Distance', ylabel = 'Frequency', title = "Average Distance in a Random Network \n with 5000 Nodes and 2n Edges", column = 7)


data_path = '../averagesFiftyRuns.csv'
calculateDistributionStatistics(data_path = data_path)
