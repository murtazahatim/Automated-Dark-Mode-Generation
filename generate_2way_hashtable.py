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
import pickle


# Meta informations.
__version__ = '1.1.1'
__author__ = 'Murtaza Rangwala'
__author_email__ = 'dev@murtaza.info'


# Data Preprocessing

dataset = pd.read_csv('color_mappings_v4.csv', header = None )
transactions = []

print("Starting Loop")
for i in range(0, 556911):
    transactions.append([str(dataset.values[i,j]) for j in range(0, 2)])
    

print("Starting Rule Generation")
# Training Apriori on the dataset
rules = apriori(transactions, min_support = 0.0001, min_confidence = 0.2, min_lift = 3, min_length = 2)


# Visualizing the results
results = list(rules)
hashtable2 = {}

for record in results:
    
    # first index of the inner list
    # Contains base item and add item
    pair = record[0] 
    items = [x for x in pair]
    
    print("Rule: " + items[0] + " -> " + items[1])
    
    #second index of the inner list
    print("Support: " + str(record[1]))
    
    #third index of the list located at 0th
    #of the third index of the inner list
    
    print("Confidence: " + str(record[2][0][2]))
    
    print("Lift: " + str(record[2][0][3]))
    
    print("=====================================")
    
    light_color = None
    dark_color = None
    confidence = record[2][0][2]
    
    for item in items:
        
        if item[0:2] == "L#":
            light_color = item
        elif item[0:2] == "D#":
            dark_color = item
            
    if light_color in hashtable2:
        existing_confidence = hashtable2[light_color][1]
        
        if existing_confidence < confidence:
            hashtable2[light_color] = [dark_color, confidence]
    else:
        hashtable2[light_color] = [dark_color, confidence]
            
            
print(hashtable2.items())

hashtable_file = open("color_mapping.pkl", "wb")
pickle.dump(hashtable2, hashtable_file)
hashtable_file.close()

