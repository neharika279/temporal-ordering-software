'''
Created on 16-Dec-2017

@author: Neharika Mazumdar
'''

from __future__ import division
import numpy as np
import kMeansClustering as km
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist
import scipy.stats as stats
import copy,random


MSTlist=[[[]]]
concordanceDict={}

def getProgressionSimilarityDict(finalModuleSet,mst):
    
    global concordanceDict
    numerator=1
    
    
    for module in finalModuleSet:
        
        moduleTrans=np.transpose(np.array(module))
        treeTuple=()
        
        distMatrix=getDistanceMatrix(moduleTrans)
        
        for tree in mst:
            
            pre_value=getSValue(tree,distMatrix)
            
            i=0
            while(i<1000):
                
                np.random.shuffle(distMatrix)
                current_value=getSValue(tree,distMatrix)
                #print "prev_value:",pre_value
                #print "curr_value:",current_value
                
                if(current_value<pre_value):
                    numerator=numerator+1
                
                
                pre_value=current_value
                i=i+1
            probVal=0.0
            probVal=(numerator/1000)*0.33
            #print "probVal:",probVal
            if(probVal>=0.2):
                
                treeTuple=treeTuple+(mst.index(tree),)
                
        concordanceDict[finalModuleSet.index(module)]=treeTuple
                
    
    #print concordanceDict
    return concordanceDict
    
    
    
def getSValue(tree,distMatrix):
    
    
    sumValues=0
    
    for row in tree:
        
        for adjVal in row:
            
            if tree[tree.index(row)][row.index(adjVal)]==1:
                
                sumValues=sumValues+distMatrix[tree.index(row)][row.index(adjVal)]
    
    return sumValues
            
  
def getProgressionSimilarityMatrix(finalModuleSet,concDict):
        
    progressionSimilarityMatrix=[[0 for x in range(len(finalModuleSet))] for y in range(len(finalModuleSet))] 
    
    
    for outerModule in finalModuleSet:
        
        for innerModule in finalModuleSet:
            
            matrixCellValue=0
            
            treeTupleOuter=concDict[finalModuleSet.index(outerModule)]    
            treeTupleInner=concDict[finalModuleSet.index(innerModule)]
            
            for treeNumber in treeTupleOuter:

                if treeNumber in treeTupleInner:
                
                    matrixCellValue=matrixCellValue+1
                    #print "yet another concordant common MST"
            
            progressionSimilarityMatrix[finalModuleSet.index(outerModule)][finalModuleSet.index(innerModule)]=matrixCellValue
            
    
    return progressionSimilarityMatrix        
    
    
      
def getMSTlist(finalModuleSet):
    
    global MSTlist
    
    for module in finalModuleSet:
        
        moduleTrans=np.transpose(np.array(module))
        currentMST=moduleWiseMST(moduleTrans)
        MSTlist.append(currentMST)
        
    MSTlist.pop(0)
    #print "MST list:"
    #print np.array(MSTlist)
    #print "indices of geneModules:"
    #print len(finalModuleSet)
    
    #print "indices of MSTs:"
    #print len(MSTlist)
    return MSTlist


def moduleWiseMST(geneModuleTranspose):
    
    distMatrix=getDistanceMatrix(geneModuleTranspose)

    treeGraph=getMST(range(len(geneModuleTranspose)), distMatrix)
    
    keys=sorted(treeGraph.keys())
    size=len(keys)
    
    M = [ [0]*size for i in range(size) ]
    
    for a,b in [(keys.index(a), keys.index(b)) for a, row in treeGraph.items() for b in row]:
        M[a][b] = 2 if (a==b) else 1
        
    return M


def getDistanceMatrix(dataset):
    Q = np.inner(dataset,dataset)
    diag = np.diagonal(Q)
   
    R = np.ones(Q.shape)*diag
   
    return np.sqrt(R+np.transpose(R) - 2*Q)

def getMST(V,W):
    

    W = np.array(W, np.float)
    INF = 10000 * np.amax(np.amax(W))
    
    P = {}

    Q = PriorityDict()
    Q[V[0]] =  0      

    i = 1 
    for v in V[1:]:
        Q[i] = INF
        i += 1
 
    for u in Q:       
        Adj = adjacent(W, u)               
        for v in Adj:
            v=tuple(v)
            for item in v:   
                w = W[u,item]  
                try:
                    if w < Q[item]:
                       
                        P[item] = u
                        
                        Q[item] = w
                except KeyError:
                    continue 
    g = {}
    for key in P:
        i, j = key, P[key]
        add(g, i, j, W[i][j])
    return g

def add (graph, i, j=None, weight=1, undirected=True, noselfloops=True):
    """Add a vertex or edge to a graph."""
    if j is None:
        if i not in graph.keys():
            graph[i] = {}
    else:
        if (i==j) and noselfloops:
            return
        if i not in graph:
            graph[i] = {}
        if j not in graph:
            graph[j] = {}
        graph[i][j] = weight
        #print "Weight:"
        #print weight
        #print graph[i][j]
        #print i,j,graph
        if undirected:
            graph[j][i] = weight


def adjacent(W, u):
    return list(np.nonzero(np.greater(W[u],0)))

def reorderProgressionSimilarityMatrix(progMatrix):
    
    distMatrix = dist.pdist(progMatrix)
    distSquareMatrix = dist.squareform(distMatrix)
    print "distance square matrix:"
    print np.array(distSquareMatrix)
    Z = hier.linkage(distSquareMatrix)
    print np.array(Z)
    print "shape:",np.array(Z).shape
    return distSquareMatrix

def getFinalSelectedModules(progMat,finalModuleSet):
    
    resultSet=[[]]
    finalResultSet=[[]]
    
    for i in range(2):
        resultSet.append(finalModuleSet[i])
        
    resultSet.pop(0)
    
    i=0
    while(i<len(resultSet)):
        finalResultSet[0].append(resultSet[i])
        
    return finalResultSet
    
    
def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))
        
    


"*****************************************PRIORITY DICT IMPLEMENTATION TAKEN FROM EXISTING MAGWENE PRIORITY DICT IMPLEMENTATION*****************************"

class PriorityDict(dict):
    def __init__(self):
        """Initialize PriorityDict by creating binary heap of pairs (value,key). 
        Note that changing or removing a dict entry will not remove the old pair 
        from the heap until it is found by smallest() or until the heap is 
        rebuilt.
        """        
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        '''Find smallest item after removing deleted items from heap.'''
        if len(self) == 0:
            raise IndexError, "smallest of empty PriorityDictionary"
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and \
                        heap[smallChild] > heap[smallChild+1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]
    
    def __iter__(self):
        '''Create destructive sorted iterator of PriorityDictionary.'''
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()
    
    def __setitem__(self,key,val):        
        """Change value stored in dictionary and add corresponding pair to heap. 
        Rebuilds the heap if the number of deleted items grows too large, to 
        avoid memory leakage.
        """
        dict.__setitem__(self,key,val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.iteritems()]
            self.__heap.sort()  # builtin sort likely faster than O(n) heapify
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and \
                    np.any(newPair < heap[(insertionPoint-1)//2]):
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair
    
    def setdefault(self,key,val):
        '''Reimplement setdefault to call our customized __setitem__.'''
        if key not in self:
            self[key] = val
        return self[key]

    def update(self, other):
        for key in other.keys():
            self[key] = other[key]


