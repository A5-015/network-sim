

# Takes the total number of nodes that needs to be in the graph, total number of
#       edges that need to be in the graph, and a boolean value for weighting the
#       edges. If weighting flag is set to True, the weight between edges will be
#       calculated with the generateWeight() function. Otherwise, the weights will
#       be assigned uniformly to all edges as 1.
def generateNetwork(nodeSize, edgeBudget, name = "network"):

    # Check if given parameters make sense
    if(edgeBudget > nodeSize*(nodeSize-1)/2):
        print("Provided too many edges, please check the values")
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
            #####################
            ## REWARD FUNCTION ##
            #####################
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
