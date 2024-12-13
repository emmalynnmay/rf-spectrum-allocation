from radiograph.system import is_not_out_of_range

def add_edge(adj, v, w):
    if w not in adj[v]:
        adj[v].append(w)
    if v not in adj[w]:
        adj[w].append(v)  
    return adj
 
#Time Complexity: O(V^2 + E), in worst case.
#https://www.geeksforgeeks.org/graph-coloring-set-2-greedy-algorithm/
# Assigns colors (starting from 0) to all vertices and prints the assignment of colors
def find_coloring(adj, V):
     
    result = [-1] * V
 
    # Assign the first color to first vertex
    result[0] = 0;
 
    # A temporary array to store the available colors. 
    # True value of available[cr] would mean that the color cr is assigned to one of its adjacent vertices
    available = [False] * V
 
    # Assign colors to remaining V-1 vertices
    for u in range(1, V):
         
        # Process all adjacent vertices and flag their colors as unavailable
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
 
        # Reset the values back to false for the next iteration
        for i in adj[u]:
            if (result[i] != -1):
                available[result[i]] = False

    return (V, result)
 
def allocate_with_coloring(colors, vertices, sim, verbose):

    graph = [[] for _ in range(len(vertices))]
    
    for vert_index in range(len(vertices)):
        for potential_neighbor_index in range(len(vertices)):
            if vertices[vert_index] == vertices[potential_neighbor_index]:
                continue
            if is_not_out_of_range(vertices[vert_index], vertices[potential_neighbor_index], sim):
                graph = add_edge(graph, vert_index, potential_neighbor_index)

    (V, result) = find_coloring(graph, len(vertices))

    num_colors_needed = max(result) + 1

    verts_by_color_index = [[] for _ in range(num_colors_needed)]
    num_of_verts_by_color_index = [0] * num_colors_needed

    if verbose:
        print("Proposed Coloring:")
    for u in range(V):
        if verbose:
            print(" Vertex", vertices[u], f" -> Color: {result[u]}")
        verts_by_color_index[result[u]].append(vertices[u])
        num_of_verts_by_color_index[result[u]] += 1

    if verbose:
        print("Real Coloring:")
    for color_we_have in colors:    
        #Let's assign the next color_we_have to the color_index that has been assigned to the most vertices
        max_number = max(num_of_verts_by_color_index)
        color_index = num_of_verts_by_color_index.index(max_number)

        if color_index == -1:
            #We have successfully assigned all needed colors
            break

        #Remove from the running for the next iterations of the loop
        num_of_verts_by_color_index[color_index] = -1

        for vertex in verts_by_color_index[color_index]:
            if verbose:
                print(" Vertex", vertex, " -> Color", color_we_have.assigned_frequency, f"({color_we_have})")
            color_we_have.grant_frequency(color_we_have.assigned_frequency, vertex)
            vertex.begin_broadcasting(False)

    for leftover_color_index in range(len(num_of_verts_by_color_index)):
        if num_of_verts_by_color_index[leftover_color_index] != -1 and verbose:
            print(f" Not enough colors to cover color {leftover_color_index}. {len(verts_by_color_index[leftover_color_index])} vertices left uncolored.")
