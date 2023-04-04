import min_heap
import random
import matplotlib.pyplot as plot

class DirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)


def dijkstra(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(source, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
    return dist


def bellman_ford(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    nodes = list(G.adj.keys())

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
    return dist


def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total

def create_random_complete_graph(n,upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i,j,random.randint(1,upper))
    return G


#Assumes G represents its nodes as integers 0,1,...,(n-1)
def mystery(G):
    n = G.number_of_nodes()
    d = init_d(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]: 
                    d[i][j] = d[i][k] + d[k][j]
    return d

def init_d(G):
    n = G.number_of_nodes()
    d = [[float("inf") for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if G.are_connected(i, j):
                d[i][j] = G.w(i, j)
        d[i][i] = 0
    return d

#--------------- PART 1 BEGINS :worry: ----------------

# uhhhh prolly works? not much testing done 
def dijkstra_approx(G, source, k) :
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())
    relaxes = {}

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
        relaxes[node] = k
    Q.decrease_key(source, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                if relaxes[neighbour] > 0 :
                    Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                    dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                    pred[neighbour] = current_node
                    relaxes[neighbour] -= 1
    return dist

def bellman_ford_approx(G, source, k) :
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    nodes = list(G.adj.keys())
    relaxes = {}

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
        relaxes[node] = k
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                    if dist[neighbour] > dist[node] + G.w(node, neighbour):
                        if relaxes[neighbour] > 0 :
                            dist[neighbour] = dist[node] + G.w(node, neighbour)
                            pred[neighbour] = node
                            relaxes[neighbour] -= 1
    return dist
# G = DirectedWeightedGraph()
# G.add_node(0)
# G.add_node(1)
# G.add_node(2)
# G.add_node(4)
# G.add_node(5)
# G.add_node(3)
# G.add_edge(0, 1, 10)
# G.add_edge(0, 2, 5)
# G.add_edge(0, 3, 20)
# G.add_edge(2, 3, 10)
# G.add_edge(1, 4, 5)
# G.add_edge(4, 5, 20)
# G.add_edge(3, 5, 10)
# print(dijkstra_approx(G, 0, 2))
# print(bellman_ford_approx(G, 0, 2))

# EXPERIMENT SUITE 1

#EXPERIMENT 1 - AVERAGE DISTANCE WHEN K IS VARIED
# (track which function gives the shortest or longest distance on average)
#vary k, keep num of nodes, weights of edges, and density constant

k_vals = [0, 1, 2, 3, 4, 5, 6,7,8,9,10,11,12,13,14,15]

def exp1(k_vals:list, size:int, runs:int) :
    avg_dist_size = [[], [], [], []]
    avg_dijkstra = 0
    avg_dijkstra_approx = 0
    avg_bellman_ford = 0
    avg_bellman_ford_approx = 0
    for k in k_vals : 
        for _ in range(runs) :
            G = create_random_complete_graph(size, 100)
            avg_dijkstra = total_dist(dijkstra(G, 0))
            avg_dijkstra_approx = total_dist(dijkstra_approx(G, 0, k))
            avg_bellman_ford = total_dist(bellman_ford(G, 0))
            avg_bellman_ford_approx = total_dist(bellman_ford_approx(G, 0, k))
        avg_dist_size[0].append(avg_dijkstra)
        avg_dist_size[1].append(avg_dijkstra_approx)
        avg_dist_size[2].append(avg_bellman_ford)
        avg_dist_size[3].append(avg_bellman_ford_approx)
    return (avg_dist_size, k_vals)

# test1 = t2exp1(edges1, 1000)
test = exp1(k_vals, 100, 1)
plot.xlabel("k value")
plot.ylabel("Distance of all nodes from source")
plot.plot(test[1], test[0][0], label="Dijkstra Distance")
plot.plot(test[1], test[0][1], label="Dijkstra Approx Distance")
plot.plot(test[1], test[0][2], label="Bellman-Ford Distance")
plot.plot(test[1], test[0][3], label="Bellman-Ford Approx Distance")
legend = plot.legend(loc="upper right")
plot.title("Shortest Path Distances for Graphs of 100 Nodes")
plot.show()