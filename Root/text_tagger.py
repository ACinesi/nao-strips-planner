import treetaggerwrapper
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize


class Node(object):
    def __init__(self, name, leaf=False, goal=None):
        self.name = name
        self.children = []
        self.leaf = leaf
        self.goal = goal

    def add_child(self, obj):
        self.children.append(obj)



def process_text(text):
    """Return the text as list of tagged words removing italian stopwords"""
    text = text.lower()
    tokens = word_tokenize(text)
    filtered_tokens = []
    for token in tokens:
        if not token.isdigit() and not token in stopwords.words('italian'):
            filtered_tokens.append(token)
    appoggio = ""
    result = []
    for x in filtered_tokens:
        appoggio += " " + x
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='it')
    tags = tagger.tag_text(unicode(appoggio))
    tags2 = treetaggerwrapper.make_tags(tags)
    for tag in tags2:
        temp = tag[2]
        result.append(temp)
    return result

def strips_goals(text):
    lemmas = process_text(text)
    print "Tag words ->", lemmas
    root = Node("root")
    dare = Node("restituire")
    prendere = Node("prendere")
    trovare = Node("raggiungere")
    palla = Node("palla", True, "!Bring(ball)")
    palla2 = Node("palla", True, "Bring(ball)")
    enrico = Node("enrico", True, "PersonAt(enrico,B)")
    root.add_child(dare)
    root.add_child(prendere)
    root.add_child(trovare)
    dare.add_child(palla)
    prendere.add_child(palla2)
    trovare.add_child(enrico)
    goals = list()
    currentNode = root
    for word in lemmas:
        for children in currentNode.children:
            if word == children.name:
                if children.leaf:
                    goals.append(children.goal)
                    currentNode = root
                else:
                    currentNode = children
    goals.reverse()#TODO
    temp_goals = ""
    if len(goals) > 0:
        for index, goal in enumerate(goals):
            # print "Goal state->", goal
            if index == 0:
                temp_goals += goal
            else:
                temp_goals += ", " + goal
    else:
        print "No goal reached in the tree."
    return temp_goals

   