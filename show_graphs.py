#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:20:48 2020

@author: paul
"""
#from plotly.graph_objs import Bar
#from plotly import offline

class Graphs:
    def __init__(self):
        pass
    
    def simple_graph(self, x_values, y_values):
        data = [{
            'type': 'bar',
            'x': x_values[-100:],
            'y': y_values[-100:],
            'hovertext': x_values,
            'marker': {
                'color': 'rgb(60, 100, 150)',
                'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
            },
            'opacity': 0.6,
        }]
        
        my_layout = {
            'title': 'Most-Used Words by Trump Whitehouse Press Conferences',
            'titlefont': {'size': 28},
            'xaxis': {
                'title': 'Words',
                'titlefont': {'size': 64},
                'tickfont': {'size': 104},
            },
            'yaxis': {
                'title': 'Used',
                'titlefont': {'size': 64},
                'tickfont': {'size': 104},
            },
        
        }
        
        fig = {'data': data, 'layout': my_layout}
        #offline.plot(fig)                   