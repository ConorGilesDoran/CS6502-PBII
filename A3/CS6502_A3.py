# CS6502 Assignment 3
# Conor Giles-Doran
# 121105743
# 14/04/2022

class Graph:

    ### This class defines undirected graphs ###

    def __init__(self, gr_dict):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary is used
        """
        if gr_dict == None:
            gr_dict = {}

        self.__gr_dict = gr_dict

    def vertices(self):
        """ returns a list of the vertices of the graph """
        return list(self.__gr_dict.keys())

    def edges(self):
        """ returns the list of the edges (= 2-sets) of a graph """
        return self.__list_edges()

    def add_vertex(self, vertex):
        """If the vertex passed by the argument vertex is not in the dictionary
           self.__graph_dict a key "vertex" with empty-list value
        is added to the dictionary. Otherwise, the vertex is already in the
           graph and nothing is done."""
        if vertex not in self.__gr_dict:
            self.__gr_dict[vertex] = []

    def __list_edges(self):
        """ This method produces the edges of the
            graph. Edges are represented as sets {k}
            with a single vertex x (a loop on the vertex k), where we
            recall that sets never represent duplicat elements, or two
            vertices {k,l}.
        """
        edges = []
        for vertex in self.__gr_dict:
            for neighbour in self.__gr_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def count_nodes(self):
        """ A method that counts the number of nodes in the graph by
            getting the length of the list of dictionary values.
        """
        return len(self.__gr_dict.values())

    def remove_node(self, vertex):
        """ A method that removes a specified node from the graph and
            all edges asscoiated with this node.
        """
        # delete the dictionary item
        if vertex in self.__gr_dict:
            del self.__gr_dict[vertex]

        # remove from any dictionary item's values
        for v in self.__gr_dict.values():
            if vertex in v:
                v.remove(vertex)

    def add_edge(self, edge):
        """ Here we use two-element sets for the edges as we are working with
            an undericted graph.
        """
        x = tuple(edge)
        vertex1 = x[0]
        vertex2 = x[1]
        if vertex1 in self.__gr_dict:
            self.__gr_dict[vertex1].append(vertex2)
        else:
            self.__gr_dict[vertex1] = [vertex2]
        if vertex2 in self.__gr_dict:
            self.__gr_dict[vertex2].append(vertex1)
        else:
            self.__gr_dict[vertex2] = [vertex1]

    def remove_edge(self, edge):
        """ Removes a specified edge from the graph """
        x = tuple(edge)
        vertex1 = x[0]
        vertex2 = x[1]
        # remove edge nodes from each node's set of neighbours
        self.__gr_dict[vertex1].remove(vertex2)
        self.__gr_dict[vertex2].remove(vertex1)

    def __build_shortest_path(self, source, sink, path=[]):
        """ A method that finds the shortest path between two vertices in an undirected graph
            * CODE ADAPTED FROM LECTURE 11 c) GRAPH IMPLEMENTATION *
        """
        path = path + [source]
        if source not in self.__gr_dict:
            return None
        if source == sink:
            return path
        shortest = None
        for vertex in self.__gr_dict[source]:
            if vertex not in path:
                extra_part_path = self.__build_shortest_path(vertex, sink, path)
                if extra_part_path:
                    if (not shortest) or (len(extra_part_path) < len(shortest)):
                        shortest = extra_part_path
        return shortest

    def __Eulerian(self):
        """A method that checks for a graph whether an Eulerian walk is possible.
           A Eulerian walk is possible in a graph if and only if the graph
           is connected and has exactly zero or two nodes of odd degree.
           A graph is connected if a path exists between any one point and any other point in the graph.
           To check this, we can make use of the __build_shortest_path method above.
        """
        # Make list of all possible paths in the graph.
        possible_paths = []
        # Keep track of how many nodes are off odd degree.
        odd_degrees = 0

        for node1 in self.__gr_dict.keys():
            # degree = number of neighbours
            degree = len(self.__gr_dict[node1])

            if degree % 2 != 0:
                # check if degree is odd
                # is so, add 1 to counter
                odd_degrees += 1

            for node2 in self.__gr_dict.keys():
                # if the first and second node are not equal and either combination not in path list already.
                if node1 != node2 and [node1, node2] and [node2, node1] not in possible_paths:
                    # create possible path and append to list
                    path = [node1, node2]
                    possible_paths.append(path)

        # if there are not exactly 0 or 2 nodes of odd degree
        if odd_degrees not in [0, 2]:
            return 'Better stay put where you are now!”'
        else:
            # check if the graph is connected using __build_shortest_path method
            for path in possible_paths:
                if self.__build_shortest_path(path[0], path[1]) is None:
                    return 'Better stay put where you are now!”'
                else:
                    # continue if all paths are possible
                    continue
            # if all above is satisfactory, an Eulerian walk is possible
            return "Enjoy your walk!"

    def is_Eulerian(self):
        """ Function for implementing the __Eulerian() method:
            checks for a graph whether an Eulerian walk is possible."""
        return self.__Eulerian()

    def get_neighbours(self, node, depth=3, output ='all'):
        """A method that starting from a given node returns: the list consisting of the
            neighbors of the node (if any), the neighbors of their neighbors (if any) and the
            neighbors of their neighbors (if any)."""

        all_neighbours = []
        i = depth
        while i > 0:

            neighbours = []
            for neighbour in node:
                for n in neighbour:
                    if self.__gr_dict[n] is not None:
                        neighbours.append(self.__gr_dict[n])
            all_neighbours.append(neighbours)
            node = neighbours
            i -= 1

        # NOTE: if it is just the list of neighbours' neighbours' neighbours' (i.e. the last loop)
        # and not a list contianing all 3 sets of neighbours, then this can be specified by the 'output' parameter
        # I was unsure from the question which was required, so both options are included.
        if output == 'all':
            return all_neighbours
        elif output == 'last':
            return all_neighbours[depth-1]

    # Function for getting a more readable display of each list neighbours as a dictionary.
    # Included as an alternative, but commented out as it does not return a list as specified in question.
    #def get_neighbours(self, node, depth):
        #n_details = {}
        #for i in range(depth):
            #neighbours = []
            #for neighbour in node:
                #for n in neighbour:
                    #if self.__gr_dict[n] is not None:
                        #neighbours.append(self.__gr_dict[n])
            #n_details['neighbours x' + str(i + 1)] = neighbours
            #node = neighbours
        #return n_details


### Implementation ###
if __name__ == "__main__":

    # Dictionary representing a graph.
    gr = { "x" : ["z", "u", "a"],
          "y" : ["z", "u", "a"],
          "z" : ["x", "y"],
          "u" : ["x", "y"],
          "v" : ["w", "a"],
          "w" : ["v"],
          "a" : ["x", "y", "v"]
        }

    # Make into a graph object.
    graph = Graph(gr)

    ### Using new class methods ###

    # Count nodes.
    graph.count_nodes()

    # Check if an Eulerian walk is possible.
    graph.is_Eulerian()

    # list vertices and edges prior to removing
    print(graph.vertices())
    print(graph.edges())

    # Removing a node
    graph.remove_node('u')

    # Can see it has been removed from the graph, along with its associated edges.
    print(graph.vertices())
    print(graph.edges())

    # Remove an edge
    graph.remove_edge({'y', 'z'})

    # Can see the edge has been removed from graph
    print(graph.__dict__)
    print(graph.edges())

    # Extracting the neighbours of 'a', the neighbours of those neighbours, and the neighbours of those neighbours
    # depth is therefore = 3, output = 'all
    graph.get_neighbours('a', depth=3, output='all')

    # Just extracting the neighbours' neighbours' neighbours' (i.e. the last set of neighbours)
    # depth is therefore = 3, output = 'last'
    graph.get_neighbours('a', depth=3, output='last')




