# !/usr/bin/env python3
# generateNetwork.py
# by Nishant Aswani @niniack and Barkin Simsek @woswos

def makeRandomNetwork(nodes, probability):
    G = nx.gnp_random_graph(nodes, probability)
    return G

def makeScaleFreeNetwork(nodes):
    G = nx.scale_free_network(nodes)
    return G

def returnNumberofEdges(G):
    numEdges = G.number_of_edges()
    return numEdges

def returnNodeDegree(G, node):
    degrees = G.degree(node)
    return degrees

def drawGraph(G):
    plt.figure(1, figsize=(20,10))
    nx.draw_networkx(G, with_labels=True, font_weight='bold')
    plt.show()
