import random
import matplotlib.pyplot as plot
import timeit

class RBNode:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.colour = "R"

    def get_uncle(self):
        return

    def is_leaf(self):
        return self.left == None and self.right == None

    def is_left_child(self):
        return self == self.parent.left

    def is_right_child(self):
        return not self.is_left_child()

    def is_red(self):
        return self.colour == "R"

    def is_black(self):
        return not self.is_red()

    def make_black(self):
        self.colour = "B"

    def make_red(self):
        self.colour = "R"

    def get_brother(self):
        if self.parent.right == self:
            return self.parent.left
        return self.parent.right

    def get_uncle(self):
        return self.parent.get_brother()

    def uncle_is_black(self):
        if self.get_uncle() == None:
            return True
        return self.get_uncle().is_black()

    def __str__(self):
        return "(" + str(self.value) + "," + self.colour + ")"

    def __repr__(self):
         return "(" + str(self.value) + "," + self.colour + ")"

    def rotate_right(self):
        null_parent = False
        if self.left == None :
            return
        y = self.left 
        self.left = y.right 
        if y.right != None :
            y.right.parent = self
        y.parent = self.parent 
        if self.parent != None :
            if self == self.parent.right :
                self.parent.right = y
            else : 
                self.parent.left = y
        else :
            null_parent = True 
        y.right = self
        self.parent = y
        return (null_parent, y)

    def rotate_left(self):
        null_parent = False
        if self.right == None :
            return
        y = self.right 
        self.right = y.left
        if y.left != None :
            y.left.parent = self 
        y.parent = self.parent
        if self.parent != None :
            if self == self.parent.left :
                self.parent.left = y
            else :
                self.parent.right = y 
        else :
            null_parent = True
        y.left = self 
        self.parent = y
        return (null_parent, y)

    def gparent(self) :
        return self.parent.parent



class RBTree:

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root == None

    def get_height(self):
        if self.is_empty():
            return 0
        return self.__get_height(self.root)

    def __get_height(self, node):
        if node == None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def rotate_left(self, node) :
        if node.right == None :
            return
        y = node.right 
        node.right = y.left
        if y.left != None :
            y.left.parent = node 
        y.parent = node.parent
        if node.parent == None :
            self.root = y
        elif node == node.parent.left :
            node.parent.left = y
        else :
            node.parent.right = y 
        y.left = node 
        node.parent = y
        return y
    
    def rotate_right(self, node) :
        if node.left == None :
            return
        y = node.left 
        node.left = y.right 
        if y.right != None :
            y.right.parent = node 
        y.parent = node.parent 
        if node.parent == None :
            self.root = y
        elif node == node.parent.right :
            node.parent.right = y
        else : 
            node.parent.left = y
        y.right = node 
        node.parent = y
        return y

    #NOT ASSIGNMENT RELEVANT
    # def find(self, value) :
    #     if self.is_empty() :
    #         return False 
    #     else :
    #         self.__find(self.root, value)

    # def __find(self, node, value) :
    #     if value < node.value :
    #         if node.left == None :
    #             return False 
    #         else :
    #             self.__find(node.left, value)
    #     elif value > node.value :
    #         if node.right == None :
    #             return False 
    #         else :
    #             self.__find(node.right, value)
    #     else :
    #         return True

    def insert(self, value):
        if self.is_empty():
            self.root = RBNode(value)
            self.root.make_black()
        else:
            self.__insert(self.root, value)

    def __insert(self, node, value):
        if value < node.value:
            if node.left == None:
                node.left = RBNode(value)
                node.left.parent = node
                self.fix(node.left)
            else:
                self.__insert(node.left, value)
        else:
            if node.right == None:
                node.right = RBNode(value)
                node.right.parent = node
                self.fix(node.right)
            else:
                self.__insert(node.right, value)

    def fix(self, node):
        #You may alter code in this method if you wish, it's merely a guide.
        if node.parent == None:
            node.make_black()
        while node != None and node.parent != None and node.parent.is_red(): 
            # case of uncle being black
            if node.uncle_is_black() :
                #left left case
                if (node.parent == node.gparent().left) and (node == node.parent.left) : 
                    y = self.rotate_right(node.gparent())
                    y.right.colour, y.colour = y.colour, y.right.colour
                #left right case 
                elif (node.parent == node.gparent().left) and (node == node.parent.right) :
                    temp = node
                    x = self.rotate_left(node.parent)
                    y = self.rotate_right(x.parent)
                    y.right.colour, y.colour = y.colour, y.right.colour
                #right right case
                elif (node.parent == node.gparent().right) and (node == node.parent.right) :
                    y = self.rotate_left(node.gparent())
                    y.left.colour, y.colour = y.colour, y.left.colour
                #right left case
                elif (node.parent == node.gparent().right) and (node == node.parent.left) :
                    temp = node
                    x = self.rotate_right(node.parent)
                    y = self.rotate_left(x.parent)
                    y.left.colour, y.colour = y.colour, y.left.colour
                node = node.parent
            # case of uncle being red
            else :
                node.parent.make_black()
                node.get_uncle().make_black()
                node.gparent().make_red()
                node = node.gparent()
        self.root.make_black()
        
    # def left_left_case() : 
        
    def __str__(self):
        if self.is_empty():
            return "[]"
        return "[" + self.__str_helper(self.root) + "]"

    def __str_helper(self, node):
        if node.is_leaf():
            return "[" + str(node) + "]"
        if node.left == None:
            return "[" + str(node) + " -> " + self.__str_helper(node.right) + "]"
        if node.right == None:
            return "[" +  self.__str_helper(node.left) + " <- " + str(node) + "]"
        return "[" + self.__str_helper(node.left) + " <- " + str(node) + " -> " + self.__str_helper(node.right) + "]"


# test code
# tree = RBTree()
# tree.insert(50)
# tree.insert(25)
# tree.insert(12)
# tree.insert(100)
# tree.insert(37)
# tree.insert(43)
# print(tree)
# tree.insert(150)
# print(tree)
# tree.insert(125)
# print(tree)
# tree.insert(41)
# print(tree)
# tree.insert(38)
# print(tree)
# print(tree.get_height())

#test for left right and right left
# tree.insert(20)
# tree.insert(10)
# tree.insert(15)

class Node :
    def __init__(self, value) :
        self.value = value 
        self.left = None
        self.right = None
        self.parent = None
    
    def is_leaf(self) :
        return self.left == None and self.right == None 
    
    def is_left_child(self):
        return self == self.parent.left

    def is_right_child(self):
        return not self.is_left_child()

    def __str__(self):
        return "(" + str(self.value) + ")"

    def __repr__(self):
         return "(" + str(self.value) + ")"

class BST :
    def __init__(self) :
        self.root = None 
    
    def is_empty(self) :
        return self.root == None
    
    def get_height(self):
        if self.is_empty():
            return 0
        return self.__get_height(self.root)

    def __get_height(self, node):
        if node == None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    # def find(self, value) :
    #     if self.is_empty() :
    #         return False 
    #     else :
    #         self.__find(self.root, value)

    # def __find(self, node, value) :
    #     if value < node.value :
    #         if node.left == None :
    #             return False 
    #         else :
    #             self.__find(node.left, value)
    #     elif value > node.value :
    #         if node.right == None :
    #             return False 
    #         else :
    #             self.__find(node.right, value)
    #     else :
    #         return True

    def insert(self, value):
        if self.is_empty():
            self.root = Node(value)
        else:
            self.__insert(self.root, value)

    def __insert(self, node, value):
        if value < node.value:
            if node.left == None:
                node.left = Node(value)
                node.left.parent = node
            else:
                self.__insert(node.left, value)
        else:
            if node.right == None:
                node.right = Node(value)
                node.right.parent = node
            else:
                self.__insert(node.right, value) 

    def __str__(self):
        if self.is_empty():
            return "[]"
        return "[" + self.__str_helper(self.root) + "]"

    def __str_helper(self, node):
        if node.is_leaf():
            return "[" + str(node) + "]"
        if node.left == None:
            return "[" + str(node) + " -> " + self.__str_helper(node.right) + "]"
        if node.right == None:
            return "[" +  self.__str_helper(node.left) + " <- " + str(node) + "]"
        return "[" + self.__str_helper(node.left) + " <- " + str(node) + " -> " + self.__str_helper(node.right) + "]"

#------------------------------ EXPERIMENT 1 ------------------------------

def create_random_list(length, max_value) :
    return [random.randint(0, max_value) for _ in range(length)]

# generate red-black tree
def random_rbt(l) :
    tree = RBTree()
    for i in l :
        # print(i)
        tree.insert(i)
    return tree

# tree = random_rbt(create_random_list(10000, 10000))
# print(tree)

# generate binary search tree
def random_bst(l) :
    tree = BST() 
    for i in l :
        # print(i)
        tree.insert(i)
    return tree

# sanity check
# tree= BST()
# tree1 = RBTree()
# l = create_random_list(20, 9999)
# for i in l :
#     print(i)
#     # tree.insert(i)
#     tree1.insert(i)
# # print(tree)
# print(tree1)


# NOT PART OF ASSIGNMENT
# def time() :
#     avg = 0
#     for _ in range(10) :
#         l = create_random_list(100000, 10000)
#         index = random.randint(0, 100000) 
#         item = l[index]
#         bst = random_bst(l)
#         rbt = random_rbt(l)
#         start1 = timeit.default_timer()
#         rbt.find(item)
#         end1 = timeit.default_timer()
#         rbt_time = end1 - start1

#         start2 = timeit.default_timer()
#         bst.find(item)
#         end2 = timeit.default_timer()
#         bst_time = end2 - start2
#         avg += bst_time - rbt_time
#     return avg/10


# calculate the average height difference between 
#  red black trees and binary search trees
def average_height_diff(list_length, max_val, runs) :
    bst_height = 0
    rbt_height = 0
    for _ in range(runs) :
        l = create_random_list(list_length, max_val)
        bst_height += random_bst(l).get_height()
        rbt_height += random_rbt(l).get_height()

    bst_height /= runs
    rbt_height /= runs
    return (bst_height - rbt_height)

# tuple = average_height_diff(10000, 100000, 100)
# print(tuple)
# print("\n")
# tuple1 = average_height_diff(10000, 10000, 100)
# print(tuple1)
# print("\n")
# tuple2 = average_height_diff(10000, 1000, 100)
# print(tuple2)
# print("\n")
# tuple4 = average_height_diff(10000, 500, 100)
# print(tuple4)
# print("\n")
# tuple6 = average_height_diff(10000, 400, 100)
# print(tuple6)
# print("\n")
# tuple7 = average_height_diff(10000, 300, 100)
# print(tuple7)
# print("\n")
# tuple5 = average_height_diff(10000, 200, 100)
# print(tuple5)
# print("\n")
# tuple3 = average_height_diff(10000, 100, 100)
# print(tuple3)
# print("\n")


# NOT ASSIGNMENT RELEVANT (i think)
# tuple = average_height_diff(100000, 10000, 10)
# tuple = average_height_diff(100000, 1000, 10)
# tuple = average_height_diff(100, 100, 1000)
# tuple = average_height_diff(100, 10, 1000)
# tuple = average_height_diff(100, 50, 1000)
# tuple = average_height_diff(100, 300, 1000)
# tuple = average_height_diff(1000, 1000, 100)
# tuple = average_height_diff(1000, 2000, 100)
# tuple = average_height_diff(1000, 10000, 100)
# tuple = average_height_diff(1000, 200, 100)

#------------------------------ EXPERIMENT 2 ------------------------------
def swap(L, i, j):
    L[i], L[j] = L[j], L[i]

def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L

swap_list = [0, 1, 10, 25, 50, 100, 150, 250, 325, 500, 625, 750, 875, 1000,]
def experiment(list_length, max_value, swap_list, runs) :
    bst_height = 0
    rbt_height = 0
    avg = 0
    avg_diff = []
    for i in swap_list :
        for _ in range(runs) :
            l = create_near_sorted_list(list_length, max_value, i)
            bst_height += random_bst(l).get_height()
            rbt_height += random_rbt(l).get_height()
        bst_height /= runs
        rbt_height /= runs
        avg_diff.append(bst_height - rbt_height)
        bst_height = 0
        rbt_height = 0
    
    return (swap_list, avg_diff)


# test0 = experiment(500, 10000, swap_list, 100)
# test1 = experiment(500, 1000, swap_list, 100)
# test2 = experiment(500, 500, swap_list, 100)
# test3 = experiment(500, 250, swap_list, 100)
# test4 = experiment(500, 100, swap_list, 100)
# fig, ax = plot.subplots()
# plot.xlabel("Number of Swaps")
# plot.ylabel("Height")
# plot.plot(test0[0], test0[1], label = "Max Value of 10 000")
# plot.plot(test1[0], test1[1], label = "Max Value of 1000")
# plot.plot(test2[0], test2[1], label = "Max Value of 500")
# plot.plot(test3[0], test3[1], label = "Max Value of 250")
# plot.plot(test4[0], test4[1], label = "Max Value of 100")
# legend = plot.legend(loc="upper right")
# plot.title("Difference in Height of Depending on Swaps to a Sorted List")
# plot.show()