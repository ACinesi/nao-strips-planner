class Node(object):
    def __init__(self, name, leaf=False, goal=None):
        self.name = name
        self.children = []
        self.leaf = leaf
        self.goal = goal

    def add_child(self, obj):
        self.children.append(obj)


dare = Node("dare")
prendere =Node("prendere")
palla = Node("palla", True, "!Bring(Ball)")

dare.add_child(palla)
prendere.add_child(palla)

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
