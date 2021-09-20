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

dataset = pd.read_csv('color_mappings_v5.csv', header = None )
transactions = []

print("Starting Loop")
for i in range(0, 556911):
    transactions.append([str(dataset.values[i,j]) for j in range(0, 3)])
    

print("Starting Rule Generation")
# Training Apriori on the dataset
rules = apriori(transactions, min_support = 0.00025, min_confidence = 0.2, min_lift = 3, min_length = 3)


# Visualizing the results
results = list(rules)
hashtable1 = {}

for record in results:
    
    # first index of the inner list
    # Contains base item and add item
    pair = record[0] 
    items = [x for x in pair]
    
    if (len(items) == 3):
    
        print("Rule: " + items[0] + " | " + items[1] + " -> " + items[2])
        
        #second index of the inner list
        print("Support: " + str(record[1]))
        
        #third index of the list located at 0th
        #of the third index of the inner list
        
        print("Confidence: " + str(record[2][0][2]))
        
        print("Lift: " + str(record[2][0][3]))
        
        print("=====================================")
        
        light_color = None
        dark_color = None
        component = None
        confidence = record[2][0][2]
        
        for item in items:
            
            if item[0:2] == "L#":
                light_color = item
            elif item[0:2] == "D#":
                dark_color = item
            else:
                component = item
                
        if component in hashtable1:
            if light_color in hashtable1[component]:
                existing_confidence = hashtable1[component][light_color][1]
                
                if existing_confidence < confidence:
                    hashtable1[component][light_color] = [dark_color, confidence]
            else:
                hashtable1[component][light_color] = [dark_color, confidence]
        else:
            nested_dict = {
                light_color: [dark_color, confidence]
                }
            
            hashtable1[component] = nested_dict
            
print(hashtable1.items())

hashtable_file = open("component_color_mapping.pkl", "wb")
pickle.dump(hashtable1, hashtable_file)
hashtable_file.close()

