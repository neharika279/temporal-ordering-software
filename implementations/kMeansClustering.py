'''
Created on 04-Nov-2017

@author: Neharika Mazumdar
'''

import numpy as np
import csv,copy
import Cluster_Ensembles as ce
from sklearn.cluster import KMeans
from numpy import ndarray
from scipy.stats.stats import pearsonr
from scipy.sparse import * 
from networkx.algorithms import cluster
from sets import Set
#from trial import geneExpressionData

expressions=6
samples=6
c1=0.7
c2=0.9


geneModulesAfterClustering=[[[]]]
finalCoherentGeneModules=[[[]]]

def kMeans(sparseDataMatrix,originalDataMatrix):
    
    cluster0=[[]]
    cluster1=[[]]
    clusterCentroids=[[]]
    clusterLabels=[[]]
        
    
    kmeans=KMeans(n_clusters=2,max_iter=100).fit(sparseDataMatrix)
    
    clusterLabels=kmeans.labels_
    
    clusterCentroids=kmeans.cluster_centers_
    
    
    for item in range(len(originalDataMatrix)):
        
        if(clusterLabels[item]==0):
            #copy the 'item' row of dataMatrix in cluster0
            
            cluster0.append(originalDataMatrix[item])
            
            
        elif(clusterLabels[item]==1):
            #copy the 'item' row of dataMatrix in cluster1
           
            cluster1.append(originalDataMatrix[item])
            
            
    cluster0.pop(0)
    
    cluster1.pop(0)
    
   
    return cluster0, cluster1,clusterCentroids
         
    
def checkThresholdForClustering(clusterMatrix,clusterCentroids):
    
    sumCorr=0
    pearsonValue=0.0
    
    for item in range(len(clusterMatrix)):
        corr,pvalue=pearsonr(clusterMatrix[item], clusterCentroids)
        sumCorr+=corr
        
    pearsonValue=sumCorr/len(clusterMatrix)
    
    
    if (pearsonValue<c1):
        return False
        
    if(pearsonValue>c1):
        return True
            

def iterative_coherence(gene_module, centroid):
    
    threshold=checkThresholdForClustering(gene_module,centroid)
    
    if(not threshold):
        #print ""
        #print "did not pass threshold c1"
        S = coo_matrix(gene_module)
        #print "intermediate sparse matrix:"
        #print S.toarray()
        
        cluster0,cluster1,centroid=kMeans(S.tocsr(),gene_module)
        
        iterative_coherence(cluster0,centroid[0])
        iterative_coherence(cluster1,centroid[1])
        
    else:
        #print ""
        #print "passed threshold c1"
        geneModulesAfterClustering.append(gene_module)
        

def getCoherentGeneModules(dataMatrix):  
    
    global geneModulesAfterClustering
    
    S = coo_matrix(dataMatrix)
    #print "intermediate sparse matrix:"
    #print S.toarray()
        
    cluster0,cluster1,centroid=kMeans(S.tocsr(),dataMatrix)
    
    #print ""
    #print "original cluster0::"
    #print np.array(cluster0)
    
    #print ""
    #print "original cluster1::"
    #print np.array(cluster1)
    
    
    iterative_coherence(cluster0, centroid[0])
    iterative_coherence(cluster1, centroid[1])
    
#     #check for cluster0:
#     thresholdCluster0=checkThresholdForClustering(cluster0,centroid[0])
#     if(not thresholdCluster0):
# 
#         getCoherentGeneModules(cluster0)
#         #add cluster0 to gene module
#     else:
#         geneModulesAfterClustering.append(cluster0)
#     
#     
#     #check cluster1
#     thresholdCluster1=checkThresholdForClustering(cluster1,centroid[1])
#     if(not thresholdCluster1):
# 
#         getCoherentGeneModules(cluster1)
# 
#     #add cluster1 to gene module
#     else:
#         geneModulesAfterClustering.append(cluster1)
    

    return geneModulesAfterClustering
    
def calculatePairwiseModuleCorrelation(geneModuleMatrix):
    
    global finalCoherentGeneModules
        
    finalCoherentGeneModules=[np.sort(item) for idx,item in enumerate(geneModuleMatrix)]
    #finalCoherentGeneModulesTupleList=[tuple(l) for l in finalCoherentGeneModules]
    
    merged=False
    #finalCoherentGeneModules.tolist()
    #print ""
    #print "before everything geneModuleMatrix:"
    #print geneModuleMatrix
    #print np.array(geneModuleMatrix)
    #print ""
    #print "size of geneModuleMatrix:"
    #print len(geneModuleMatrix)
   
    for outerIndex,outerModule in enumerate(finalCoherentGeneModules):
       
        #print "in OUTER FOR LOOP"
        #print ""
        #print "geneModuleMatrix element being considered:"
        #print outerModule
        for innerIndex,innerModule in enumerate(finalCoherentGeneModules):
            
            #print "in INNER FOR LOOP"
            #print ""
            #print "geneModuleMatrix element being considered:"
            #print innerModule
            #print "index of outer module::"
            #print outerIndex
            #print "index of inner module::"
            #print innerIndex
            if(outerIndex!=innerIndex):
                
                #print ""
                #print "different indices"
                #print "considering modules::"
                #print ""
                #print "cluster1:"
                #print outerModule
                #print "mean of cluster1::"
                #print (np.mean(outerModule, axis=0))
                #print ""
                #print "cluster2:"
                #print innerModule
                #print "mean of cluster2::"
                #print (np.mean(innerModule,axis=0))
                
                mergeThresholdResult=checkThresholdForMerging((np.mean(outerModule, axis=0)), (np.mean(innerModule,axis=0)))
                
                if(not mergeThresholdResult):
                    #print ""
                    #print "merging modules"
                    if(outerModule in finalCoherentGeneModules):
                        #print "removing:"
                        #print np.array(outerModule)
                        finalCoherentGeneModules.remove(outerModule)
                    
                    if(innerModule in finalCoherentGeneModules):
                        #print "removing:"
                        #print np.array(innerModule)
                        finalCoherentGeneModules.remove(innerModule)
                 
                    merged_list=mergeGeneModules(outerModule, innerModule)
                    
                    
                    if(np.sort(merged_list) not in finalCoherentGeneModules):
                        finalCoherentGeneModules.append(np.sort(merged_list))
                        
                    merged=True
                    
                    break
                
                
                #print ""
                #print "after first merge, before second FOR CYCLE::geneModuleMatrix::"
                #print ""
                #print "gene module matrix after considering a module pair"
                #print np.array(finalCoherentGeneModules)
            
        if(merged):
            break
    
    #finalCoherentGeneModules.pop(0)
    
    recursiveMerging(finalCoherentGeneModules)
    
    return finalCoherentGeneModules



def strip_last_empty (rowiter, delimiter=","):
    allextra = True
    rows = []
    for row in rowiter:
        if not len(row):
            rows.append(row)
            allextra = False
            continue
        if len(row[-1]):    # if the last element is not an empty string
            allextra = False
        rows.append(row)

    if allextra:            # if every row has the extra empty string, strip it
        return [r[:-1] for r in rows]
    else:
        return rows
    
def seq_astype (seq, type=int, na=False, nastring="NA", navalue=-999):
    
    try:
        return [type(i) for i in seq], None
    except ValueError:
        if not na:
            raise
        cseq, mask = [],[]
        for i in seq:
            if i == nastring:
                cseq.append(navalue)
                mask.append(1)
            else:
                try:
                    cseq.append(type(i))
                    mask.append(0)
                except ValueError:
                    raise ValueError("Unable to automatically convert seq.")
        return cseq, mask           

                
    
        
def recursiveMerging(geneModuleMatrix):
    global finalCoherentGeneModules
    merged=False
    #print ""
    #print "gene module in recursive function:"
    #print np.array(geneModuleMatrix)
    
    for outerIndex,outerModule in enumerate(geneModuleMatrix):
        #print "OUTER MODULE::"
        #print outerModule
        for innerIndex,innerModule in enumerate(geneModuleMatrix):
            #print "INNER MODULE::"
            #print innerModule
           
            if(outerIndex!=innerIndex):
                #print ""
                #print "different indices"
                mergeThresholdResult=checkThresholdForMerging((np.mean(outerModule, axis=0)), (np.mean(innerModule,axis=0)))
            
                if(not mergeThresholdResult):
                    #print ""
                    #print "merging the modules"
                    np.delete(finalCoherentGeneModules, np.sort(outerModule))
                    #finalCoherentGeneModules.remove(np.sort(outerModule))
                    np.delete(finalCoherentGeneModules, np.sort(innerModule))
                    merged_list=mergeGeneModules(outerModule, innerModule)
                    
                    if(np.sort(merged_list) not in finalCoherentGeneModules):
                        finalCoherentGeneModules.append(np.sort(merged_list))
                    
                    merged=True
                    break
        if(merged):
            break
            
    if(geneModuleMatrix==finalCoherentGeneModules):
        return
    else:
        recursiveMerging(finalCoherentGeneModules)
def checkThresholdForMerging(moduleMean1,moduleMean2):
    corr,pvalue=pearsonr(moduleMean1, moduleMean2)
    
    if(corr<c2):
        return True
    
    elif(corr>c2):
        return False
    
    
def mergeGeneModules(module1,module2):
    
    #global finalCoherentGeneModules
    merged_list=[[]]
    
    for item in module1:
        merged_list.append(item)
        
    for item1 in module2:
        merged_list.append(item1)
    
    merged_list.pop(0)

    return merged_list
    
    




        
        
    
    
    
    
    