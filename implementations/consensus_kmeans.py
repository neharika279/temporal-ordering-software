# -*- coding: utf-8 -*-
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances

def consensus_kmeans( data, L, c1,affinity ):
    data = data.T
    clusters = consensus_kmeans_recursive( data,np.arange(len(data)), L, c1,affinity )
    clust_labels = np.zeros(len(data))
    for l,c in enumerate(clusters):
        for i in c:
            clust_labels[i] = l
    
    return clust_labels,clusters
    
def consensus_kmeans_recursive( data,indices, L, c1,affinity ):
    clusters = []    
    if len(data) == 1:
        clusters.append(indices)
        return clusters
        
    mean_cor = compute_average_correlation(data,affinity);

    if mean_cor > c1:
        clusters.append(indices)
        return clusters
    
    kmeans = KMeans(n_clusters=2)
    
    consensus = np.zeros((L, len(data)))
    
    for i in range(L):
        c = kmeans.fit_predict(data)
        consensus[i] = c
        
    consensus_clust = kmeans.fit_predict(consensus.T)
    
    
    clust1 = data[consensus_clust.nonzero()]
    clust1_indices = indices[consensus_clust.nonzero()]
    
    clust2 = data[(consensus_clust *-1 + 1).nonzero()]
    clust2_indices = indices[(consensus_clust *-1 + 1).nonzero()]
    
    c_ret1 = consensus_kmeans_recursive( clust1, clust1_indices, L, c1,affinity );
    c_ret2 = consensus_kmeans_recursive( clust2, clust2_indices, L, c1,affinity );
    
    for c in c_ret1:
        clusters.append(c)
        
    for c in c_ret2:
        clusters.append(c)
    
    return clusters
    
 
def compute_average_correlation(data,affinity):
    
    dists = []
    centroid = np.mean(data,0)
    dists = pairwise_distances(data,Y=centroid,metric="correlation")
        
    dists = 1-dists
    return np.nanmean(dists)
    
def test_consensus_kmeans():
    data_file = "/Users/ryaneshleman/Dropbox/SFSU/research/cst_lib/workspace/data/parasite_data.csv"
    affinity = "euclidean"
    linkage = "average"    
    data =  np.loadtxt(fname = data_file, delimiter = ',')
    data = stats.zscore(data)
    data = np.nan_to_num(data)
    
    L=100;
    c1=.9;
    c2=.9;
    
    clusters =  consensus_kmeans( data, L, c1,c2,affinity )
    
    
    
            
    print clusters

if __name__ == "main":
    test_consensus_kmeans()