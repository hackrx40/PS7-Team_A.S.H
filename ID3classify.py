import pandas as pd
import math
import numpy as np

data = pd.read_csv("mockdata.csv")
features = ['location', 'age']  # Modify the features list

class Node:
    # ... (rest of the Node class remains the same)
    

    def info_gain(self, examples, attr):
        # ... (rest of the info_gain method remains the same)

    def ID3(self, examples, attrs):
        root = Node()
        max_gain = 0
        max_feat = ""
        for feature in attrs:
            gain = self.info_gain(examples, feature)
            if gain > max_gain:
                max_gain = gain
                max_feat = feature
        root.value = max_feat
        uniq = np.unique(examples[max_feat])
        for u in uniq:
            subdata = examples[examples[max_feat] == u]
            if self.entropy(subdata) == 0.0:
                newNode = Node()
                newNode.isLeaf = True
                newNode.value = u
                newNode.pred = np.unique(subdata["answer"])
                root.children.append(newNode)
            else:
                dummyNode = Node()
                dummyNode.value = u
                new_attrs = attrs.copy()
                new_attrs.remove(max_feat)
                child = self.ID3(subdata, new_attrs)
                dummyNode.children.append(child)
                root.children.append(dummyNode)

        return root

    def printTree(self, root: Node, depth=0):
        # ... (rest of the printTree method remains the same)

    def classify(self, root: Node, new):
        loc = new['location']
        age = new['age']
        for child in root.children:
            if child.value == loc:
                if child.isLeaf:
                    pred = child.pred[0]  # Assuming only one unique prediction for each leaf
                    print("Predicted Label for new example (Location: {}, Age: {}) is: {}".format(loc, age, pred))
                    return
                else:
                    self.classify(child.children[0], new)

# Create the Decision Tree and print the tree
root_node = Node()
root_node = root_node.ID3(data, features)
root_node.printTree(root_node)

# Classify new examples
new_example1 = {'location': 'CityA', 'age': 25}
root_node.classify(root_node, new_example1)

new_example2 = {'location': 'CityB', 'age': 40}
root_node.classify(root_node, new_example2)
