import matplotlib.pyplot as plt
import csv
import numpy as np
import collections
import seaborn as sns

data_path = '../averagesFiftyRuns.csv'

fig, ax = plt.subplots()

axis_font = {'size':'15'}
title_font = {'size':'20'}
ax.tick_params(labelsize=12)

ax.set_xlabel('Average Degree', **axis_font)
ax.set_ylabel('Frequency', **axis_font)
ax.set_title("Average Degree in a Scale-Free Network with 5000 Nodes and 2n Edges", **title_font)

data = np.loadtxt(data_path, delimiter=',', skiprows=1)

sns.distplot(data[:,2], ax=ax, kde=False, bins=None)

mng = plt.get_current_fig_manager()
mng.window.showMaximized()
plt.show()
