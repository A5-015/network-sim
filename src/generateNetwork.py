# !/usr/bin/env python3
# generateNetwork.py
# by Nishant Aswani @niniack and Barkin Simsek @woswos

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections

def main():

    randomNetwork = makeRandomNetwork(100, 1000);
    print(nx.info(randomNetwork))
    #drawGraph(randomNetwork)
    #drawHistogram(randomNetwork)


    network = generateNetwork(nodeSize = 100, edgeBudget = 1000, name = "Test Network")
    print(nx.info(network))
    #drawWeightedGraph(network)
    #drawHistogram(network)


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

def generateNetwork(nodeSize, edgeBudget, name = "network"):

    # Check if given parameters make sense
    if(edgeBudget > nodeSize*(nodeSize-1)/2):
        print("Provided too many edges, pleas check the values")
        return None

    # Create an empty graph
    G = nx.Graph()
    G.name = name

    # For normalzing weights
    mappingRatio = float(1) / float(nodeSize)

    # Initialize all nodes to equal weights
    for m in range(nodeSize):
        G.add_node(m, weight = float(mappingRatio))

    # Edge budget loop counter
    i = 0

    while i < edgeBudget:
        weights = nx.get_node_attributes(G, 'weight')
        #print(weights)

        # For the first edge only
        if i == 0:
            # Choose any random two nodes
            n1 = np.random.randint(0, nodeSize)
            n2 = np.random.randint(0, nodeSize)

            # Choose another node if they are same
            while(n2 == n1):
                n2 = np.random.randint(0, nodeSize)

        else:
            # This returns an array but we want a single value, that is why
            #       we have [0] at the end
            n1 = np.random.choice(a = nodeSize, size = 1, replace = True, p = list(weights.values()))[0]
            n2 = np.random.choice(a = nodeSize, size = 1, replace = True, p = list(weights.values()))[0]

            # Choose another node if they are same
            while(n2 == n1):
                n2 = np.random.choice(a = nodeSize, size = 1, replace = True, p = list(weights.values()))[0]

        # This is for making sure that the edge was successfully added to the graph.
        #       Because networkx doesn't add if an edge already exists and it doesn't
        #       give any warning when there is a conflict
        oldEdgeCount = G.number_of_edges()
        G.add_edge(n1, n2, weight = 1)
        newEdgeCount = G.number_of_edges()

        if oldEdgeCount != newEdgeCount:
            increaseRatio = float(mappingRatio) / float(10*(float(i+1))) # i+1 is used to prevent division by 0

            # Increase weights of the chosen nodes
            n_1_original_weight = float(weights[n1])
            n_2_original_weight = float(weights[n2])

            total_reduction = float(float(2) * increaseRatio)
            total_reduction_per_node = float(total_reduction / float(nodeSize - 2))

            for k in range(nodeSize):
                original_weight = float(weights[k])
                G.add_node(k, weight = float(float(original_weight) - float(total_reduction_per_node)))

            G.add_node(n1, weight = float(n_1_original_weight + increaseRatio))
            G.add_node(n2, weight = float(n_2_original_weight + increaseRatio))

            ''''
            print("looping...")
            print("Current i: " + str(i))
            print("Chosen node 1: " + str(n1))
            print("Chosen node 2: " + str(n2))
            print("Node 1 old weight: " + str(n_1_original_weight))
            print("Node 2 old weight: " + str(n_2_original_weight))
            print("Node 1 new weight: " + str(float(n_1_original_weight + increaseRatio)))
            print("Node 2 new weight: " + str(float(n_2_original_weight + increaseRatio)))
            print("Total reduction " + str(total_reduction))
            print("Total reduction per node " + str(total_reduction_per_node))
            #print("Value of the first node " + str(float(weights[1])))
            print("\n")
            '''

            i = i + 1

        else:
            '''
            print("Shit!")
            print("\n")
            '''

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

    #ax.set_xlim([10,50])

    plt.show()


def drawGraph(G):
    if(G == None):
        return None

    plt.figure(1, figsize=(20,10))
    nx.draw_networkx(G, with_labels=True, font_weight='bold')
    plt.show()

# Takes a network grahg and graphs it based on the weights of the edges in the network
def drawWeightedGraph(G):
    if(G == None):
        return None

    # Positions for all nodes
    # Check the following link for options
    #       https://networkx.github.io/documentation/networkx-1.10/reference/drawing.html#module-networkx.drawing.layout
    pos = nx.random_layout(G)

    pos_weight = {}
    for k, v in pos.items():
        pos_weight[k] = (v[0], v[1] + 0.05)

    # Create a figure
    plt.figure(1, figsize=(20,10))
    #plt.margins(50, 50)

    # Iterate through all edges and plot them depending on their weights
    for (u, v, d) in G.edges(data = True):
        edge = [(u, v)]
        nx.draw_networkx_edges(G, pos, edgelist = edge, width = d['weight']*2)

    # Draw nodes and add labes to all nodes
    labels = nx.get_node_attributes(G, 'weight')

    nx.draw_networkx_nodes(G, pos, node_size = np.multiply(labels.values(), float(20000)))
    nx.draw_networkx_labels(G, pos, font_weight='bold')
    #nx.draw_networkx_labels(G, pos_weight, labels = labels, font_weight='bold', font_color = "b")

    #plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
