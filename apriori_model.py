# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 19:02:10 2021

A rule population script using apriori algorithm

@author: Murtaza Hatim Rangwala
"""

# Library Imports

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori


# Meta informations.
__version__ = '1.1.1'
__author__ = 'Murtaza Rangwala'
__author_email__ = 'dev@murtaza.info'


# Data Preprocessing

dataset = pd.read_csv('color_mappings_v2.csv', header = None )
transactions = []
for i in range(0, 556431):
    transactions.append([str(dataset.values[i,j]) for j in [1, 3, 4]])
    

# Training Apriori on the dataset
rules = apriori(transactions, min_support = 0.001, min_confidence = 0.2, min_lift = 3, min_length = 3)


# Visualizing the results
results = list(rules)

with open('rules_v2.txt', 'w') as rules_file:
    
    for item in results:
    
        # first index of the inner list
        # Contains base item and add item
        pair = item[0] 
        items = [x for x in pair]
        
        print("Rule: " + items[0] + " -> " + items[1])
        rules_file.write("Rule: " + items[0] + " -> " + items[1] + "\n")
        
        #second index of the inner list
        print("Support: " + str(item[1]))
        rules_file.write("Support: " + str(item[1]) + "\n")
        
        #third index of the list located at 0th
        #of the third index of the inner list
        
        print("Confidence: " + str(item[2][0][2]))
        rules_file.write("Confidence: " + str(item[2][0][2]) + "\n")
        
        print("Lift: " + str(item[2][0][3]))
        rules_file.write("Lift: " + str(item[2][0][3]) + "\n")
        
        print("=====================================")
        rules_file.write("=====================================\n")