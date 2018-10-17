'''
Created on 31-Aug-2018
 
@author: Neharika Mazumdar
'''
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
import executeMethods as ex
import spd as spd
import cst as cst
 
 
def test_run_spd():
     
    data_file = "dataC.csv"
    affinity = "euclidean"
    linkage = "average"    
    data =  np.loadtxt(fname = data_file, delimiter = ',')
    data = stats.zscore(data)
    data = np.nan_to_num(data)
    #data = [[0,1],[0,2],[0,4],[0,3]]
     
     
    dataset=ex.readFromFile(data_file, 'option2', 'nolabel')
     
    #dPath,edges,mst,branch,label_dict=ex.executeBasicMST(dataset)
    #print "basic mst mst:"
    #print mst
     
    path,new_mst,similar_progressions=spd.run_spd(data,affinity,10,0.5,0.5,5)
    print ""
    print "path:"
    print path
    print "new mst:"
    print new_mst
     
    #print "mst in dict:"
    #graph=ex.get_dict(new_mst.todense())
    #print graph
    noise,intensity=ex.get_path_stats(new_mst)
    print "noise, intensity:"
    print noise
    print intensity
    #print "type of new_mst:"
    #print type(new_mst)
 
 
def test_run_pq():
    data_file = "dataC.csv"
    data_file_trivial="alphamod.txt"
    data_file_parasite="finalExprSmall.csv"
    
    dataset=ex.readFromFile(data_file, 'option2', 'nolabel')
    dPath,edges,mst,branch,label_dict=ex.executeBasicMST(dataset)
    
    #pq_ranks,total_paths=ex.executePQtree(data_file,'option2','nolabel',mst,dPath,10)
    
    pqtree=mop.make_pqtree(mst)
    pqperm = mop.pqtree_perms(pqtree)
    print "pqperm 1:"
    print pqperm
    
    print "pqtree:"
    print pqtree 
#     print "type of original pqtree:"
#     print type(pqtree)

    #dataset1=ex.readFromFile(data_file_parasite, 'option2', 'nolabel')
    #dPath1,edges1,mst1,branch1,label_dict1=ex.executeBasicMST(dataset1)
    
    #pqtree1=mop.make_pqtree(mst1)
    
    #print "pqtree1:"
    #print pqtree1
    
    
    #if pqtree != pqtree1:
        #print "unequal"
    #else:
        #print "equal" 
    
    
#     pqtree=mop.get_int_values_for_pqnodes(pqtree)
#     print "type of new pqtree:"
#     print type(pqtree)
#     
#     for item in pqtree:
#         print type(item)
#         if(len(item)>1):
#             for i in item:
#                 print type(i[0])
#         else:
#             print type(item)






#     print "pqranks:"
#     print pq_ranks
#     print "total pq:"
#     print total_paths
    
    
     
def test_list_comp():
    
    l1=[([(19,), (64, 25), ([(30,), (32,), (20,), (23,)],), (65, 50)],), (11,), (54, 35), ([(15,), (48,), (67,), (28,)], [(33,), (8, 31)], 
        [(7,), (56, 10, 45), ([(6,), (9,), (66,), (18, 38)],)], [(2,), (58, 1), (39,), (21, 44), (16,)], [(12,), (36,), (69, 53), (47,)])]
    
    l2=[(11,), ([(19,), (64, 25), ([(30,), (32,), (20,), (23,)],), (65, 50)],), (54, 35), ([(15,), (48,), (67,), (28,)], [(33,), (8, 31)], 
        [(7,), (56, 10, 45), ([(6,), (9,), (66,), (18, 38)],)], [(2,), (58, 1), (39,), (21, 44), (16,)], [(12,), (36,), (69, 53), (47,)])]
    
    for x in l1:
        print type(x)
        print "interior"
        print type(x[0])
    for y in l2:
        print type(y)
        print "interior"
        print type(y[0])
        
     
    
    if l1 != l2:
        print "not equal"
    else:
        print "equal"
        
    
    
         
#test_run_spd()
#test_run_pq()
#test_list_comp()