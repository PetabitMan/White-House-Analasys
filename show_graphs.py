#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:20:48 2020

@author: paul
"""
import matplotlib.pyplot as plt

class Graphs:
    def __init__(self):
        pass
    
    def simple_graph(self, x_values, y_values):
        plt.figure(figsize=(60, 30))

        plt.subplot(131)
        plt.bar(x_values, y_values)
        plt.subplot(132)
        plt.scatter(x_values, y_values)
        plt.subplot(133)
        plt.plot(x_values, y_values)
        plt.suptitle('Categorical Plotting')
        plt.show()
        
