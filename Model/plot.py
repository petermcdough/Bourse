#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 18:53:08 2018

@author: hugofayolle
"""

import matplotlib.pyplot as plt  # handles plots

from Model.config import config  # configuration

class Plot:
    """ This object is a canva for plots.
        It is defined by :
        - x_size and y_size which are the dimension of one graph
        - num_graphs which is the number of graphs it contains
        - fig which is the plt.figure object
    
    """
    def __init__(self, num_graphs, size = config.FIGSIZE):
        x_size, y_size = size
        self.num_graphs = num_graphs
        self.fig = plt.figure(figsize= (x_size, y_size * num_graphs))
       
    def draw_vertical_line(self, x):
        # adds a vertical line at index x
        plt.axvline(x, color='grey', linestyle ='dashed', linewidth=0.5)
    
    def fill(self, x, y, index = 1, color = None, title = None):
        # fills the graph at index with a line made of x and y and adds title
        plt.subplot(self.num_graphs, 1, index)
        if color is None:
            plt.plot(x, y)
        else:
            plt.plot(x, y, color)
        if title is not None:
            plt.title(title)
       
    def merge_xaxis(self):
        # sets xaxis to be confounded if there are many
        self.fig.subplots_adjust(hspace=0)
    
    def set_xaxis(self, xmin, xmax):
        # sets xmin and xmax
        axes = plt.gca()
        axes.set_xlim([xmin,xmax])