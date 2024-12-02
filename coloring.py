# Python3 program to implement greedy 
# algorithm for graph coloring 
from radiograph.system import is_not_out_of_range

def addEdge(adj, v, w):
     
    if w not in adj[v]:
        adj[v].append(w)
    if v not in adj[w]:
        adj[w].append(v)  
    return adj
 
# Assigns colors (starting from 0) to all
# vertices and prints the assignment of colors
def greedyColoring(adj, V):
     
    result = [-1] * V
 
    # Assign the first color to first vertex
    result[0] = 0;
 
    # A temporary array to store the available colors. 
    # True value of available[cr] would mean that the
    # color cr is assigned to one of its adjacent vertices
    available = [False] * V
 
    # Assign colors to remaining V-1 vertices
    for u in range(1, V):
         
        # Process all adjacent vertices and
        # flag their colors as unavailable
        for i in adj[u]:
            if (result[i] != -1):
                available[result[i]] = True
 
        # Find the first available color
        cr = 0
        while cr < V:
            if (available[cr] == False):
                break
            cr += 1
             
        # Assign the found color
        result[u] = cr 
 
        # Reset the values back to false 
        # for the next iteration
        for i in adj[u]:
            if (result[i] != -1):
                available[result[i]] = False

    return (V, result)
 
def allocate_with_coloring(colors, vertices):

    graph = [[] for i in range(len(vertices))]
    
    for vert_index in range(len(vertices)):
        for potential_neighbor_index in range(len(vertices)):
            if vertices[vert_index] == vertices[potential_neighbor_index]:
                continue
            if is_not_out_of_range(vertices[vert_index], vertices[potential_neighbor_index]):
                graph = addEdge(graph, vert_index, potential_neighbor_index)

    #print(graph)
    (V, result) = greedyColoring(graph, len(vertices))
    for u in range(V):
        print("Vertex", vertices[u], " -> Color", colors[result[u]].assigned_frequency, f"({colors[result[u]]})")
        colors[result[u]].grant_frequency(colors[result[u]].assigned_frequency, vertices[u])
        vertices[u].begin_broadcasting()

# Driver Code
if __name__ == '__main__':
     
    g1 = [[] for i in range(5)]
    g1 = addEdge(g1, 0, 1)
    g1 = addEdge(g1, 0, 2)
    g1 = addEdge(g1, 1, 2)
    g1 = addEdge(g1, 1, 3)
    g1 = addEdge(g1, 2, 3)
    g1 = addEdge(g1, 3, 4)
    print("Coloring of graph 1 ")
    greedyColoring(g1, 5)


#Time Complexity: O(V^2 + E), in worst case.
#Auxiliary Space: O(1), as we are not using any extra space.
#https://www.geeksforgeeks.org/graph-coloring-set-2-greedy-algorithm/