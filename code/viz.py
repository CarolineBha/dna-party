import networkx as nx
import numpy as np

class NetworkView:
    """
    Class for network visualization
    """

    def __init__(self):
        pass

    @staticmethod
    def gen_simple_graph(adjacency_mat):

        G = nx.Graph()
        G.add_nodes_from(np.arange(adjacency_mat.shape[0]))

        for i in range(adjacency_mat.shape[0]):
            for j in range(i):

                if abs(adjacency_mat[i, j]) > 0:
                    G.add_edge(i, j, weight=adjacency_mat[i,j])

        return G