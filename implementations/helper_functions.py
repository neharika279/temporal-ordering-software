# -*- coding: utf-8 -*-
from scipy.sparse.csgraph import shortest_path
import numpy as np

def get_path(i,j,predecessors):
    path = []
    current_node = i    
    next_node = predecessors[j,i]
    
    while next_node != j:
        edge = (current_node,next_node)
        #print edge
        path.append(edge)
        current_node = next_node
        
        next_node = predecessors[j,current_node]
    
    edge = (current_node,next_node)
    path.append(edge)
    return path
    
    
def get_diameter_path(Tcsr):
    diameter,predecessors = shortest_path(Tcsr,return_predecessors=True,directed=False)
    sz = Tcsr.todense().shape
    longest = np.argmax(diameter)
    i = longest / sz[0]
    j = longest % sz[0]
    
    return get_path(i,j,predecessors)
