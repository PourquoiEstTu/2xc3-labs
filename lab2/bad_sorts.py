"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.
"""
import random
import timeit
import matplotlib.pyplot as plot

# Create a random list length "length" containing whole numbers between 0 and max_value inclusive
def create_random_list(length, max_value):
    return [random.randint(0, max_value) for _ in range(length)]


# Creates a near sorted list by creating a random list, sorting it, then doing a random number of swaps
def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L


# I have created this function to make the sorting algorithm code read easier
def swap(L, i, j):
    L[i], L[j] = L[j], L[i]


# ******************* Insertion sort code *******************

# This is the traditional implementation of Insertion Sort.
def insertion_sort(L):
    for i in range(1, len(L)):
        insert(L, i)


def insert(L, i):
    while i > 0:
        if L[i] < L[i-1]:
            swap(L, i-1, i)
            i -= 1
        else:
            return

def insert_sort_experiment(n, m) : 
    for _ in range(n) :
        times = []
        L = create_random_list(m, m)
        start = timeit.default_timer()
        insertion_sort(L)
        end = timeit.default_timer()
        total = end - start
    return total/n

#print("Test 1: " + str(insert_sort_experiment(1000, 1000)))
#print("Test 2: " + str(insert_sort_experiment(100000, 100000)))

# This is the optimization/improvement we saw in lecture
def insertion_sort2(L):
    for i in range(1, len(L)):
        insert2(L, i)


def insert2(L, i):
    value = L[i]
    while i > 0:
        if L[i - 1] > value:
            L[i] = L[i - 1]
            i -= 1
        else:
            L[i] = value
            return
    L[0] = value


# ******************* Bubble sort code *******************

# Traditional Bubble sort
def bubble_sort(L):
    for i in range(len(L)):
        for j in range(len(L) - 1):
            if L[j] > L[j+1]:
                swap(L, j, j+1)

def bubble_sort1(l,n):
    times = []
    for _ in range(n):
        L = create_random_list(l, l)
        start = timeit.default_timer()
        bubble_sort(L)
        end = timeit.default_timer() 
        total = end-start
        times.append(total)
    return (total/n, times)

#print("Test 1:" + str(bubble_sort1(100,100)[0]))
#print("Test 2:" + str(bubble_sort1(1000,1000)[0]))
#print("Test 3:" + str(bubble_sort1(10000,10000)[0]))

# ******************* Selection sort code *******************

# Traditional Selection sort
def selection_sort(L):
    for i in range(len(L)):
        min_index = find_min_index(L, i)
        swap(L, i, min_index)


def find_min_index(L, n):
    min_index = n
    for i in range(n+1, len(L)):
        if L[i] < L[min_index]:
            min_index = i
    return min_index

def selection_sort_timing(n, m):
    total = 0
    for i in range(n):
        list = create_random_list(m, m)
        start = timeit.default_timer()
        selection_sort(list)
        total += timeit.default_timer() - start
    return total/n

def selection_sort_timing_graph(n, m):
    total = []
    for i in range(n):
        list = create_random_list(m, m)
        start = timeit.default_timer()
        selection_sort(list)
        total.append(timeit.default_timer() - start)
    return total

#times = selection_sort_timing_graph(30, 30)
#plot.plot(times)
#plot.show()

<<<<<<< HEAD
=======
#bubblesort tests plot
bbsort_times1 = bubble_sort1(100,100)[1]
bbsort_times2 = bubble_sort1(500,500)[1]
#bbsort_times3 = bubble_sort1(10000,10000)[1]

plot.plot(bbsort_times1)
plot.plot(bbsort_times2)
plot.show()
>>>>>>> 2bc17bc16589907c1c7dfe439ca351079aca0a8f
