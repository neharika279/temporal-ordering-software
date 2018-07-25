'''
Created on 30-Sep-2017

@author: Neharika Mazumdar
'''
from __future__ import division
import csv,copy
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
import graphFunctions as graph
import random


def path_length(path, distmtx, seglengths=None):
    """path, distance matrix -> length of path (optional: segment lengths)
    
    Given distance matrix and path (sequence of integers where values correspond
    to rows of matrix; e.g. [1,2,4,5,3,9,8,6]) calculates total path length.
    """ 
    pairs = zip(path,path[1:])
    segments = []
    tot = 0.0
    for each in pairs:
        segments.append(distmtx[each])
        tot += distmtx[each]
    
    if seglengths is None:
        return tot
    else:
        return tot, segments

def rank_paths(paths, dist):
    """Given a set of paths, and a distance matrix, rank those paths from shortest
    to longest.
    """
    spaths=[[]]
    # rank and order paths
    lengths = [path_length(i,dist) for i in paths]
    
    for index in np.argsort(lengths):
        spaths.append(list(paths[index]))
    #spaths.append(np.take(paths, np.argsort(lengths)))
    spaths.pop(0)
    
    sortedpaths = []
    for path in spaths:
        sortedpaths.append(path)
    sortedlengths = np.sort(lengths)
    
    
    class Results:
        pass
    r = Results()        
    r.paths = sortedpaths
    r.lengths = sortedlengths
    return r    


def permute_iter(seq):
    """Constructs all permutations of the given sequence.
    """
    if len(seq) == 1:
        yield (seq)
        raise StopIteration

    for i in range(len(seq)):
        eslice = seq[i:i+1]
        rest_iter = permute_iter(seq[:i] + seq[i+1:])
        for rest in rest_iter:
            yield (eslice + rest)

    raise StopIteration

def qflip_shallow(qnode):
    rev = list(qnode)
    rev.reverse()
    return rev

def pperm_shallow(pnode):
    return list(permute_iter(pnode))

def pqtree_perms(seq):
    stack = [seq[:]]
    ischanging = True
    while ischanging:
        for j in range(len(stack)):
            s = stack[j]
            for i in range(len(s)):
                if type(s[i]) == Pnode:
                    ischanging = True
                    perms = pperm_shallow(s[i])
                    if len(perms) > 1:
                        for perm in perms:
                            
                            #perm=[tuple(x) for x in perm]
                            #t=[tuple(y) for y in list(s[i])]
                            
                            #if np.not_equal(perm,list(s[i])):
                            if perm != list(s[i]):
                                stack.append(s[:i] + perm + s[i+1:])
                                stack[j] = s[:i] + s[i] + s[i+1:] 
                    else:
                        stack[j] = s[:i] + s[i] + s[i+1:]
                    break
                elif type(s[i]) == Qnode:
                    ischanging = True
                    perm = qflip_shallow(s[i])
                    if perm != list(s[i]):
                        stack.append(s[:i] + perm + s[i+1:])
                        stack[j] = s[:i] + s[i] + s[i+1:]
                    else:
                        stack[j] = s[:i] + s[i] + s[i+1:]
                    break
                else:
                    ischanging = False
                    continue
    return stack



def getGraph():
    
    f = open("jellyroll.txt", 'r')
    rows=[]
    reader=csv.reader(f,delimiter="\t")
    for r in reader:
        rows.append(r)
        
    print rows
    arrRow=np.array(rows,dtype=float)
#     print arrRow
#     print arrRow.shape
#     print "shape:"
    return arrRow

def tableasrows (filename, delimiter, commentchar="#", skipinitialspace=True,
                hasheader=False, hasrownames=False,
                autoconvert=False, na=False, nastring="NA", navalue=-999):

    f = open(filename, 'r')
    reader = csv.reader(f, delimiter=delimiter, skipinitialspace=skipinitialspace)
    srows = strip_last_empty(reader, delimiter=delimiter)
    if hasheader:
        header = srows[0]
        srows = srows[1:]
    if hasrownames:
        rownames = []
        
    rows = []
    mask = []
    for i,row in enumerate(srows):
        try:
            if row[0][0] == commentchar:
                continue
        except IndexError:
            rows.append(row)
            continue
        
        if hasrownames:
            rownames.append(row[0])
            row = row[1:]
            
        if autoconvert:
            try:    # see if it's an int
                cseq, rowmask = seq_astype(row, type=int, na=na, nastring=nastring, navalue=navalue)
                rows.append(cseq)
                if rowmask is not None:
                    mask.append(rowmask)
                else:
                    mask.append([0]*len(cseq))
            except ValueError:
                try:    # see if it's a float
                    cseq, rowmask = seq_astype(row, type=float, na=na, nastring=nastring, navalue=navalue)
                    rows.append(cseq)
                    if rowmask is not None:
                        mask.append(rowmask)
                    else:
                        mask.append([0]*len(cseq))
                except ValueError:
                    try:    # see if it's a complex number
                        cseq, rowmask = seq_astype(row, type=complex, na=na, nastring=nastring, navalue=navalue)
                        rows.append(cseq)
                        if rowmask is not None:
                            mask.append(rowmask)
                        else:
                            mask.append([0]*len(cseq))
                    except ValueError:  # can't handle it so raise Error
                        print row
                        raise ValueError("Unable to auto-convert table at Row %d. Try again with autoconvert=False" % i)
        else:
            rows.append(row)    

    class TableData(list):
        pass
    
    r = TableData(rows)
    r.data = rows
    r.mask = None
    r.header = None
    r.rownames = None               
    if na:
        r.mask = mask
    if hasheader:
        r.header = header
    if hasrownames:
        r.rownames = rownames
    return r           

def strip_last_empty (rowiter, delimiter="\t"):
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
    """Seq of strings -> Seq w/strings converted to given type.
    """
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
        graph.add(g, i, j, W[i][j])
    return g
            

def getDiameterPath(G, first = None):
    """Given a weighted tree calculates the diameter path.  Returns: (diampath, length).
    
    The diameter path is the longest of all shortest-paths in the tree.
    
    Calculation is via a double hanging path on the tree.

    The tree should be represented in the dictionary of dictionaries format.
    """
    if first is None:
        first = random.choice(G.keys())
    
    d, p  = Dijkstra(G, first)
 
    td = zip(d.values(), d.keys())
    dmax = max(td)
 
    second = dmax[1]
    d,p = Dijkstra(G, second)
    td = zip(d.values(), d.keys())
 
    dmax = max(td)
    furthest = dmax[1]

    return shortest_path_dijkstra(G, second, furthest), dmax[0]    


def Dijkstra(graph, start, end=None):
   

    D = {}    # dictionary of final distances
    P = {}    # dictionary of predecessors
    Q = PriorityDict()   # est.dist. of non-final vert.
    Q[start] = 0
    
    for v in Q:
        
        D[v] = Q[v]
        
        if v == end: break
        
        for w in graph[v]:
            
            vwLength = D[v] + graph[v][w]
           
            if w in D:
                if vwLength < D[w]:
                    raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
            elif w not in Q or vwLength < Q[w]:
                Q[w] = vwLength
                P[w] = v
    
    return (D,P)


def shortest_path_dijkstra(graph,start,end):
    """Find a single shortest path from the given start vertex
    to the given end vertex.

    The input has the same conventions as Dijkstra().
    The output is a list of the vertices in order along
    the shortest path.
    
    Returns None on failure.
    """

    D,P = Dijkstra(graph,start,end)
    Path = []
    try:
        while 1:
            Path.append(end)
            if end == start: break
            end = P[end]
    except KeyError:
        return None
    Path.reverse()
    return Path



def adjacent(W, u):
    return list(np.nonzero(np.greater(W[u],0)))



# Priority dictionary using binary heaps
# David Eppstein, UC Irvine, 8 Mar 2002

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




def diameterpath_branches(tree, diampath):
    """Given a tree and a diameter path, find the branches of the tree that lie
    off of the diameter path.
    """
    tgraph = copy.deepcopy(tree)
    branches = {}
    for node in diampath:
    
        branches[node] = []

        for n in graph.neighbors(tree, node):
            if n not in diampath:
                #print "matrixops->diameter_branches->tgraph:"
                
                graph.deledge(tgraph, n, node)
                reachable, pred = Dijkstra(tgraph, n)
                branches[node].append(reachable.keys())                
    
    subgraphs = {}
    edges = graph.edges(tree)
    weights = [graph.weight(tree, e[0], e[1]) for e in graph.edges(tree)]
    for root in branches.keys():
        subgraphs[root] = []
        for branch in branches[root]:
            subg = graph.subgraph(tree, branch)
            subgraphs[root].append(subg)
    
    class Results:
        pass

    results = Results()
    results.branches = branches
    results.subgraphs = subgraphs
    return results    

def make_pqtree(mstree):
    """Builds a PQ-tree by walking along the diameter path indecisive backbone
    of a MST.
    """
    # find diameter path
    diampath, dpl = getDiameterPath(mstree)

    # find indecisive backbone
    backbone = indecisive_backbone(mstree, diampath)

    if backbone is None:
        return Qnode(diampath)

    # find diampath branches
    dpbranches = diameterpath_branches(mstree, backbone)

    pqtree = []
    #for root in dpbranches.subgraphs.keys():
    for root in backbone:
        pqtree.append(Pnode( [Qnode((root,))] + \
                 Pnode([make_pqtree(s) for s in dpbranches.subgraphs[root]]) ))

    return Qnode(pqtree)

class Qnode(list):
    def __repr__(self):
        return str(tuple(self))

class Pnode(list):
    pass

def indecisive_backbone(G, diameterpath):
    """Given a tree and the diameter path of that tree,
    returns the "indecisive backbone" of the diameter path.

    The indecisive backbone is defined as the largest continuous set of vertices on 
    the diameter path for which the first and last vertices are either both of
    degree >= 3, both of degree == 1, or if there is only one vertex of degree >= 3, then
    that vertex alone.

    Returns None if none of the diameter path nodes are indecisive.

    """

    #find first indecisive vertex
    firstidx = None
    ct = 0
    for vertex in diameterpath:
        if graph.degree(G, vertex) >= 3:
            firstidx = ct
            break
        ct += 1

    if firstidx is None:
        return None

    #find last indecisive vertex
    opp = diameterpath[:]
    opp.reverse()
    lastidx = None

    ct = 0
    for vertex in opp:
        if graph.degree(G, vertex) >= 3:
            lastidx = ct
            break
        ct += 1

    lastidx = diameterpath.index(opp[ct])
    
    return diameterpath[firstidx:lastidx+1]

def calc_noise_ratio(graph,branch_list):
    
    keys=graph.keys()
    MST_points=len(keys)
    
    branch_points=0
    
    for sublist in branch_list:
        for sub_sub_list in sublist:
            branch_points += len(sub_sub_list)
   
    return float(round(((branch_points/MST_points)*100),2))


def calc_sampling_intesity_ratio(graph,diamPath):
    
    total_path_len=0
    path_num=0
    
    for key,value in graph.iteritems():
        
        if len(value) !=0:
            for node, path_len in value.iteritems():
                total_path_len +=path_len
                path_num +=1
        
    
   
    
    avg_path_len=round(total_path_len/path_num,2)
    intensity_ratio=round(avg_path_len/diamPath[1],2)
    return intensity_ratio
    


