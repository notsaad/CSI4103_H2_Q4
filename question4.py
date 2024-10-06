'''
Saad Mazhar code for Homework 2, Question 4
CSI 4103: Great Algorithms
Coded with the help of Claude.ai (Anthropic AI model)
'''

import numpy as np
from scipy import linalg
import string

# pasted in from the customized page on andrejs website
edges = [" -+----++--++---", "- -----++--+-+--", "+- ---++++--+---", "--- +-+--+----++", "---+ ++--++-+-++", "----+ --++----++", "--+++- --+---+++", "+++---- ---+++--", "+++--+-- ---++-+", "--+++++-- +-+-++", "----+----+ -+-++", "++-----+--- +---", "+-+-+--+++++ ---", "-+----+++---- --", "---++++--++--- +", "---++++-+++---+ "]

connected_edges = []

# form an adjacency list from the given matrix
for i in range(len(edges)):
    node = chr(ord('A') + i)
    for j in range(len(edges[i])):
        if edges[i][j] == '+':
            endNode = chr(ord('A') + j)
            connection = (node, endNode)
            connected_edges.append(connection)

# these two functions are mainly just used to convert the letters A-P to their numerical mapping 0-15
def letter_to_index(letter):
    return string.ascii_uppercase.index(letter)

def index_to_letter(index):
    return string.ascii_uppercase[index]

def create_adjacency_matrix(edge_list, n):
    """Create an adjacency matrix from a list of edges with letter labels."""
    adj_matrix = np.zeros((n, n))
    for edge in edge_list:
        i, j = map(letter_to_index, edge)
        adj_matrix[i, j] = adj_matrix[j, i] = 1
    return adj_matrix

def spectral_clustering(edge_list, n):
    # Create adjacency matrix from edge list
    adjacency_matrix = create_adjacency_matrix(edge_list, n)

    # Step 1: Compute the Laplacian matrix
    degree_matrix = np.diag(np.sum(adjacency_matrix, axis=1))
    laplacian = degree_matrix - adjacency_matrix

    # Step 2: Find the eigenvectors of the Laplacian matrix
    eigenvalues, eigenvectors = linalg.eigh(laplacian)

    # Step 3: Use the Fiedler vector (second smallest eigenvalue's eigenvector)
    fiedler_vector = eigenvectors[:, 1]

    # Step 4: Cluster the nodes
    cluster1_indices = np.where(fiedler_vector >= 0)[0]
    cluster2_indices = np.where(fiedler_vector < 0)[0]
    
    cluster1 = [index_to_letter(i) for i in cluster1_indices]
    cluster2 = [index_to_letter(i) for i in cluster2_indices]

    # Step 5: Verify the result
    connections_between_clusters = sum(1 for (i, j) in edge_list 
                                       if (i in cluster1 and j in cluster2) or (i in cluster2 and j in cluster1))

    return cluster1, cluster2, connections_between_clusters

# Example usage
def generate_example_edge_list(n=16, connections_between_clusters=8):
    edge_list = []
    nodes = [index_to_letter(i) for i in range(n)]
    
    # Create dense connections within clusters
    for cluster in range(2):
        for i in range(8*cluster, 8*(cluster+1)):
            for j in range(i+1, 8*(cluster+1)):
                if np.random.random() < 0.7:  # 70% chance of connection within cluster
                    edge_list.append((nodes[i], nodes[j]))
    
    # Add connections between clusters
    connections = 0
    while connections < connections_between_clusters:
        i = np.random.randint(0, 8)
        j = np.random.randint(8, 16)
        edge = (nodes[i], nodes[j])
        if edge not in edge_list and (edge[1], edge[0]) not in edge_list:
            edge_list.append(edge)
            connections += 1
    
    return edge_list

# Perform spectral clustering
cluster1, cluster2, connections = spectral_clustering(connected_edges, n=16)

print(f"Cluster 1: {', '.join(sorted(cluster1))}")
print(f"Cluster 2: {', '.join(sorted(cluster2))}")
# divide connections by 2 because this is an undirected graph (friendships always go both ways)
print(f"Connections between clusters: {connections//2}")
