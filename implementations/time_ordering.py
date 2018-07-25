# -*- coding: utf-8 -*-
from functools import partial
from spd import run_spd
from magwene import run_magwene
from cst import run_cst
from render_trees import print_mst
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
from sklearn.decomposition import PCA

class TimeOrdering:
    
    def __init__(self,data,affinity,method=None,linkage=None,merging=None,
                 L=None,c1=None,p_thresh=None,num_concordant_modules=None,
                 labels=None):
        self.method=method
        self.affinity=affinity
        self.linkage=linkage
        self.merging=merging
        self.L=L
        self.c1=c1
        self.p_thresh=p_thresh
        self.num_concordant_modules=num_concordant_modules
        self.labels=labels
        self.data = data
        self.mst = None
        self.path = None
        self.tree_based_reordering = None
        self.projection_based_reordering = None
        self.interpolated_path = []
        self.interpolated_path_pca = None
        self.interpolated_path_points = 200
        self.projection_order = None
        
        
        if method == "MST" or method == "magwene":
            self.execute = partial(run_magwene,self.data,self.affinity)
        
        elif method == "CST":
            if not linkage or not merging:
                raise Exception("Invalid Arguments")
            self.execute = partial(run_cst,data,affinity,linkage,self.merging)
        
        elif method == "SPD":
            if not L or not c1 or not p_thresh or not num_concordant_modules:
                raise Exception("Invalid Arguments")
                
            self.execute = partial(run_spd,data,affinity,L,c1,p_thresh,mod_size_cutoff)
            
        else:
            raise Exception("Must input tree construction method.")
            
            
            
    def perform_ordering(self):
        self.path,self.mst = self.execute()
        print "MST:::"
        print self.mst
        self.compute_data_reorderings()
        return self.path,self.interpolated_path_pca,self.projection_order,self.mst
        
    def write_tree(self,directory,file_name):
        if self.mst == None:
            raise Exception("Must compute tree before rendering it")
        
        
        print_mst(directory,file_name,self.mst,self.labels)
        
    def compute_data_reorderings(self):
        if self.mst == None:
            raise Exception("Must compute tree before reordering it")

        self.diameter_path_order = self.extract_diameter_path_order()        
        
        self.compute_interpolated_path()
        #raise
        #self.tree_based_reordering = compute_tree_based_reordering()
        self.projection_based_reordering = self.compute_projection_based_reordering()
        
    def compute_interpolated_path(self):
        interp_path = []
        interpolated_path_concat = np.zeros((1,self.data[self.diameter_path_order[0]].size))
        interpolated_path_concat[0,:] = self.data[self.diameter_path_order[0]]
        for i in range(len(self.diameter_path_order)-1):
            cur_line = np.zeros((self.interpolated_path_points,len(self.data[0,:])))
            a = self.data[self.diameter_path_order[i]]
            b = self.data[self.diameter_path_order[i+1]]
            
            slope = b-a
    
            interval = slope / self.interpolated_path_points
            for j in range(self.interpolated_path_points):
                cur_line[j,:]=a + (interval * j)
                
            self.interpolated_path.append(cur_line)
            interpolated_path_concat = np.concatenate((interpolated_path_concat,cur_line))
            
        pca = PCA(n_components=3)
        pca.fit(self.data)
        self.interpolated_path_pca = pca.transform(interpolated_path_concat)
    
    def compute_projection_based_reordering(self):
        
        self.projection_order = []
        
        path_points = self.data[self.diameter_path_order,:]
        
        p_dists = pairwise_distances(self.data,Y=path_points)
        mins = np.argmin(p_dists,axis=1)
        
        path_assignments = [[] for p in self.diameter_path_order]
        
        for i,m in enumerate(mins):
            path_assignments[m].append(i)
            
        for i in range(len(self.interpolated_path)):
            if i == 0:
                segment = self.interpolated_path[0]
            elif i == len(self.diameter_path_order)-1:
                segment = self.interpolated_path[i]
            else:
                segment = np.concatenate((self.interpolated_path[i-1],self.interpolated_path[i]))
            
            points = path_assignments[i]
            data_points = self.data[points,:]
            dists = pairwise_distances(data_points,Y=segment)
        
            min_dists = np.argmin(dists,axis=1)
            sorted_points_idx = np.argsort(min_dists)
        
            for p in sorted_points_idx:
                self.projection_order.append(points[p])
                
        
 
    def extract_diameter_path_order(self):
        path_nodes = []
        path_nodes.append(self.path[0][0])
        
        for p in self.path:
            path_nodes.append(p[1])
            
        return path_nodes
        