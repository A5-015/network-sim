# !/usr/bin/env python3
# generateNetwork.py
# by Nishant Aswani @niniack and Barkin Simsek @woswos

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections

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

    plt.show()

def drawGraph(G):
    if(G==None):
        return None
    plt.figure(1, figsize=(20,10))
    nx.draw_networkx(G, with_labels=True, font_weight='bold')
    plt.show()


randomNetwork = makeRandomNetwork(100, 1000);
drawGraph(randomNetwork)
drawHistogram(randomNetwork)
