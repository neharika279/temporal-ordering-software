# -*- coding: utf-8 -*-
from scipy.sparse.csgraph import minimum_spanning_tree
from sklearn.metrics.pairwise import pairwise_distances
from scipy import stats
import numpy as np
import numpy.matlib
from consensus_kmeans import consensus_kmeans
import random
from helper_functions import get_diameter_path
import path
import matrixOperations as mop


def run_spd(data,affinity,L,c1,p_thresh,mod_size_cutoff):
    #L=100;
    #c1=.8;
    #p_thresh = .002;
    #mod_size_cutoff = 5;
    labels,clusters =  consensus_kmeans(data,L,c1,affinity)

    msts = []
    dist_mats = []    
    for c in clusters:
        d = data[:,c]
        dists = pairwise_distances(d,metric=affinity)
        mst = minimum_spanning_tree(dists)
        msts.append(mst.todense())
        dist_mats.append(dists)
        
    concordance_table = compute_concordance_table(msts,dist_mats)
    #print ""
    #print "concordance table:"
    #print concordance_table

    similar_progressions,indices = compute_similar_progressions(concordance_table,msts,p_thresh)
#     print ""
#     print "similar progressions:"
#     print similar_progressions
    #print type(similar_progressions)
    
    included_clusters = indices[-mod_size_cutoff:]
    
    data_indices = []
    for i in included_clusters:
        data_indices += list(clusters[i])
        
    new_data = data[:,data_indices]
    
    new_dists = pairwise_distances(new_data,metric=affinity)
    #print "new_dists"
    #print new_dists
    
    graph_dict_mst=mop.getMST(range(len(new_dists)),new_dists)
    #print "dict of dict mst:"
    #print graph_dict_mst
    
    diamPath,diamLength=mop.getDiameterPath(graph_dict_mst,0)
    #print "diam path by basic mst method:"
    #print diamPath

    #new_mst = minimum_spanning_tree(new_dists)
    #path = get_diameter_path(new_mst)
    return diamPath,graph_dict_mst,similar_progressions,diamLength

def compute_similar_progressions(concordance_table,msts,p_thresh):
    concordant = concordance_table <= p_thresh
    similar_progressions = np.zeros((len(msts),len(msts)))
    
    for i in range(len(msts)):
        for j in range(i,len(msts)):
            concordant_i = concordant[i]
            concordant_j = concordant[j]
            num_concordant = np.count_nonzero(np.logical_and(concordant_i, concordant_j))
            similar_progressions[i,j] = num_concordant
            similar_progressions[j,i] = num_concordant
    
    #sort
    sums = sum(similar_progressions)
    idxs = np.argsort(sums)
    similar_progressions = similar_progressions[:,idxs]
    similar_progressions = similar_progressions[idxs,:]
    return similar_progressions,idxs

def compute_concordance_table(msts,dists):
    concordance_table = np.zeros((len(msts),len(msts)))
    
    for i,m in enumerate(msts):
        for j,d in enumerate(dists):
            concordance_table[i,j] = statistical_concordance(m,d)
            
    return concordance_table
    
def statistical_concordance(mst,dist):

    tree = mst > 0
    mst_dist = sum(dist[tree])
    iters = 200     
    rows = range(len(mst))
    cols = range(len(mst))
    distances = np.zeros(iters)
    
    for i in range(iters):
        random.shuffle(rows)
        random.shuffle(cols)
        tree = tree[:,cols]
        tree = tree[rows,:]
        d = sum(dist[tree])
        distances[i] = d

    d = stats.norm(loc=np.mean(distances), scale = np.std(distances))
    p = d.cdf(mst_dist)
    return p
