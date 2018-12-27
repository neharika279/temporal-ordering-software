import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

def hello():
    print "hello"
    sample_arr1=[[-7.654,2.45,8.90,4.1234],[2,4,5,6],[4,6.78,9.34,4]]
    sample_arr2=[[-7.654,2.45,8.90,4.1234],[2,7.908,9.1234,5.67],[3,9,10,11]]
    #sample_arr=np.array(sample_arr).reshape(-1,1)
    #sample_arr=np.array(sample_arr).reshape(1,-1)
    #print sample_arr
    
    centroid_1 = [np.mean(sample_arr1,0)]
    print centroid_1
    centroid_2 = [np.mean(sample_arr2,0)]
    print centroid_2
    
    centroid_dists1 = pairwise_distances(sample_arr1,Y=centroid_2,metric='euclidean')
    centroid_dists2 = pairwise_distances(sample_arr2,Y=centroid_1,metric='euclidean')

hello()
