# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 11:25:23 2022

@author: ldestouches
"""

to_shuffle = ["A","B","C","D"]
to_shuffle=[1,2,3,4]
permutation = [1,3,2,0]

shuffled = []

for j in range(len(to_shuffle)):
    new_index = permutation[j]
    new_element = to_shuffle[new_index]
    print(j,new_index,new_element)
    shuffled.append(new_element)
    
print(to_shuffle)
print(shuffled)