from collections import deque

#Undirected graph using an adjacency list
class Graph:

    def __init__(self, n):
        self.adj = {}
        for i in range(n):
            self.adj[i] = []

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self):
        self.adj[len(self.adj)] = []

    def add_edge(self, node1, node2):
        if node1 not in self.adj[node2]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)

    def number_of_nodes():
        return len()


#Breadth First Search
def BFS(G, node1, node2):
    Q = deque([node1])
    marked = {node1 : True}
    for node in G.adj:
        if node != node1:
            marked[node] = False
    while len(Q) != 0:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node == node2:
                return True
            if not marked[node]:
                Q.append(node)
                marked[node] = True
    return False


#Depth First Search
def DFS(G, node1, node2):
    S = [node1]
    marked = {}
    for node in G.adj:
        marked[node] = False
    while len(S) != 0:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for node in G.adj[current_node]:
                if node == node2:
                    return True
                S.append(node)
    return False

#BFS path return implementation
def BFS2(G, node1, node2):
    Q = deque([node1])
    pathList = []
    appendCount = 0
    marked = {node1 : True}
    for node in G.adj:
        if node != node1:
            marked[node] = False
    while len(Q) != 0:
        current_node = Q.popleft()
        pathList.append(current_node)
        num_of_adj_nodes = len(G.adjacent_nodes(current_node))
        num_of_marks = 0 
        print("Current node: " + str(current_node))
        print("Number of adjacent nodes to current_node: " + str(num_of_adj_nodes))
        for node in G.adj[current_node]:
            if node == node2:
                pathList.append(node2)
                return pathList
            if not marked[node]:
                print("Marked node: " + str(node))
                Q.append(node)
                marked[node] = True
            else :
                num_of_marks += 1
                print("Number of marked nodes: " + str(num_of_marks))
        if num_of_marks == num_of_adj_nodes :
            pathList.pop()

    return []

g = Graph(6)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(2, 3)
g.add_edge(2, 4)
g.add_edge(3, 5)
g.add_edge(3, 4)
g.add_edge(4, 2)
print(BFS2(g, 0, 5))