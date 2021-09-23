#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 23:07:43 2021

@author: fnuk
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 19:02:10 2021

A rule population script using apriori algorithm

@author: Murtaza Hatim Rangwala
"""

# Library Imports

import pickle
import pandas as pd
import math


# Meta informations.
__version__ = '1.1.1'
__author__ = 'Murtaza Rangwala'
__author_email__ = 'dev@murtaza.info'


# Data Preprocessing

dataset = pd.read_csv('test.csv', header = None )
transactions = []

print("Starting Loop")
for i in range(0, len(dataset)):
    transactions.append([str(dataset.values[i,j]) for j in [0, 1, 3]])
    

# Loading hashtables

hashtable1 = pickle.load(open("component_color_mapping.pkl", "rb"))
hashtable2 = pickle.load(open("color_mapping.pkl", "rb"))
default_hashtable = pickle.load(open("default_mapping.pkl", "rb"))


# Functions

def hex2rgb(hex_color):
    hex = hex_color.lstrip('L#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def rgb2hex(rgb_color):
    return "D#{0:02x}{1:02x}{2:02x}".format(rgb_color[0], rgb_color[1], rgb_color[2])


def colorCloserToBlack(light_color):
    rgb = hex2rgb(light_color)
    
    luminance = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    
    if luminance < 128:
        return True
    else:
        return False
    

def makeColorLighter(color):
    rgb = hex2rgb(color)
    
    limit_red = 255 / rgb[0] if rgb[0] != 0 else math.inf
    limit_green = 255 / rgb[1] if rgb[1] != 0 else math.inf
    limit_blue = 255 / rgb[2] if rgb[2] != 0 else math.inf
    
    constant = None
    
    if limit_red < limit_green and limit_red < limit_blue:
        constant = limit_red - 0.1
    elif limit_blue < limit_green and limit_blue < limit_red:
        constant = limit_blue - 0.1
    else:
        constant = limit_green - 0.1
        
    new_rgb = (int(rgb[0] * constant), int(rgb[1] * constant), int(rgb[2] * constant))
    
    return rgb2hex(new_rgb)



def makeColorDarker(color):
    rgb = hex2rgb(color)
    
    return rgb2hex((int(rgb[0] * 0.5), int(rgb[1] * 0.5), int(rgb[2] * 0.5)))


# Finding Dark Color Mappings
output = []
unique_components = []

for record in transactions:
    component = record[1]
    light_color = record[2]
    
    if record[0] not in unique_components:
        
        if light_color == "L#ffffff":
            output.append({
                    "name": record[0],
                    "dark": "#000000"})
    
        elif component in hashtable1:
            if light_color in hashtable1[component]:
                print(light_color + " --> " + hashtable1[component][light_color][0])
                output.append({
                    "name": record[0],
                    "dark": hashtable1[component][light_color][0].lstrip('D')})
                
        elif light_color in hashtable2:
            print(light_color + " --> " + hashtable2[light_color][0])
            output.append({
                "name": record[0],
                "dark": hashtable2[light_color][0].lstrip('D')})
            
        elif light_color in default_hashtable:
            print(light_color + " --> " + default_hashtable[light_color])
            output.append({
                "name": record[0],
                "dark": default_hashtable[light_color].lstrip('D')})
            
        else:
            print(light_color + " --> " + makeColorLighter(light_color))
            if colorCloserToBlack(light_color):
                output.append({
                "name": record[0],
                "dark": makeColorLighter(light_color).lstrip('D')})
            
            else:
                print(light_color + " --> " + makeColorDarker(light_color))
                output.append({
                "name": record[0],
                "dark": makeColorDarker(light_color).lstrip('D')})
                
        unique_components.append(record[0])
            
        
print(output)

outfile = open("output.pkl", "wb")
pickle.dump(output, outfile)
outfile.close()