import min_heap
import random
import math
import timeit
import matplotlib.pyplot as plot
import csv

class WeightedGraph:
    def __init__(self) :
        self.adj = {}
        self.weights = {}

    def add_edge(self, node1, node2, weight):
        if not self.has_edge(node1, node2):
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)
        self.weights[(node1, node2)] = weight
        self.weights[(node2, node1)] = weight

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def add_node(self, node):
        self.adj[node] = []

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)

    # functions from the graphs.py Graph() implementation from lecture
    def has_edge(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

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

#--------------- PART 1 ----------------

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

#------------------------- PART 2 -------------------------
def a_star(G, s, d, h):
    if (s == d): 
        return ({d:s}, 0)
    elif (G.adj.keys() == {}): return ()
    pred = {} #Predecessor dictionary.
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())
    checked = []

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(s, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min() #pop out element with least distance
        current_node = current_element.value #get the 'value' of the current elm
        if dist[current_node] == float("inf"): dist[current_node] = 0
        if current_node == d: 
            return (pred, dist[d])
        for neighbour in G.adj[current_node]: #for all adjacent nodes
            
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]: #if the distance is better 
                
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour) + h[neighbour]) #change key to better value
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour) #update list
                pred[neighbour] = current_node #update pred
    return (pred) #return pred, and no path since none found

#------------------------- PART 3 -------------------------
# code for creating the graph from the csv files
lines = {} #used to store the lines for each station connection (used in part 3)
london_stations = WeightedGraph()
fh = open("london_stations.csv", 'r')
station_data = csv.DictReader(fh)
station_data_list = [] # so that the data from the csv can be used after the 
                       #  the file gets closed
for row in station_data :
    london_stations.add_node(int(row["id"]))
    station_data_list.append(row)
fh.close()

fh2 = open("london_connections.csv", 'r')
connections = csv.DictReader(fh2)

# stations is a whole row/dict of the london_connections.csv file
for stations in connections :
    coord1 = (0,0)
    coord2 = (0,0) 
    
    lines[int(stations["station1"]), int(stations["station2"])] = int(stations["line"])
    lines[int(stations["station2"]), int(stations["station1"])] = int(stations["line"])

    # searches london_stations.csv for the two stations of the
    #  current iteration that are connected and gets their 
    #  latitude + longitude

    for row in station_data_list :
        # print("huh2")
        if stations["station1"] == row["id"] :
            coord1 = (float(row["latitude"]), float(row["longitude"]))
        if stations["station2"] == row["id"] :
            coord2 = (float(row["latitude"]), float(row["longitude"]))
        # print(coord1)
        # print(coord2)

    # adds the connection b/w the two stations of the current iteration
    # the weight of the edge is the distance b/w the two stations using the 
    #  latitude and longitude as coordinates
    london_stations.add_edge(int(stations["station1"]), 
                                int(stations["station2"]), 
                                math.sqrt((coord2[0] - coord1[0])**2 + 
                                        (coord2[1] - coord1[1])**2) * 100)
# the final value of the weight is multiplied by 100 to make the heuristic 
#  function work better and let it have an acc impact on the algo
fh2.close()

# prints the adjacency list of the graph
#  and the weights for each edge
# for i in london_stations.adj :
#    print(i, end=" : ")
#    print(london_stations.adj[i])
#    for j in london_stations.adj[i] :
#        print(london_stations.w(i, j))

# given a graph and two points in that graph, the function calculates the 
#  straight-line distance (more accurately displacement if yk about physics :smirk:) 
#  b/w two stations
def heuristic(graph:WeightedGraph, source:str, dest:str) :
    src_coord = (0, 0)
    dest_coord = (0, 0)

    # searchs for source and dest id's
    for row in station_data_list :
        # print(row["id"])
        if row["id"] == source :
            src_coord = (row["latitude"], row["longitude"])
        if row["id"] == dest :
            dest_coord = (row["latitude"], row["longitude"])
    
    # just in case error checking
    if src_coord == (0,0) :
        return "The src id you inputted is not assocated with a station id"
    if dest_coord == (0,0) :
        return "The dest id you inputted is not assocated with a station id"
    
    # data in csv is text so have to convert before doing math
    src_coord = (float(src_coord[0]), float(src_coord[1]))
    dest_coord = (float(dest_coord[0]), float(dest_coord[1]))
    distance = math.sqrt((dest_coord[0] - src_coord[0])**2 + 
                            (dest_coord[1] - src_coord[1])**2)
    
    # feel free to edit the return value as needed, the only important part 
    #  of it is that distance*100 is returned
    return {int(source) : distance * 100}

# When you're using this in A* the dest will always be fixed to the destination
#  node you're trying to find the shortest path for

#dijkstra algo to compare with a*
def dijkstra_compare(G, s, d):
    if (s == d or G.adj.keys() == {}): 
        return ({d:s}, [s])
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())
    checked = []

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(s, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min() #pop out element with least distance
        current_node = current_element.value #get the 'value' of the current elm
        if dist[current_node] == float("inf"): dist[current_node] = 0
        dist[current_node] = current_element.key #don't ignore?
        if current_node == d: 
            return (pred, dist[d])
        for neighbour in G.adj[current_node]: #for all adjacent nodes
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]: #if the distance is better 
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour)) #change key to better value
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour) #update list
                pred[neighbour] = current_node #update pred
    return (pred) #return pred, and no path since none found


def createDict(ld, d):
    dict = {}
    for i in london_stations.adj:
        z = heuristic(ld,str(i),str(d))
        dict.update(z)
    return dict

def amountOfLines(path:dict, d):
    total = 0
    past = []
    z = d
    if path == {} or path[d] == d: return 0
    while z in path.keys():
        #print(path[z])
        if lines[path[z], z] not in past:
            total +=1
            past.append(lines[path[z], z])
        z = path[z]
    return total


def part3():
    g = 0
    a_star_dict = []
    dijkstra_dict = []
    for i in london_stations.adj.keys() :
        q = createDict(london_stations, i)
        for p in london_stations.adj.keys():
            start = timeit.default_timer()
            o = a_star(london_stations, p, i, q)
            end = timeit.default_timer()
            start2 = timeit.default_timer()
            k = dijkstra_compare(london_stations, p, i)
            end2 = timeit.default_timer()
            a_star_dict.append((end - start, amountOfLines(o[0], i)))
            dijkstra_dict.append((end2 - start2))
        #print("done") #print statements for progress, not necessary but nice to verify its running
        #print(i) # very useful ^^^^^^^
    return (a_star_dict, dijkstra_dict)

#Printing Our Results

#used in ordering the csv file output
#f = []
#for i in london_stations.adj.keys() :
#    for p in london_stations.adj.keys():
#        f.append((i, p))

#WARNING: This code will take a while to run, so be prepared to wait
#p3 = part3()

#Writing output to csv file
#with open("PathAnalysis.csv", "w", newline='') as file:
#    fo = csv.writer(file)
#    fo.writerow(["Starting Station", "End Station", "A* Algorithm Path Creation Time", "Dijkstra Algorithm Path Creation Time", "Number of Lines used in Path"])
#    for i in range(0, len(f)):
#        fo.writerow([f[i][0], f[i][1], (p3[0][i][0]), (p3[1][i]), (p3[0][i][1])])