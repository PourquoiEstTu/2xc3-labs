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
<<<<<<< HEAD
        # null_parent = False
        if self.left == None :
            return
        left_child = self.left 
        right_child = left_child.right
        left_child.right = self 
        self.left = right_child
        self.parent = left_child
        if right_child != None :
            right_child.parent = self
        return left_child
        # if left_child.right != None :
        #     left_child.right.parent = self
        # left_child.parent = self.parent
        # #REMEMBER TO ALSO DEAL WITH THIS IN THE RBTree CLASS
        # if self.parent != None :
        #     if self == self.parent.left :
        #         self.parent.left = left_child
        #     else :
        #         self.parent.right = left_child
        # # else :
        # #     null_parent = True
        # left_child.right = self
        # self.parent = left_child
        # return null_parent
=======
        #do
        return
>>>>>>> parent of 365f1c5... Probably correct rotate_{right,left}, hasnt been tested yet

    def rotate_left(self):
        # null_parent = False
        if self.right == None :
            return
        right_child = self.right
<<<<<<< HEAD
        # print(right_child)
        left_child = right_child.left
=======
        self.right = right_child.left
        if right_child.left != None :
            right_child.left.parent == self.right
        right_child.parent = self.parent
        if self == self.parent.left :
            self.parent.left = right_child
        else :
            self.parent.right = right_child
>>>>>>> parent of 365f1c5... Probably correct rotate_{right,left}, hasnt been tested yet
        right_child.left = self
        self.right = left_child 
        self.parent = right_child
        if left_child != None :
            left_child.parent = self
        return right_child
        # if right_child.left != None :
        #     right_child.left.parent = self
        # right_child.parent = self.parent
        # #REMEMBER TO ALSO DEAL WITH THIS IN THE RBTree CLASS
        # if self.parent != None :
        #     if self == self.parent.left :
        #         self.parent.left = right_child
        #     else :
        #         self.parent.right = right_child
        # # else :
        # #     null_parent = True
        # # print(right_child)
        # right_child.left = self
        # self.parent = right_child
        # return null_parent

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
        # if node.parent.parent == None and node.is_red() and node.get_brother.is_red() :
        #     node.make_black()
        #     node.get_brother.make_black()
        # print(self.get_height==0)
        # print(self)
        # print(node)
        # if self.get_height() == 2 :
        #     if node == node.parent.right and node.parent.left == None :
        #         colour = node.colour
        #         node.colour = node.parent.colour
        #         node.parent.colour = colour
        #         node.parent.rotate_left() 
        #         self.root = node
        #     elif node.parent.left != None and node.parent.right != None :
        #         node.parent.left.make_black()
        #         node.parent.right.make_black()
        while node != None and node.parent != None and node.parent.is_red(): 
            print(self)
            #case of uncle being black
            if node.uncle_is_black() :
                #left left case
                if (node.parent == node.gparent().left) and (node == node.parent.left) : 
                    # node.gparent().rotate_right()
                    # #swap colour of grandparent with parent
                    # colour = node.parent.colour
                    # node.parent.colour = node.gparent().colour
                    # node.gparent().colour = colour

                    node = node.rotate_left()
                    node.make_black()
                    node.left.make_red()
                #left right case 
                elif (node.parent == node.gparent().left) and (node == node.parent.right) :
                    # node.parent.rotate_left()
                    # node.gparent().rotate_right()
                    # colour = node.parent.colour
                    # node.parent.colour = node.gparent().colour
                    # node.gparent().colour = colour

                    node.left = node.rotate_left()
                    node.left.parent = node 
                    node = node.rotate_right()
                    node.right.make_red()
                #right right case
                elif (node.parent == node.gparent().right) and (node == node.parent.right) :
                    #swap colour of grandparent with parent
                    # if node.gparent().rotate_left() :
                    #     self.root = node.parent
                    # colour = node.parent
                    # node.parent.colour = node.gparent().colour
                    # node.gparent().colour = colour

                    node = node.rotate_right()
                    node.make_black()
                    node.right.make_red()
                #right left case
                elif (node.parent == node.gparent().right) and (node == node.parent.left) :
                    # node.parent.rotate_right()
                    # node.gparent().rotate_left()
                    # #swap colour of grandparent with parent
                    # colour = node.parent.colour
                    # node.parent.colour = node.gparent().colour
                    # node.gparent().colour = colour

                    node.right = node.rotate_right()
                    node.right.parent = node
                    node = self.rotate_left()
                    node.make_black()
                    node.left.make_red()
                node = node.parent
            #case of uncle being red
            else :
                node.parent.make_black()
                node.get_uncle().make_black()
                node.parent.parent.make_red()
                node = node.parent.parent
        self.root.make_black()
        
                    
        
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


tree = RBTree()
tree.insert(5)
# tree.insert(4)
tree.insert(10)
tree.insert(11)
# print(tree.get_height())
# tree.insert(12)
# tree.insert(9)
# tree.insert(8)
print(tree)
print(tree.root.right)
