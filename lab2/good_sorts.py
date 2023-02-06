"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.

In contains traditional implementations for:
1) Quick sort
2) Merge sort
3) Heap sort

Author: Vincent Maccio
Students: Love you Maccio~
"""

import random
import timeit
import matplotlib.pyplot as plot
import math

# ************ Quick Sort ************
def quicksort(L):
    copy = quicksort_copy(L)
    for i in range(len(L)):
        L[i] = copy[i]


def quicksort_copy(L):
    if len(L) < 2:
        return L
    pivot = L[0]
    left, right = [], []
    for num in L[1:]:
        if num < pivot:
            left.append(num)
        else:
            right.append(num)
    return quicksort_copy(left) + [pivot] + quicksort_copy(right)

# *************************************


# ************ Merge Sort *************

def mergesort(L):
    if len(L) <= 1:
        return
    mid = len(L) // 2
    left, right = L[:mid], L[mid:]

    mergesort(left)
    mergesort(right)
    temp = merge(left, right)

    for i in range(len(temp)):
        L[i] = temp[i]


def merge(left, right):
    L = []
    i = j = 0

    while i < len(left) or j < len(right):
        if i >= len(left):
            L.append(right[j])
            j += 1
        elif j >= len(right):
            L.append(left[i])
            i += 1
        else:
            if left[i] <= right[j]:
                L.append(left[i])
                i += 1
            else:
                L.append(right[j])
                j += 1
    return L

# *************************************

# ************* Heap Sort *************

def heapsort(L):
    heap = Heap(L)
    for _ in range(len(L)):
        heap.extract_max()

class Heap:
    length = 0
    data = []

    def __init__(self, L):
        self.data = L
        self.length = len(L)
        self.build_heap()

    def build_heap(self):
        for i in range(self.length // 2 - 1, -1, -1):
            self.heapify(i)

    def heapify(self, i):
        largest_known = i
        if self.left(i) < self.length and self.data[self.left(i)] > self.data[i]:
            largest_known = self.left(i)
        if self.right(i) < self.length and self.data[self.right(i)] > self.data[largest_known]:
            largest_known = self.right(i)
        if largest_known != i:
            self.data[i], self.data[largest_known] = self.data[largest_known], self.data[i]
            self.heapify(largest_known)

    def insert(self, value):
        if len(self.data) == self.length:
            self.data.append(value)
        else:
            self.data[self.length] = value
        self.length += 1
        self.bubble_up(self.length - 1)

    def insert_values(self, L):
        for num in L:
            self.insert(num)

    def bubble_up(self, i):
        while i > 0 and self.data[i] > self.data[self.parent(i)]:
            self.data[i], self.data[self.parent(i)] = self.data[self.parent(i)], self.data[i]
            i = self.parent(i)

    def extract_max(self):
        self.data[0], self.data[self.length - 1] = self.data[self.length - 1], self.data[0]
        max_value = self.data[self.length - 1]
        self.length -= 1
        self.heapify(0)
        return max_value

    def left(self, i):
        return 2 * (i + 1) - 1

    def right(self, i):
        return 2 * (i + 1)

    def parent(self, i):
        return (i + 1) // 2 - 1

    def __str__(self):
        height = math.ceil(math.log(self.length + 1, 2))
        whitespace = 2 ** height
        s = ""
        for i in range(height):
            for j in range(2 ** i - 1, min(2 ** (i + 1) - 1, self.length)):
                s += " " * whitespace
                s += str(self.data[j]) + " "
            s += "\n"
            whitespace = whitespace // 2
        return s

# *************************************
    
# -------- TESTING CODE ---------------

# I have created this function to make the sorting algorithm code read easier
def swap(L, i, j):
    L[i], L[j] = L[j], L[i]

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

# 1 for the singleton case, 15 b/c for small arrays,
#  quicksort and mergesort have a lot of overhead 
#  (according to 2c03), and then the rest for good 
#  measure
list_lengths = [1, 15, 100, 1000, 10000, 1000000]
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
swapList = [0, 10, 100, 500, 1000, 2500, 5000, 7500, 10000, 50000]
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

# --------------- EXPERIMENT 4 CODE ------------------
# length_vs_time_Test0 = sortingAlgoTiming(10, quicksort)
# length_vs_time_Test1 = sortingAlgoTiming(10, mergesort)
# length_vs_time_Test2 = sortingAlgoTiming(10, heapsort)
# # fig, ax = plot.subplots()
# plot.xlabel("List Length (Number of Elements)")
# plot.ylabel("Time (s)")
# plot.plot(list_lengths, length_vs_time_Test0[1], label = "Quicksort")
# plot.plot(list_lengths, length_vs_time_Test1[1], label = "Mergesort")
# plot.plot(list_lengths, length_vs_time_Test2[1], label = "Heapsort")
# legend = plot.legend(loc="upper center")
# # ax.plot(swapTest1[1], swapTest1[2])
# # ax.plot(swapTest2[1], swapTest2[2])
# plot.title("Sorting Algorithm Time Depending on List Length")
# plot.show()

# --------------- EXPERIMENT 5 CODE ------------------

swapTest0 = sortingAlgoTimingNearSorted(500, quicksort)
swapTest1 = sortingAlgoTimingNearSorted(500, mergesort)
swapTest2 = sortingAlgoTimingNearSorted(500, heapsort)
# fig, ax = plot.subplots()
plot.xlabel("Swaps")
plot.ylabel("Time (s)")
plot.plot(swapTest0[2], swapTest0[1], label = "Quicksort")
plot.plot(swapTest1[2], swapTest1[1], label = "Mergesort")
plot.plot(swapTest2[2], swapTest2[1], label = "Heapsort")
legend = plot.legend(loc="upper center")
# ax.plot(swapTest1[1], swapTest1[2])
# ax.plot(swapTest2[1], swapTest2[2])
plot.title("Sorting Algorithm Time Depending on Swaps in a Near Sorted List")
plot.show()