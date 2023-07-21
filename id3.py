import pandas as pd
import math
import numpy as np

data = pd.read_csv("trainingdata.csv")
features=[feat for feat in data]
features.remove("answer")

class Node:
    def __init__(self):
        self.children=[]
        self.value=""
        self.isLeaf=False
        self.pred=""

    def entropy(self,examples):
        pos=0.0
        neg=0.0
        for _, row in examples.itterrows():
            if row["answer"]=="yes":
                pos+=1
            else:
                neg+=1
        if pos == 0.0 or neg == 0.0:
            return 0.0
        else:
            p=pos/(pos+neg)
            n=neg/(pos+neg)
            return -(p*math.log(p,2)+n*math.log(n,2))
        
    def info_gain(self,examples, attr):
        uniq=np.unique(examples[attr])
        #print("\n",uniq)
        gain=self.entropy(examples)
        #print("\n",gain)
        for u in uniq:
            subdata = examples[examples[attr]==u]
            #print("\n", subdata)
            sub_e=self.entropy(subdata)
            gain-=(float(len(subdata))/float(len(examples)))* sub_e 
            print("\n",gain)
        return gain
    
    def ID3(self, examples, attrs):
        root = Node()
        max_gain = 0
        max_feat = ""
        for feature in attrs:
            #print ("\n",examples)
            gain = self.info_gain(examples, feature)
            if gain > max_gain:
                max_gain = gain
                max_feat = feature
        root.value = max_feat
        #print ("\nMax feature attr",max_feat)
        uniq = np.unique(examples[max_feat])
        #print ("\n",uniq)
        for u in uniq:
            #print ("\n",u)
            subdata = examples[examples[max_feat] == u]
            #print ("\n",subdata)
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
    
    def printTree(self, root:Node, depth=0):
        for i in range(depth):
            print("\t", end="")
        print(root.value, end="")
        if root.isLeaf:
            print(" -> ", root.pred)
        print()
        for child in root.children:
            self.printTree(child, depth + 1)

    def classify(self, root:Node, new):
        for child in root.children:
            if child.value == new[root.value]:
                if child.isLeaf:
                    print ("Predicted Label for new example", new," is:", child.pred)
                    exit
                else:
                    self.classify(child.children[0], new)