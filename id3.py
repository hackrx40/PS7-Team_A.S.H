import pandas as pd
import math
import numpy as np

data = pd.read.read_csv()
features=[feat for feat in data]
features.remove("answer")

class Node:
    def __init__(self):
        self.children=[]
        self.value=""
        self.isLeaf=False
        self.pred=""

    def entropy(examples):
        pos=0.0
        neg=0.0
        for _, row in examples.itterrows():
            if row["answer"]=="yes":
                pos+=1
            else:
                neg+=1
        if pos = 0.0 or neg = 0.0:
            return 0.0
        else:
            p=pos/(pos+neg)
            n=neg/(pos+neg)
            return -(p*math.log(p,2)+n*math.log(n,2))
