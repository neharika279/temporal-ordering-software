'''
Created on 30-Sep-2017

@author: Neharika Mazumdar
'''
from __future__ import division
from Bio import SeqIO
import sys,re,os
from os import listdir
from os.path import isfile,join
import csv,copy
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
import graphFunctions as graph
import random
from scipy.spatial.distance import hamming
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.manifold import MDS
import sequence_distance as seq
from sklearn.preprocessing import Imputer
import config

UPLOAD_FOLDER = config.UPLOAD_FOLDER
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
                                                       
                            list_s=list(s[i])                                    
                            if perm != list_s:
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


def get_int_values_for_pqnodes(seq):
    
    #print "incoming seq:"
    #print type(seq)
    if isinstance(seq, Qnode):
        seq=tuple(seq)
        seq=get_int_values_for_pqnodes(seq)
                
    elif isinstance(seq, Pnode):
        seq=list(seq)
        seq=get_int_values_for_pqnodes(seq)
    
    else:
        for i in seq:
            if isinstance(i, Qnode):
                i=get_int_values_for_pqnodes(i)
                
            elif isinstance(i, Pnode):
                i=get_int_values_for_pqnodes(i)   
            
            
            else:
                if isinstance(i, tuple):
                    i=(int(x) for x in i)
                elif isinstance(i, list):
                    i=[int(y) for y in i]
                else:
                    i=int(i)
      
    return seq

def getGraph():
    
    f = open("jellyroll.txt", 'r')
    rows=[]
    reader=csv.reader(f,delimiter="\t")
    for r in reader:
        rows.append(r)
        
    #print rows
    arrRow=np.array(rows,dtype=float)
    return arrRow



# def get_classical_MDS_eigenvals(A,dimensions):
#     A = A**2
# 
#     # centering matrix
#     n = A.shape[0]
#     J_c = 1./n*(np.eye(n) - 1 + (n-1)*np.eye(n))
#     
#     # perform double centering
#     B = -0.5*(J_c.dot(A)).dot(J_c)
#     
#     # find eigenvalues and eigenvectors
#     for i in range(dimensions):
#         eigen_val = np.linalg.eig(B)[i]
#        
#         eigen_vec = np.linalg.eig(B)[i].T
#         
#     
#     # select top 2 dimensions (for example)
#     PC1 = np.sqrt(eigen_val[0])*eigen_vec[0]
#     PC2 = np.sqrt(eigen_val[1])*eigen_vec[1]
    


def cmdscale(D):
    """                                                                                       
    Classical multidimensional scaling (MDS)                                                  
                                                                                               
    Parameters                                                                                
    ----------                                                                                
    D : (n, n) array                                                                          
        Symmetric distance matrix.                                                            
                                                                                               
    Returns                                                                                   
    -------                                                                                   
    Y : (n, p) array                                                                          
        Configuration matrix. Each column represents a dimension. Only the                    
        p dimensions corresponding to positive eigenvalues of B are returned.                 
        Note that each dimension is only determined up to an overall sign,                    
        corresponding to a reflection.                                                        
                                                                                               
    e : (n,) array                                                                            
        Eigenvalues of B.                                                                     
                                                                                               
    """
    # Number of points                                                                        
    n = len(D)
 
    # Centering matrix                                                                        
    H = np.eye(n) - np.ones((n, n))/n
 
    # YY^T                                                                                    
    B = -H.dot(D**2).dot(H)/2
 
    # Diagonalize                                                                             
    evals, evecs = np.linalg.eigh(B)
 
    # Sort by eigenvalue in descending order                                                  
    idx   = np.argsort(evals)[::-1]
    evals = evals[idx]
    evecs = evecs[:,idx]
 
    # Compute the coordinates using positive-eigenvalued components only                      
    w, = np.where(evals > 0)
    L  = np.diag(np.sqrt(evals[w]))
    V  = evecs[:,w]
    Y  = V.dot(L)
 
    return Y, evals


def compute_scree_coordinates(filename,distance_type):
    
    if not filename.endswith("fas") and not filename.endswith('fasta') and not filename.endswith('fa'):
            #print(input)
            sys.exit("Warning! The above file may not be in fasta format. Exiting")
    else:
        print filename
        seqs=parseInput(filename,False)
       
        seq_distance_matrix=get_dist(seqs,distance_type)
        dimensions=len(seq_distance_matrix)
        Y,eigenvals=cmdscale(seq_distance_matrix)

    return eigenvals,dimensions


def calc_hausdorff_matrix(seqDict,onlyFiles):
    
    num_files=len(onlyFiles)
    host_hausdorff_matrix=np.zeros([num_files,num_files],float) 
    
    for i in range(num_files):
        for j in range(num_files):
            
            host1_seqs=seqDict[onlyFiles[i]]
            host2_seqs=seqDict[onlyFiles[j]]
    
            h_dist1=hausdorff(host1_seqs, host2_seqs)
            h_dist2=hausdorff(host2_seqs, host1_seqs)

            host_hausdorff_matrix[i][j]=(h_dist1+h_dist2)/2.0
            
    
    #print "hausdorff host matrix:"
    #print host_hausdorff_matrix
    return host_hausdorff_matrix

def hausdorff(a,b):
    
    x_max=0.00
    
    for i in a:
        for j in b:
            #print i,j
            diff=seq.Tamuradistance(str(i), str(j))#abs(i-j)
            if diff>x_max:
                x_max=diff
                
                a_element=i
    
   
    
    x_min=x_max+10
    
    for k in b:
        min_diff=seq.Tamuradistance(str(a_element),str(k))#abs(a_element-k)
        if min_diff<x_min:
            x_min=min_diff
            
            b_element=k
    
            
    
    #print "a_element:",a_element
    #print "b_element:",b_element
    h_dist=seq.Tamuradistance(str(a_element), str(b_element))#abs(a_element-b_element)
    #print 'h_dist:',h_dist
    return h_dist

    
def parseSequenceFile(filePath,distancetype,dimension_scaling_factor):
    
    if os.path.isdir(filePath):                                                                                 #found folder
        #print "found folder"
        
        onlyfiles = [join(filePath, f) for f in listdir(filePath) if isfile(join(filePath, f))]
        #print onlyfiles
        
        seqsDict={}
        for input in onlyfiles:
        
            if not input.endswith("fas") and not input.endswith('fasta') and not input.endswith('fa'):
                sys.exit("Warning! The above file may not be in fasta format. Exiting")
            else:
                seqsDict[input]=parseInput(input,False)
        
        #print seqsDict
        
        seq_distance_matrix=calc_hausdorff_matrix(seqsDict, onlyfiles)
        #print "seq_distance_matrix::"
        #print str(seq_distance_matrix)
        
        
    else:                                                                                                           #found file
        #print "found file"
    
        if not filePath.endswith("fas") and not filePath.endswith('fasta') and not filePath.endswith('fa'):
                #print(input)
                sys.exit("Warning! The above file may not be in fasta format. Exiting")
        else:
            print filePath
            seqs=parseInput(filePath,False)
            print "number of seqs read:"
            print len(seqs)
           
            seq_distance_matrix=get_dist(seqs,distancetype)
            #print "seq_distance_matrix::"
            #print str(seq_distance_matrix)
        
    
    #embedding = MDS(n_components=dimension_scaling_factor,dissimilarity='precomputed')
    #MDS_fix_matrix=embedding.fit_transform(seq_distance_matrix)
    
    MDS_fix_matrix=MDSEmbedding(dimension_scaling_factor, seq_distance_matrix)
    
    
    
    resultFilePath=os.path.join(UPLOAD_FOLDER, "results.txt")
    f_res = open(resultFilePath, "a")
    f_res.write("Genetic distance matrix for distance type "+distancetype+":\n")
    f_res.write(str(np.array(seq_distance_matrix))+"\n\n")
    f_res.write("MDS embedded co-ordinate points in "+str(dimension_scaling_factor)+"space:\n")
    f_res.write(str(np.array(MDS_fix_matrix))+"\n\n")
    f_res.close()
    
    MDSFilePath=os.path.join(UPLOAD_FOLDER, "temp_MDS_file.txt")
    
    if os.path.exists(MDSFilePath):
        os.remove(MDSFilePath)
        
    f = open(MDSFilePath, "w")
    
    for row in MDS_fix_matrix:
        for item in row:
            f.write('%s' % item)
            f.write("\t")
        f.write("\n")
    f.close()
    
    alpha = tableasrows(MDSFilePath,"\t", autoconvert=True, hasrownames=False)
    
    return alpha
        
def MDSEmbedding(dimension_factor,distance_matrix):
    embedding = MDS(n_components=dimension_factor,dissimilarity='precomputed',metric=True,random_state=42)
    MDS_fix_matrix=embedding.fit_transform(distance_matrix)
    
    return MDS_fix_matrix

       
def parseInput(input_file,freq): #get sequences from a file
    if not freq:
        seqs=[]    
        with open(input_file) as input_handle:
            for record in SeqIO.parse(input_handle, "fasta"): 
                seqs.append(record.seq)
        
    else:
        seqs={}
        with open(input_file,'r') as f:
            for record in SeqIO.parse(f,'fasta'):
                freq = int(re.findall('_(\d*)$', record.id)[0])
                seqs[record.seq]=freq
                
    
    return seqs


def get_dist(seqs,distancetype):
    
    l=len(seqs)
    seq_distance_matrix=np.zeros([l,l],float) 
    
    if(distancetype=='hamming'):
        for i in range(l):
            for j in range(l):
                #seq_hamming_matrix[i][j]=hamming(str(seqs[i]), str(seqs[j]))
                seq_distance_matrix[i][j]=seq.hamming_distance(str(seqs[i]), str(seqs[j]))
    elif(distancetype=='p'):
        for i in range(l):
            for j in range(l):
                
                seq_distance_matrix[i][j]=seq.pdistance(str(seqs[i]), str(seqs[j]))
    elif(distancetype=='jc'):
        for i in range(l):
            for j in range(l):
                
                seq_distance_matrix[i][j]=seq.JukesCantordistance(str(seqs[i]), str(seqs[j]))
    elif(distancetype=='tn'):
        for i in range(l):
            for j in range(l):
                
                seq_distance_matrix[i][j]=seq.TajimaNeidistance(str(seqs[i]), str(seqs[j]))
    elif(distancetype=='t'):
        for i in range(l):
            for j in range(l):
                
                seq_distance_matrix[i][j]=seq.Tamuradistance(str(seqs[i]), str(seqs[j]))
      
    return seq_distance_matrix
        
def preprocess(dataset):
    
    for i in range(len(dataset)):
        for j in range(len(dataset[i])):
            
            if(dataset[i][j]==''):
                dataset[i][j]=0.0
                
    imp_mean_nan = Imputer(missing_values=np.nan, strategy='mean')
    imp_mean_zero = Imputer(missing_values=0.0, strategy='mean')
    #imp_mean_empty = Imputer(missing_values='', strategy='mean')
    
    #dataset=imp_mean_empty.fit_transform(dataset)
    dataset=imp_mean_nan.fit_transform(dataset)
    dataset=imp_mean_zero.fit_transform(dataset)
    
    
    return dataset


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
            
            for r in range(len(row)):
                if row[r]=="":
                    row[r]=0.0
        else:
            for r in range(len(row)):
                if row[r]=="":
                    row[r]=0.0
            
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
    
    rows=preprocess(np.array(rows))
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
     
    #p_eud=np.sqrt(R+np.transpose(R) - 2*Q)
    
    p_eud=pairwise_distances(dataset,metric='euclidean')
    #print "euclidean matrix"
    
    #print "p_eud len:"
    #print len(p_eud)
    
    #print p_eud
    return p_eud


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
    #print "graph:"
    #print G
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
    diampath=[int(d) for d in diampath]
    # find indecisive backbone
    backbone = indecisive_backbone(mstree, diampath)
#     print "backbone:"
#     print backbone
#     print "type of backbone:"
#     print type(diampath)
#     print "type of backbone elements:"
#     print type(backbone[0])

    if backbone is None:
        return Qnode(diampath)
    
    backbone=[int(b) for b in backbone]
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

def decisive_indecisive(mst):
    
    d_i={"d":[],"i":[]}
    
    node_list=mst.keys()
    
    for vertex in node_list:
        if graph.degree(mst, vertex) >= 3:
            d_i.get("i").append(vertex)
        else:
            d_i.get("d").append(vertex)

    return d_i

def calc_noise_ratio(graph,branch_list):
    
    keys=graph.keys()
    MST_points=len(keys)
    branch_points=0
    
    for sublist in branch_list:
        for sub_sub_list in sublist:
            branch_points += len(sub_sub_list)
    
    return float(round(((branch_points/MST_points)*100),2))


def calc_sampling_intesity_ratio(graph,diamLen):
    
    total_path_len=0
    path_num=0
    
    for key,value in graph.iteritems():
        
        if len(value) !=0:
            for node, path_len in value.iteritems():
                total_path_len +=path_len
                path_num +=1
        
    
   
    print "diamPath[1]::::"
    print diamLen
    avg_path_len=round(total_path_len/path_num,2)
    intensity_ratio=round(avg_path_len/diamLen,2)
    return intensity_ratio
    


