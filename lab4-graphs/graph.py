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
        print(current_node)
        if not marked[current_node]:
            marked[current_node] = True
            for node in G.adj[current_node]:
                if node == node2:
                    #print(marked)
                    return True
                S.append(node)
    #print(marked)
    return False

#Depth first search path return
def DFS2(G, node1, node2):
    S = [node1]
    marked = {}
    path = []
    counter = -1
    found = False
    for node in G.adj:
        marked[node] = False #initialize marked dictionary to false 
    while len(S) != 0:
        #print(S)
        #print(marked)
        current_node = S.pop() #take/remove last element of S
        #print(current_node)
        #print(path)
        #print(" ")
        if not marked[current_node]: #check element if not marked
            marked[current_node] = True #mark element
            path.append(current_node)
            for node in G.adj[current_node]: #for each node adjacent to current_node
                if node == node2: #check if correct node found
                    path.append(node)
                    #print(S)
                    if path[0] != node1: return [node1] + path
                    else: return path
                if (not marked[node]): 
                    counter += 1
                    S.append(node) #add adjancent nodes to S 
                    found = True
            if not found and len(S) != 0: 
                for x in range(0, counter):
                    path.remove(path[len(path) - 1])
            found = False
    #print(marked)
    return []

#BFS path return implementation
def BFS2(G, node1, node2):
    Q = deque([node1])
    pathList = []
    breakVar = False
    marked = {node1 : True}
    for node in G.adj:
        if node != node1:
            marked[node] = False
    while len(Q) != 0:
        current_node = Q.popleft()
        pathList.append(current_node)
        num_of_adj_nodes = len(G.adjacent_nodes(current_node))
        num_of_marks = 0 
        # print("Current node: " + str(current_node))
        # print("Number of adjacent nodes to current_node: " + str(num_of_adj_nodes))
        for node in G.adj[current_node]:
            if node == node2:
                pathList.append(node2)
                breakVar = True
                break 
            if not marked[node]:
                # print("Marked node: " + str(node))
                Q.append(node)
                marked[node] = True
        if breakVar :
            break
        # print(pathList)
    if pathList[len(pathList) - 1] != node2 :
        return []
    for i in range(1, len(pathList) - 2) :
        # print(pathList[i])
        if (pathList[i - 1] not in G.adjacent_nodes(pathList[i])) or (pathList[i+1] not in G.adjacent_nodes(pathList[i])) :
            # print(pathList[i])
            pathList.pop(i)

    return pathList


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
print(DFS2(g, 0, 5))

o = Graph(6)
o.add_edge(0, 1)
o.add_edge(0, 2)
o.add_edge(0, 3)
o.add_edge(2, 4)
o.add_edge(2, 5)
o.add_edge(3, 5)
print(BFS2(o, 0, 0))
print(DFS2(o, 0, 0))


#uncomplete
def BFS3(G, node1, node2):
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