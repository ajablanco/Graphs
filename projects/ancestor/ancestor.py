from graph import Graph
from util import Stack

def earliest_ancestor(ancestors, starting_node):
    g = Graph()

    for ancestor in ancestors:
        if ancestor[0] not in g.vertices:
            g.add_vertex(ancestor[0])
        if ancestor[1] not in g.vertices:
            g.add_vertex(ancestor[1])

        g.add_edge(ancestor[1], ancestor[0])

    s = Stack()
    visited = set()
    s.push([starting_node])
    longest_path = []

    while s.size() > 0:
        path = s.pop()
        # print("path", path)
        current_node = path[-1]
        # print("current", current_node)

        if len(path) > len(longest_path):
            longest_path = path
            # print("path", len(path))
            # print("longest", len(longest_path))


        if current_node not in visited:
            visited.add(current_node)
            parents = g.get_neighbors(current_node)
            print("parents", parents)

            for parent in parents:
                new_path = path+[parent]
                s.push(new_path)
                # print("new_path", new_path)


    if starting_node == longest_path[-1]:
        return -1
    else:
        return longest_path[-1]
