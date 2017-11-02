
class Node(object):
    def __init__(self, name, leaf=False, goal=None):
        self.name = name
        self.children = []
        self.leaf = leaf
        self.goal = goal

    def add_child(self, obj):
        self.children.append(obj)


start = Node("start")
take = Node("take")
move = Node("move")          sdsdsdsdsdasd
the = Node("the")
to = Node("to")
ball = Node("ball", True, "bring(Ball)")
thomas = Node("Thomas", True, "at(Thomas)")

start.add_child(take)
start.add_child(move)
take.add_child(the)
move.add_child(to)
the.add_child(ball)
to.add_child(thomas)



text1 = "take the ball"
text = "move to Thomas"

words = text.split(" ")

currentNode = start

for word in words:
    for children in currentNode.children:
        if word == children.name:
            currentNode = children
            break

if currentNode.leaf:
    print(currentNode.goal)
else:
    raise Exception("No goal reached.")
