import random

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
                    # temp1 = node.gparent()
                    # temp2 = node.parent
                    y = self.rotate_right(node.gparent())
                    y.right.colour, y.colour = y.colour, y.right.colour
                    # temp1.colour, temp2.colour = temp2.colour, temp1.colour
                #left right case 
                elif (node.parent == node.gparent().left) and (node == node.parent.right) :
                    temp = node
                    x = self.rotate_left(node.parent)
                    #left left case is reused here
                    # temp1 = node.gparent()
                    # temp2 = node.parent
                    y = self.rotate_right(x.parent)
                    y.right.colour, y.colour = y.colour, y.right.colour
                    # temp1.colour, temp2.colour = temp2.colour, temp1.colour
                    # node = temp2.left
                    # continue
                #right right case
                elif (node.parent == node.gparent().right) and (node == node.parent.right) :
                    # temp1 = node.gparent()
                    # temp2 = node.parent
                    y = self.rotate_left(node.gparent())
                    # temp1.colour, temp2.colour = temp2.colour, temp1.colour
                    y.left.colour, y.colour = y.colour, y.left.colour
                #right left case
                elif (node.parent == node.gparent().right) and (node == node.parent.left) :
                    temp = node
                    x = self.rotate_right(node.parent)
                    # print(x)
                    #right right case is resued here 
                    # temp1 = node.gparent()
                    # temp2 = node.parent
                    y = self.rotate_left(x.parent)
                    # print(y)
                    y.left.colour, y.colour = y.colour, y.left.colour
                    # temp1.colour, temp2.colour = temp2.colour, temp1.colour
                    # node = temp2.right
                    # continue
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

# generate random red-black tree
def random_rbt(list_length, max_value) :
    tree = RBTree()
    l = create_random_list(list_length, max_value)
    for i in l :
        # print(i)
        tree.insert(i)
    return tree

# tree = random_rbt(10, 100)
# print(tree)

# generate random binary search tree
def random_bst(list_length, max_value) :
    tree = BST() 
    l = create_random_list(list_length, max_value)
    for i in l :
        print(i)
        tree.insert(i)
    return tree

tree = random_bst(10, 100)
print(tree)
