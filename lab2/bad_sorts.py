"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.
"""
from math import floor
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

# improved bubble sort
def bubble_sort2(L) :
    value_i = L[0]
    for i in range(len(L)) :
        value_i = L[0]
        for j in range(len(L) - 1) :
            #print(L)
            #print(value_i)
            # print(value_i > L[j+1])
            # print(j == len(L) - 2)
            # print(j == len(L) - 1)
            if value_i > L[j+1] :
                L[j] = L[j+1]
            else :
                L[j] = value_i
                value_i = L[j+1]
            if j == len(L) - 2 :
                L[len(L) - 1] = value_i

# rand_list_original = create_random_list(20, 30)
# rand_list_to_be_sorted = rand_list_original.copy()
# bubblesort2(rand_list_to_be_sorted)
# print("Sorted rand list:")
# print(rand_list_to_be_sorted)
# print("Original rand list:")
# print(rand_list_original)


# testing function for traditional
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

# helper/auxilliary function for selection_sort
def find_min_index(L, n):
    min_index = n
    for i in range(n+1, len(L)):
        if L[i] < L[min_index]:
            min_index = i
    return min_index

#improved selection sort code for Experiment 2 
def improved_selection_sort(L):
    for i in range(floor(len(L)/2)):
        minman_index = find_max_min_index(L, i)#get min
        if (L[i] != L[minman_index[0]]): swap(L, i, minman_index[0])#swap min value
        if (L[i] != L[minman_index[1]]): swap(L, len(L) - i - 1, minman_index[1])#swap max value

#aux function for improved select sort
def find_max_min_index(L, n):
    max_index = len(L) - n - 1
    min_index = n
    for i in range(n, len(L) - n):
        if L[i] > L[max_index]:
            max_index = i
        if L[i] < L[min_index]:
            min_index = i
    return (min_index, max_index)

# generic testing function that can test any sort and 
#  returns a tuple with both the list needed for the graph
#  (times) and the total time (total)

# USE THIS FUNCTION FOR TESTING AND GET RID OF THE OTHER 
#  ONES LATER
list_lengths = [1, 15, 100, 500, 1000, 2500, 5000, 7500, 10000]
def sortingAlgoTiming(n, func):
    times = []
    total = 0
    for i in list_lengths :
        for j in range(n) :
            list = create_random_list(i, i)
            start = timeit.default_timer()
            func(list)
            end = timeit.default_timer() 
            total += end - start
        times.append(total/n)
    return (total/n, times)

# generic testing function using a near sorted
#  list instead 
swapList = [100, 500, 1000, 5000, 10000, 50000]
def sortingAlgoTimingNearSorted(m, func):
    times = []
    total = 0
    swaps = []
    for i in swapList:
        list = create_near_sorted_list(m, m, i)
        start = timeit.default_timer()
        func(list)
        end = timeit.default_timer() 
        total += end - start
        times.append(end - start)
        swaps.append(i)
    return (total, times, swaps)

# ------- CODE FOR EXPERIMENT 1 TESTS ----------------
# lengthTest0 = sortingAlgoTiming(1, bubble_sort)
# lengthTest1 = sortingAlgoTiming(1, selection_sort)
# lengthTest2 = sortingAlgoTiming(1, insertion_sort)
# fig, ax = plot.subplots()
# plot.xlabel("Length")
# plot.ylabel("Time (s)")
# plot.plot(list_lengths, lengthTest0[1], label = "Bubble Sort")
# plot.plot(list_lengths, lengthTest1[1], label = "Selection Sort")
# plot.plot(list_lengths, lengthTest2[1], label = "Insertion Sort")
# legend = plot.legend(loc="upper center")
# plot.title("Sorting Algorithm Time Depending on List Length")
# plot.show()

#================== CODE FOREXPERIMENT 2 =========================
# ---------------- SELECTION SORT GRAPH
# newSelection = sortingAlgoTiming(10, improved_selection_sort)[1]
# oldSelection = sortingAlgoTiming(10, selection_sort)[1]

# plot.xlabel("Length")
# plot.ylabel("Time (s)")
# plot.plot(list_lengths, newSelection, label = "Improved Selection Sort")
# plot.plot(list_lengths, oldSelection, label = "Traditonal Selection Sort")
# plot.title("Sorting Algorithm Time Depending on List Length")
# legend = plot.legend(loc = "upper center")
# plot.show()

#------------------ BUBBLESORT GRAPH --------------------------
# lengthTest0 = sortingAlgoTiming(1, bubble_sort)
# lengthTest1 = sortingAlgoTiming(1, bubble_sort2)
# fig, ax = plot.subplots()
# plot.xlabel("Length")
# plot.ylabel("Time (s)")
# plot.plot(list_lengths, lengthTest0[1], label = "Traditional Bubble Sort")
# plot.plot(list_lengths, lengthTest1[1], label = "Improved Bubble Sort")
# legend = plot.legend(loc="upper center")
# plot.title("Sorting Algorithm Time Depending on List Length")
# plot.show()

# --------------PLOT/CODE FOR EXPERIMENT 3 ------------
# swapTest0_0 = sortingAlgoTimingNearSorted(5000, insertion_sort)
# swapTest1 = sortingAlgoTimingNearSorted(5000, selection_sort)
# swapTest2 = sortingAlgoTimingNearSorted(5000, bubble_sort)
# plot.xlabel("Swaps")
# plot.ylabel("Time (s)")
# plot.plot(swapTest0_0[2], swapTest0_0[1], label = "Insertion Sort")
# plot.plot(swapTest1[2], swapTest1[1], label = "Selection Sort")
# plot.plot(swapTest2[2], swapTest2[1], label = "Bubble Sort")
# legend = plot.legend(loc="upper center")
# plot.title("Sorting Algorithm Time Depending on Swaps in a Near Sorted List")
# plot.show()