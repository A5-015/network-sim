# !/usr/bin/env python3
# generateNetwork.py
# by Nishant Aswani @niniack and Barkin Simsek @woswos

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections
import seaborn as sns
from scipy.stats import powerlaw
from scipy.stats import poisson

def main():

    runs = 5

    nodes = 1000
    edges = nodes*2

    averageDistanceData = np.zeros(runs)
    averageDegreeData = np.zeros(runs)

    ################################################################
    ################################################################

    randomNetworkHistData = []

    for i in range(runs):
        print("Simulating network #" + str(i))
        randomNetwork = makeRandomNetwork(nodes = nodes, edges = edges)
        print(nx.info(randomNetwork))
        print("Max degree: " + str(max(sorted([d for n, d in randomNetwork.degree()]))))
        print("Min degree: " + str(min(sorted([d for n, d in randomNetwork.degree()]))))
        print("Average distance: " + str(averageDistance(randomNetwork)))
        print('\n')
        averageDistanceData[i] = averageDistance(randomNetwork)
        averageDegreeData[i] = averageDegree(randomNetwork)
        randomNetworkHistData.append(degreeDistribution(randomNetwork))

    # PLOTTING
    overlayHistogram(randomNetworkHistData, type="random")
    plotAvgDistance(averageDistanceData)
    plotServiceTime(averageDegreeData)

    np.savetxt('randomNetworkAvgDistance.txt', averageDistanceData)
    np.savetxt('randomNetworkAvgDegree.txt', averageDegreeData)
    np.savetxt('randomNetworkHistData.txt', randomNetworkHistData)

    ################################################################
    ################################################################
    '''
    scaleFreeNetworkHistData = []

    for i in range(runs):
        print("Simulating network #" + str(i))
        scaleFreeNetwork = makeScaleFreeNetwork(nodes = nodes, edges = edges)
        print(nx.info(scaleFreeNetwork))
        print("Max degree: " + str(max(sorted([d for n, d in scaleFreeNetwork.degree()]))))
        print("Min degree: " + str(min(sorted([d for n, d in scaleFreeNetwork.degree()]))))
        # print("Average distance: " + str(averageDistance(scaleFreeNetwork)))
        print('\n')
        # averageDistanceData[i] = averageDistance(scaleFreeNetwork)
        averageDegreeData[i] = averageDegree(scaleFreeNetwork)
        scaleFreeNetworkHistData.append(degreeDistribution(scaleFreeNetwork))


    # PLOTTING
    overlayHistogram(scaleFreeNetworkHistData, type="scalefree")
    plotAvgDistance(averageDistanceData)
    plotServiceTime(averageDegreeData)


    # np.savetxt('scaleFreeNetworkAvgDistance.txt', averageDistanceData)
    np.savetxt('scaleFreeNetworkAvgDegree.txt', averageDegreeData)
    np.savetxt('scaleFreeNetworkHistData.txt', scaleFreeNetworkHistData)
    '''
    ################################################################
    ################################################################

def plotAvgDistance(data):

    fig, ax = plt.subplots()
    sns.distplot(data, ax=ax, kde=False, bins=None)

    axis_font = {'size':'15'}
    title_font = {'size':'20'}
    ax.tick_params(labelsize=12)

    ax.set_xlabel('Average Distance', **axis_font)
    ax.set_ylabel('Frequency', **axis_font)
    ax.set_title("Average Distance", **title_font)

    plt.show()


def plotServiceTime(data):

    fig, ax = plt.subplots()
    data = np.exp(-data)
    sns.distplot(data, ax=ax, kde=False, bins=None)

    axis_font = {'size':'15'}
    title_font = {'size':'20'}
    ax.tick_params(labelsize=12)

    ax.set_xlabel('Inverse Degree', **axis_font)
    ax.set_ylabel('Frequency', **axis_font)
    ax.set_title("Service Time", **title_font)

    plt.show()


def averageDegree(G):
    s = sum([v for k, v in G.degree()])
    res = (float(s)/float(G.number_of_nodes()))

    return res


def averageDistance(G):

    average = 0

    for i in range(nx.number_of_nodes(G)):
        for k in range(i):
            try:
                average = (nx.shortest_path_length(G, i, k) + average) / 2
            except:
                # just for having something in the except case
                a = 1

    return average


def degreeDistribution(G):
    a = np.array(sorted([d for n, d in G.degree()]))
    mini = np.array(min(sorted([d for n, d in G.degree()])))
    a = np.subtract(a, mini)
    # for fixing the offset
    return a


def overlayHistogram(data, type):
    fig, ax = plt.subplots()

    # print(data)

    xmax = np.amax(data)
    # ymax = np.argmax(np.bincount(data))
    ax.set_xlim(left=0, right=xmax)
    # ax.set_ylim(top=ymax)

    axis_font = {'fontname':'Arial', 'size':'15'}
    title_font = {'fontname': 'Arial', 'size':'20'}
    ax.tick_params(labelsize=12)


    if (type == "random"):
        for i in range(len(data)):
            mlest = data[i].mean()
            sns.distplot(data[i], ax=ax, kde=False)
            plt.plot(data[i], poisson.pmf(data[i], mlest)*len(data[i]), 'ko', markersize=4)

        ax.set_xlabel('Degree', **axis_font)
        ax.set_ylabel('Frequency', **axis_font)
        ax.set_title("Degree Distribution of a Random Network \n Modeled by a Poisson Distribution", **title_font)

    else:
        for i in range(len(data)):
            sns.distplot(data[i], ax=ax, kde=False, fit=powerlaw)
        ax.set_xlabel('Degree', **axis_font)
        ax.set_ylabel('Frequency', **axis_font)
        ax.set_title("Degree Distribution of a Scale-Free Network \n Modeled by a Power Law Distribution", **title_font)

    #ax.legend()
    #plt.legend(labels=['a', 'b', 'c'])
    plt.show()


def makeRandomNetwork(nodes, edges):

    if(edges > nodes*(nodes-1)/2):
        print("Too many edges")
        return None

    nodeArray = np.arange(nodes)
    edgeArray = np.zeros((edges, 2))

    for i in range(edges):
        n1 = np.random.randint(0,nodes)
        n2 = np.random.randint(0,nodes)
        while(n2 == n1):
            n2 = np.random.randint(0,nodes)
        edgeArray[i][0] = n1;
        edgeArray[i][1] = n2;

    G = nx.Graph()
    G.add_nodes_from(nodeArray)
    G.add_edges_from(edgeArray)

    return G


def makeScaleFreeNetwork(nodes, edges):

    if(edges > nodes*(nodes-1)/2):
        print("Too many edges")
        return None

    initialNodes = 10
    remainingNodes = np.arange(initialNodes, nodes)
    G = nx.complete_graph(initialNodes)

    for i in remainingNodes-initialNodes:
        # n1 = np.random.randint(i,len(remainingNodes))
        n1 = i;
        n2Array = _selectNodes(G, int(edges/len(remainingNodes)) )
        for j in range(len(n2Array)):
            G.add_edge(n1, n2Array[j])

    return G


def _selectNodes(G, numConnections):

    networkNodeWeights = []
    selectedNodes = []

    for node in G.nodes():
        nodeDegree = G.degree(node)
        nodeProbability = nodeDegree / (2 * len(G.edges()))
        networkNodeWeights.append(nodeProbability)

    for i in range(numConnections):
        selectedNodes.append(np.random.choice(G.nodes(),p=networkNodeWeights))

    return selectedNodes


if __name__ == '__main__':
    main()
