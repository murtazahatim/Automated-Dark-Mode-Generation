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

# Meta informations.
__version__ = '1.1.1'
__author__ = 'Murtaza Rangwala'
__author_email__ = 'dev@murtaza.info'


# Loading output

ready_array = pickle.load(open("output.pkl", "rb"))


xml_output = '<?xml version="1.0" encoding="utf-8"?>\n'
xml_output += "<resources>\n"
for i in ready_array:
    s = '\t<color name="'+ i["name"] + '">'+ i["dark"] + '</color>\n'
    xml_output += s
    
xml_output += "</resources>\n"

xmlfile = "colors.xml"

f = open(xmlfile, "a")
f.write(xml_output)
f.close