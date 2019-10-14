# !/usr/bin/env python3
# generateNetwork.py
# by Nishant Aswani @niniack and Barkin Simsek @woswos

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections
import seaborn as sns
from scipy.stats import powerlaw

def main():

    runs = 5
    randomNetworkHistData = []

    # for i in range(runs):
    #     randomNetwork = makeRandomNetwork(nodes = 500, edges = 1500)
    #     #drawGraph(randomNetwork)
    #     #drawHistogram(randomNetwork)
    #     print(nx.info(randomNetwork))
    #     print("Max degree: " + str(max(sorted([d for n, d in randomNetwork.degree()]))))
    #     print("Min degree: " + str(min(sorted([d for n, d in randomNetwork.degree()]))))
    #     # print("Average distance: " + str(averageDistance(randomNetwork)))
    #     randomNetworkHistData.append(degreeDistribution(randomNetwork))
    #
    # overlayHistogram(randomNetworkHistData)

    scaleFreeNetworkHistData = []

    for i in range(runs):
        scaleFreeNetwork = makeScaleFreeNetwork(nodes = 500, edges = 1600)
        print(nx.info(scaleFreeNetwork))
        print("Max degree: " + str(max(sorted([d for n, d in scaleFreeNetwork.degree()]))))
        print("Min degree: " + str(min(sorted([d for n, d in scaleFreeNetwork.degree()]))))
        # print("Average distance: " + str(averageDistance(scaleFreeNetwork)))
        scaleFreeNetworkHistData.append(degreeDistribution(scaleFreeNetwork))

    overlayHistogram(scaleFreeNetworkHistData)


    '''
    # network = generateNetwork(nodeSize = 100, edgeBudget = 1000, name = "Test Network")
    scaleFreeNetwork = makeScaleFreeNetwork(nodes = 500, edges = 1500)
    print(nx.info(scaleFreeNetwork))
    drawGraph(scaleFreeNetwork)
    drawHistogram(scaleFreeNetwork)
    '''

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

def overlayHistogram(data):
    # bins = np.linspace(0, 15, 10)
    #
    # plt.hist(x, bins, alpha=0.5, label='x', stacked=True, histtype='barstacked')
    # plt.hist(y, bins, alpha=0.5, label='y', stacked=True, histtype='barstacked')
    # plt.legend(loc='upper right')
    # plt.show()

    fig, ax = plt.subplots()

    # print(data)

    xmax = np.amax(data)
    # ymax = np.argmax(np.bincount(data))
    ymax = 0.4
    ax.set_xlim(left=0, right=xmax)
    ax.set_ylim(top=ymax)


    for i in range(len(data)):
        sns.distplot(data[i], fit=powerlaw, ax=ax, kde=False)

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

def drawHistogram(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # print "Degree sequence", degree_sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    # # draw graph in inset
    # plt.axes([0.4, 0.4, 0.5, 0.5])
    # Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
    # pos = nx.spring_layout(G)
    # plt.axis('off')
    # nx.draw_networkx_nodes(G, pos, node_size=20)
    # nx.draw_networkx_edges(G, pos, alpha=0.4)

    #ax.set_xlim([10,50])

    plt.show()


def drawGraph(G):
    if(G == None):
        return None

    plt.figure(1, figsize=(20,10))
    nx.draw_shell(G, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == '__main__':
    main()
