# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 23:48:30 2019

@author: User
"""

import numpy as np

concentrations = np.arange(0.1, 0.55, 0.05)
print(concentrations)

concentrations = np.flip(concentrations)

print(concentrations)

Vc = np.array([])

i = 0

while i < len(concentrations)-1:
    Vc = np.append(Vc, concentrations[i + 1] * 50 / concentrations[i])
    print(Vc)
    i += 1

print(Vc)


def calc_error(c_number):
    
    if c_number == 0:
        e = concentrations[0] * np.power((np.power(0.1 / 50, 2) + np.power(0.5 / 100, 2)), 0.5)
        print("c_number: ", e)
        print(concentrations[0])
        return concentrations[0] * np.power((np.power(0.1 / 50, 2) + np.power(0.5 / 100, 2)), 0.5)
    
    first_term = (np.power(0.1 / 50, 2) + np.power(0.5 / 100, 2))
    
    second_term = c_number * np.power(0.5 / 50, 2)
    
    third_term = 0
    
    x = 0
    
    while x < c_number:
        
        third_term += np.power(0.5/Vc[x], 2)
        
        x += 1
        
    return concentrations[c_number] * np.power(first_term + second_term + third_term, 0.5)


c_errors = np.array([])

y = 0

while y < len(concentrations):
    
    c_errors = np.append(c_errors, calc_error(y))
    y += 1
    
print(c_errors)

for e in c_errors:
    print(e)