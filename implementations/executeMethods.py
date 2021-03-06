'''
Created on 03-May-2018

@author: Neharika Mazumdar
'''
import matrixOperations as mop
import spd as csp
import cst as cs
from scipy import stats
#import kMeansClustering as kMeans
import json
#import progressionSimilarity as progressionSim
import graphFunctions as graph
import numpy as np

def get_node_pairs(graph):
    
    node_tuple_list=[]
    for key in graph.keys():
        valList=graph[key]
        
        for value in valList:
            
            if key in graph[value]:
                node_tuple_list.append((key,value))
    
    temp_list=[]
    for a,b in node_tuple_list:
        if (a,b) not in temp_list and (b,a) not in temp_list:
            temp_list.append((a,b))
    
    return set(temp_list)

def get_nodes_and_edges(edges):
    
    temp_list=[]
    edges_data={}
    
    for edgeX in edges:
        a,b=edgeX
        temp_list.append(int(a))
        temp_list.append(int(b))
    
    node_list=list(set(temp_list))

    edge_list=list(edges)
    l=len(edge_list)
    for i in range(l):
        edge=list(edge_list[i])
        edge=[int(x) for x in edge]
        edges_data[i]=edge
        
   
    e=json.dumps(edges_data)
    
    
    return e,node_list

def get_complete_ordering(dPath,mst):
    
    ordering={}
    dPath=[int(j) for j in dPath]
    tupDiampath=tuple(dPath)
    results=mop.diameterpath_branches(mst, tupDiampath)
    
    
    for item in dPath:
        order_nodes=[]
        order_nodes.append(item)
        ordering[dPath.index(item)]=order_nodes
     
    branchList=results.branches.values()
     
    if all(subList==[] for subList in branchList):
        print "no branch exists"

    else:
        print"branch exists"
        #print "branches:" 
        
        l=len(dPath)
        for i in range(l):
            if (branchList[i]):
                for k in branchList[i]:
                    if k:
                        for z in k:
                            ordering[i].append(int(z))
   
    
    return ordering   

def executeBasicMST(alpha):
    
    
    
    if(alpha.rownames!=None):
        
        label_dict=get_label_dict(alpha.rownames)
    else:
        label_dict={}
        
    dataset=np.array(alpha)
   # print "MST dataset::"
   # print str(dataset)
    
    distMat=get_distance_mat(alpha)
   # print "MST dist_mat::"
   # print str(distMat)
    
    f = open("temp_Euclidean.txt", "w")
    
    for row in distMat:
        for item in row:
            f.write('%s' % item)
            f.write("\t")
        f.write("\n")
    f.close()
    
    #print "MST distMat:"
    #print distMat
    
    ############################REMOVE LATER###############################
    #distMat=chop(distMat)
    #print "MST chopped distMat:"
    #print distMat
    
    ########################################################################
    
    resultGraph=mop.getMST(range(len(distMat)),distMat)
    #print "result graph:"
    #print resultGraph
    diamPath,diamLength=mop.getDiameterPath(resultGraph)
    
    edges=mop.graph.edges(resultGraph)
    
    branch,branchList=findBranch(resultGraph,diamPath)
    
    return diamPath,edges,resultGraph,branch,label_dict,diamLength

def chop(num_arr):
    
    for i in range(len(num_arr)):
        for j in range(len(num_arr)):
            
            if((float(num_arr[i][j])<(10**-3)) and i!=j):
                num_arr[i][j]=1.5   
    return num_arr

def get_distance_mat(dataset):
    return mop.getDistanceMatrix(dataset)

def findBranch(resultGraph,diamPath):
    

    branch=0
    tupDiampath=tuple(diamPath)
    results=mop.diameterpath_branches(resultGraph, tupDiampath)
    
    branchList=results.branches.values()
     
    if all(subList==[] for subList in branchList):
        branch=0
    else:
        branch=1
        
    return branch,branchList

def get_label_dict(labels):
    
    label_dict={}
    unique_labels=list(set(labels))

    
    for lab in range(len(unique_labels)):
        
        temp_label_list=[]
        
        for l in range(len(labels)):
            
            if(labels[l]==unique_labels[lab]):
                temp_label_list.append(int(l))
    
        label_dict[lab]=list(temp_label_list)
   
    
    return label_dict

############### Reading input data ##########################################
##Takes in  5 parameters: input filename, input filetype, label type, distance type for sequence data, the dimension count for MDS embedding
##argument filetype can have the following values:
##option1 = tab separated values
##option2 = comma separated values
##option3 = sequence data (fasta files)
##label/nolabel : indicates whether input data is labeled into groups/phases

def readFromFile(filePath,filetype,labeltype,distancetype,dimension_scaling_factor):
    if(filetype=='option1'):
        if(labeltype=='nolabel'):
            alpha = mop.tableasrows(filePath,"\t", autoconvert=True, hasrownames=False)
        elif(labeltype=='label'):
            alpha = mop.tableasrows(filePath,"\t", autoconvert=True, hasrownames=True)
    elif(filetype=='option2'):
        if(labeltype=='nolabel'):
            alpha = mop.tableasrows(filePath,",", autoconvert=True, hasrownames=False)
        elif(labeltype=='label'):
            alpha = mop.tableasrows(filePath,",", autoconvert=True, hasrownames=True)
            
    elif(filetype=='option3'):
        alpha=mop.parseSequenceFile(filePath,distancetype,dimension_scaling_factor)
       
    elif(filetype=='option4'):
        alpha=mop.parseSequenceFile(filePath,distancetype,dimension_scaling_factor)
    
    else:
        return -1
    return alpha
 
def fetchScreeCoordinates(filename,distancetype):
    return mop.compute_scree_coordinates(filename,distancetype)
 
def readFromFileSequenceData(filePath,distancetype,dimension_scaling_factor):
    
    alpha=mop.parseSequenceFile(filePath,distancetype,dimension_scaling_factor)
   
    return alpha
 
 
 
 
def get_path_stats(resultGraph,diamPath,diamLength):
    
    noise_to_signal_ratio=0
    intensity_ratio=0
    #alpha=readFromFile(filepath, filetype)
    
    #diamPath,diamLength=mop.getDiameterPath(resultGraph)

    branch,branchList=findBranch(resultGraph, diamPath)
    
    if branch==1:
        noise_to_signal_ratio=mop.calc_noise_ratio(resultGraph, branchList)
        intensity_ratio=mop.calc_sampling_intesity_ratio(resultGraph, diamLength)

            
    return noise_to_signal_ratio,intensity_ratio  
        
def executePQtree(filePath,filetype,labeltype,mst_graph,dpath,pqno,distance_type,dimension_factor):
     
    perm_dict={}
    total_paths=0
    alpha=readFromFile(filePath, filetype,labeltype,distance_type,dimension_factor)
    
     
    distMat=mop.getDistanceMatrix(alpha)
     
    branch,branchList=findBranch(mst_graph, dpath)
     
    if branch==0:
        print "no branches exist"
        pqTree=None
    else:
        print"branch exists"
        perm_list=[]
        total_perm_list=[]
        path_length_list=[]
        pqtree = mop.make_pqtree(mst_graph)
        
        pqperm = mop.pqtree_perms(pqtree)
       
        rpaths = mop.rank_paths(pqperm, distMat)
        total_paths=len(rpaths.paths)
        for i in range(pqno):
            #print i, rpaths.paths[i], rpaths.lengths[i]
            perm_list.append(list(reversed(rpaths.paths[i])))     
        
        for j in range(total_paths):
            #print i, rpaths.paths[i], rpaths.lengths[i]
            total_perm_list.append(list(reversed(rpaths.paths[j])))  
            path_length_list.append(rpaths.lengths[j])   
     
    l=len(perm_list)
    for i in range(l):
        curr_perm=[int(k) for k in perm_list[i]]
        perm_dict[i]=curr_perm
         
    return perm_dict,total_paths,total_perm_list,path_length_list

    
def cst(dataset):
    
    if(dataset.rownames!=None):
        
        label_dict=get_label_dict(dataset.rownames)
    else:
        label_dict={}
    
    dataset = stats.zscore(dataset)
    dataset = np.nan_to_num(dataset)
    
    tcsr =cs.run_cst(dataset,"euclidean","weighted","NearestNeighbors")
    
    graph=get_dict(tcsr)
    cst_edges=mop.graph.edges(graph)
    
    
    dpath,dlen=mop.getDiameterPath(graph)
#     temp_list=[]
#     for p in path:
#         a,b=p
#         if a not in temp_list:
#             temp_list.append(int(a)) 
#         if b not in temp_list:
#             temp_list.append(int(b))
#     
#     dpath=temp_list
    
    branch,branchList=findBranch(graph, dpath)
    
    return dpath,cst_edges,label_dict,graph,branch,dlen

def get_edges(graph):
    return mop.graph.edges(graph)

def get_dict(tcsr):
    
    #############################convert tcsr to dict of dict format########################################
    tcsr_graph_dict={}
    
    for i in range(len(tcsr)):
        
        temp_dict={}
        
        for j in range(len(tcsr)):
            
            tcsr_graph_dict[i]=temp_dict
            
            if(tcsr[i][j]>0.00):
                
                temp_dict[j]=tcsr[i][j]
    #print "graph dict for tcsr:"
    #print tcsr_graph_dict
    return tcsr_graph_dict
    ##########################################################################################################

    
def spd(dataset,param_dict):

    param = json.loads(param_dict)
    print param.get('L')
    
    if(dataset.rownames!=None):
        
        label_dict=get_label_dict(dataset.rownames)
    else:
        label_dict={}
    
    
    dataset = stats.zscore(dataset)
    dataset = np.nan_to_num(dataset)
    dpath,graph,progMat,dlen=csp.run_spd(dataset, "euclidean", param.get('L'), param.get('c'), param.get('p'), param.get('mod'))
     
    result_progMat=list(list(d) for d in progMat)
    
    #newmst=newmst.toarray()
    #graph=get_dict(newmst)
    
    spd_edges=mop.graph.edges(graph)
    
    branch=1
    return dpath,spd_edges,label_dict,result_progMat,graph,branch,dlen


def get_order_dist_mat(dataset,ordering):
    
    #parsed_order=parse_order(ordering)
    
    ordering_matrix=[]
   
 
    for orderno in ordering:
        
        ordering_matrix.append(dataset[orderno])
    
    
    ordering_matrix=np.array(ordering_matrix)
    
    distmat=get_distance_mat(ordering_matrix)
    distmat=list(list(float(d) for d in r) for r in distmat)
    
    
    return distmat

def parse_order(ordering):
    
    order=str(ordering)
    
    for ch in ['[',']']:

        if ch in order:
           
            replaced_order=order.replace(ch,'')
            order=replaced_order
    
    
    ord=replaced_order.split(',')
   
    parsed_order=list(int(k) for k in ord)
    
    return parsed_order

def get_order_dimension_readings(dataset,ordering):

    order_dimension_readings=[]
    #parsed_order=parse_order(ordering)
    
    for orderno in ordering:
        order_dimension_readings.append(dataset[orderno])
    
    trans_order_dimension=np.transpose(order_dimension_readings)
    
    trans_order_dimension=list(list(float(d) for d in r) for r in trans_order_dimension)
    
    return trans_order_dimension

def get_indecisive_backbone(mst,dpath):
    return mop.indecisive_backbone(mst, dpath)


def get_decisive_indecisive_nodes(mst):
    return mop.decisive_indecisive(mst)


