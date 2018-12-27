# -*- coding: utf-8 -*-
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from sklearn.metrics.pairwise import pairwise_distances
from scipy.sparse.csgraph import shortest_path
from scipy import stats
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from scipy.cluster import hierarchy
from helper_functions import get_diameter_path
#import numpy.matlib
from scipy.sparse import csr_matrix

def run_cst(data,affinity,linkage,merge_method):
    
    Z = hierarchy.linkage(data, linkage)
    
    Tcsr = merge_clusters(Z,data,affinity,merge_method)
    
#    diameter,predecessors = shortest_path(Tcsr,return_predecessors=True,directed=False)
    

#    longest = np.argmax(diameter)
#    i = longest / len(data)
#    j = longest % len(data)
    
    path = get_diameter_path(csr_matrix(Tcsr))
    return path,Tcsr
    
    
def merge_clusters(Z,data,affinity,merge_method):
    nodes = []
    links = []
    adj_mat = np.zeros((len(data),len(data)))
    dist_mat = pairwise_distances(data,metric=affinity)
    #print "distance matrix:"
    #print dist_mat

    # initialize leaf clusters
    for i,d in enumerate(data):
        nodes.append([i])
        
    
    for c1,c2,d,size in Z:
        #print 
        c1 = nodes[int(c1)]
        c2 = nodes[int(c2)]
        
        link = get_linkage(c1,c2,data,affinity,method=merge_method)    
        #print "output of linkage:"
        #print link    
        links.append(link)
        
        adj_mat[link[0],link[1]] = dist_mat[link[0],link[1]]
        adj_mat[link[1],link[0]] = dist_mat[link[1],link[0]]        
        
        new_clust = c1 + c2
        assert len(new_clust) == size
        nodes.append(new_clust)
    
    return adj_mat
       
def get_linkage(c1,c2,data,affinity,method,lambda_val=.01):

    if method == "NearestNeighbors":
        return nearest_neighbors_linkage(c1,c2,data,affinity)
    elif method == "WeightedCentroids":
        return weighted_centroids_linkage(c1,c2,data,affinity,lambda_val)
    elif method == "CentroidPoints":
        return centroid_points_linkage(c1,c2,data,affinity)

    raise Exception("Unknown Merging Method")
    

def nearest_neighbors_linkage(c1,c2,data,affinity):
    c1_points = data[c1,:]
    c2_points = data[c2,:]
    dists = pairwise_distances(c1_points,Y=c2_points,metric=affinity)
    
    shortest = np.argmin(dists)
    if len(c1) == 1:
        i=0
    else:
        i = shortest / len(c2)
    
    if len(c2) == 1:
        j=0
    else:
        j = shortest % len(c2) 
    link = (c1[i],c2[j])
    return link
    
def centroid_points_linkage(c1,c2,data,affinity):
    
    c1_points = data[c1,:]
    c2_points = data[c2,:]
    
    centroid_1 = [np.mean(c1_points,0)]
    centroid_2 = [np.mean(c2_points,0)]
    
    centroid_dists1 = pairwise_distances(c1_points,Y=centroid_2,metric=affinity)
    centroid_dists2 = pairwise_distances(c2_points,Y=centroid_1,metric=affinity)
    
    shortest1 = np.argmin(centroid_dists1)
    shortest2 = np.argmin(centroid_dists2)
    
    link = (c1[shortest1],c2[shortest2])
    return link   
      
def weighted_centroids_linkage(c1,c2,data,affinity,lambda_val):
    c1_points = data[c1,:]
    c2_points = data[c2,:]
    centroid_1 = np.mean(c1_points,0)
    centroid_2 = np.mean(c2_points,0)
    
    centroid_dists1 = pairwise_distances(c1_points,Y=centroid_2,metric=affinity)
    centroid_dists2 = pairwise_distances(c2_points,Y=centroid_1,metric=affinity)
    
    cent_dists1 = np.repmat(centroid_dists1, 1, len(c2)) * lambda_val
    cent_dists2 = np.repmat(centroid_dists2, 1, len(c1)).T * lambda_val
    
    dists = pairwise_distances(c1_points,Y=c2_points,metric=affinity)
    dists = dists + cent_dists1 + cent_dists2
    
    shortest = np.argmin(dists)
    if len(c1) == 1:
        i=0
    else:
        i = shortest / len(c2)
    
    if len(c2) == 1:
        j=0
    else:
        j = shortest % len(c2) 
    link = (c1[i],c2[j])
    return link        

def test_run_cst():
    data_file = "dataC.csv"
    affinity = "euclidean"
    linkage = "average"    
    data =  np.loadtxt(fname = data_file, delimiter = ',')
    print "data:"
    print data
    data = stats.zscore(data)
    data = np.nan_to_num(data)
    #data = [[0,1],[0,2],[0,4],[0,3]]
    
    path,tcsr =run_cst(data,affinity,linkage,"CentroidPoints")
    print path
    print tcsr
#test_run_cst()

