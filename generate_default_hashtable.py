# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 19:02:10 2021

A rule population script using apriori algorithm

@author: Murtaza Hatim Rangwala
"""

# Library Imports

import pickle
import pandas as pd


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
    

temp_hashtable = {}

for pairing in transactions:
    
    if pairing[0] in temp_hashtable:
        if pairing[1] in temp_hashtable[pairing[0]]:
            temp_hashtable[pairing[0]][pairing[1]] += 1
        else:
            temp_hashtable[pairing[0]][pairing[1]] = 1
    else:
        nested_dict = {
            pairing[1]: 1
            }
        temp_hashtable[pairing[0]] = nested_dict
        
#print(temp_hashtable.items())

default_hashtable = {}

for light_color, mapping in temp_hashtable.items():
    max_mapping = (None, 0)
    
    for dark_color, count in mapping.items():
        if count > max_mapping[1]:
            max_mapping = (dark_color, count)
            
    default_hashtable[light_color] = max_mapping[0]
    
print(default_hashtable)

hashtable_file = open("default_mapping.pkl", "wb")
pickle.dump(default_hashtable, hashtable_file)
hashtable_file.close()
    