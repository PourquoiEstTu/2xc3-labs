import min_heap
import random
import math
import timeit
# import matplotlib.pyplot as plot
import csv

class WeightedGraph:
    def __init__(self, n):
        self.adj = {}
        self.weights = {}

    def has_edge(self, node1, node2):
        return node2 in self.adj[node1]

    def add_edge(self, node1, node2, weight):
        if not self.has_edge(node1, node2):
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)
        self.weights[(node1, node2)] = weight
        self.weights[(node2, node1)] = weight

    def get_size(self):
        return len(self.adj)

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
# G.add_node(3)
# G.add_node(4)
# G.add_node(5)
# G.add_edge(0, 1, 10)
# G.add_edge(0, 2, 5)
# G.add_edge(0, 3, 20)
# G.add_edge(2, 3, 10)
# G.add_edge(2, 1, 1)
# G.add_edge(1, 3, 1)
# G.add_edge(0, 1, 10)
# G.add_edge(1, 0, 10)
# G.add_edge(1, 2, 7)
# G.add_edge(2, 1, 7)
# G.add_edge(0, 3, -5)
# G.add_edge(3, 0, -5)
# G.add_edge(3, 1, 5)
# G.add_edge(1, 3, 5)
# G.add_edge(3, 2, 1)
# G.add_edge(2, 3, 1)
# G.add_edge(2, 4, 20)
# G.add_edge(4, 2, 20)
# print(init_d(G))
# print(mystery(G))
# G.add_edge(1, 4, 5)
# G.add_edge(4, 5, 20)
# G.add_edge(3, 5, 10)
# print(dijkstra_approx(G, 0, 2))
# print(bellman_ford_approx(G, 0, 2))

#-------------------------- EXPERIMENT SUITE 1 --------------------------

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
# test = exp1(k_vals, 100, 1)
# plot.xlabel("k value")
# plot.ylabel("Distance of all nodes from source")
# plot.plot(test[1], test[0][0], label="Dijkstra Distance")
# plot.plot(test[1], test[0][1], label="Dijkstra Approx Distance")
# plot.plot(test[1], test[0][2], label="Bellman-Ford Distance")
# plot.plot(test[1], test[0][3], label="Bellman-Ford Approx Distance")
# legend = plot.legend(loc="upper right")
# plot.title("Shortest Path Distances for Graphs of 100 Nodes")
# plot.show()

#EXPERIMENT 2 - AVERAGE DISTANCE WHEN size of graph is varied
#vary number of nodes, fix k, weights of edges, and density 

sizes = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
def exp2(sizes:list, k:int, runs:int) :
    avg_dist_size = [[], [], [], []]
    avg_dijkstra = 0
    avg_dijkstra_approx = 0
    avg_bellman_ford = 0
    avg_bellman_ford_approx = 0
    for s in sizes : 
        for _ in range(runs) :
            G = create_random_complete_graph(s, 100)
            avg_dijkstra = total_dist(dijkstra(G, 0))
            avg_dijkstra_approx = total_dist(dijkstra_approx(G, 0, k))
            avg_bellman_ford = total_dist(bellman_ford(G, 0))
            avg_bellman_ford_approx = total_dist(bellman_ford_approx(G, 0, k))
        avg_dist_size[0].append(avg_dijkstra)
        avg_dist_size[1].append(avg_dijkstra_approx)
        avg_dist_size[2].append(avg_bellman_ford)
        avg_dist_size[3].append(avg_bellman_ford_approx)
    return (avg_dist_size, sizes)

# test1 = exp2(sizes, 2, 10)
# plot.xlabel("Number of Nodes in Graph")
# plot.ylabel("Distance of all nodes from source")
# plot.plot(test1[1], test1[0][0], label="Dijkstra Distance")
# plot.plot(test1[1], test1[0][1], label="Dijkstra Approx Distance")
# plot.plot(test1[1], test1[0][2], label="Bellman-Ford Distance")
# plot.plot(test1[1], test1[0][3], label="Bellman-Ford Approx Distance")
# legend = plot.legend(loc="upper left")
# plot.title("Shortest Path Distances for Graphs of Differing Sizes")
# plot.show()

#EXPERIMENT 3 - AVERAGE DISTANCE WHEN size of graph is varied
#vary number of edges, fix k, weights of edges, and number of nodes 

#new create graph for varying edges
def create_random_graph(n, edges, upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)
    for _ in range(edges):
        node1 = random.randint(0,n-1)
        node2 = random.randint(0,n-1)
        if node1 != node2 :
            G.add_edge(node1, node2, random.randint(1,upper))
        # print(node1)
        # print(node2)
    return G

# edges = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# edges = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
edges = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800,]
def exp3(size:int, k:int, edges:list, runs:int) :
    avg_dist_size = [[], [], [], []]
    avg_dijkstra = 0
    avg_dijkstra_approx = 0
    avg_bellman_ford = 0
    avg_bellman_ford_approx = 0
    for e in edges : 
        for _ in range(runs) :
            G = create_random_graph(size, e, 100)
            avg_dijkstra = total_dist(dijkstra(G, 0))
            avg_dijkstra_approx = total_dist(dijkstra_approx(G, 0, k))
            avg_bellman_ford = total_dist(bellman_ford(G, 0))
            avg_bellman_ford_approx = total_dist(bellman_ford_approx(G, 0, k))
        avg_dist_size[0].append(avg_dijkstra/runs)
        avg_dist_size[1].append(avg_dijkstra_approx/runs)
        avg_dist_size[2].append(avg_bellman_ford/runs)
        avg_dist_size[3].append(avg_bellman_ford_approx/runs)
    return (avg_dist_size, edges)

# G = create_random_graph(100, 10, 30)
# G = create_random_complete_graph(10, 30)
# for i in G.adj : 
#     print(G.adj[i])
# print(G.adj.keys())
# print(5 + G.adj[0])
# test2 = exp3(100, 5, edges, 50)
# plot.xlabel("Number of Edges in Graph")
# plot.ylabel("Distance of all nodes from source")
# plot.plot(test2[1], test2[0][0], label="Dijkstra Distance")
# plot.plot(test2[1], test2[0][1], label="Dijkstra Approx Distance")
# plot.plot(test2[1], test2[0][2], label="Bellman-Ford Distance")
# plot.plot(test2[1], test2[0][3], label="Bellman-Ford Approx Distance")
# legend = plot.legend(loc="upper center")
# plot.title("Shortest Path Distances for Graphs of Differing Sizes")
# plot.show()

#-------------------------- MYSTERY TEST --------------------------

# for i in range(1, 150) :
#     sizes.append(i)
sizes = [1, 3, 9, 27, 81, 243, 365,]# 548,]
def mysteryTest(sizes:list, upper:int, runs:int) :
    time = 0
    time_list = []
    for s in sizes :
        for _ in range(runs) :
            G = create_random_complete_graph(s, upper)
            start = timeit.default_timer()
            mystery(G)
            end = timeit.default_timer()
            time += end - start
        time_list.append(math.log(time/runs, 4))
    for i in range(len(sizes)) :
        sizes[i] = math.log(sizes[i], 3)
    return (time_list, sizes)

# ahhhhh = mysteryTest(sizes, 100, 1)
# plot.xlabel("log of Sizes")
# plot.ylabel("log of Time (s)")
# plot.plot(ahhhhh[1], ahhhhh[0])
# # legend = plot.legend(loc="upper center")
# plot.title("Number of nodes in a graph vs. time it takes to run")
# plot.show()

#------------------------- PART 3 -------------------------
london_stations = DirectedWeightedGraph()
with open("london_stations.csv", "r") as fh : #fh = file_handler (remember this?) 
    station_data = csv.DictReader(fh)
    for row in station_data :
        london_stations.add_node(row["id"])
    # for row in station_data :
    #     print(row["id"])

    with open("london_connections.csv", 'r') as fh2 :
        connections = csv.DictReader(fh2)
        for stations in connections :
            coord1 = (0,0)
            coord2 = (0,0)
            for row in station_data :
                if stations["station1"] == row["id"] :
                    coord1 = (row["latitude"], row["longitude"])
                if stations["station2"] == row["id"] :
                    coord2 = (row["latitude"], row["longitude"])
            london_stations.add_edge(stations["station1"], 
                                        stations["station2"], 
                                        math.sqrt((coord2[0] - coord1[0])^2 + 
                                                  (coord2[1] - coord1[1])^2))
            # print(stations["station1"])
            # print(stations["station2"])
            # print("\n")
for i in london_stations.adj :
    print(i, end=" ")
    print(london_stations.adj[i])
# print(dijkstra(london_stations, 11))