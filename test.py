'''
Created on 02-Jun-2018

@author: Neharika Mazumdar
'''
from __future__ import division
import implementations.matrixOperations as mOp
import implementations.kMeansClustering as kMeansclustering
import implementations.progressionSimilarity as progressionSimilarity
import implementations.executeMethods as ex
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, session
from flask.templating import render_template
from flask import request, redirect, url_for,flash,send_from_directory
from collections import OrderedDict

app = Flask(__name__)

def trythisMag():
    
    alpha = ex.readFromFile('jellyrolltest.txt', 'option1')#mOp.tableasrows('dataC.csv',',', autoconvert=True, hasrownames=False)
    
    #alpha = np.transpose(np.array(alpha))
    dataset=np.array(alpha)
    
    #print dataset[0]
    
    distMat=mOp.getDistanceMatrix(alpha)
    #print ""
    #print "len of distMat::"
    #print len(distMat)
    #print "distance matrix::"
    #print distMat
    
    graph=mOp.getMST(range(len(distMat)),distMat)
    #print "graph:"
    #print graph
    
    #print "diameter path:"
    diamPath=mOp.getDiameterPath(graph,0)
    print diamPath[0]
    tupDiampath=tuple(diamPath[0])

    results=mOp.diameterpath_branches(graph, tupDiampath)     
    branchList=results.branches.values()
     
    return diamPath[0], dataset

    
def pq(distMat,graph):
    
    perm_list=[[]]
    pqtree = mOp.make_pqtree(graph)
    print ""
    print "PQ TREE::"
    print pqtree
    pqperm = mOp.pqtree_perms(pqtree)
    print ""
    print "pq_perm::"
    print pqperm
    rpaths = mOp.rank_paths(pqperm, distMat)
    
    for i in range(10):
        #print i, rpaths.paths[i], rpaths.lengths[i]
        perm_list.append(rpaths.paths[i])     
    
    perm_list.pop(0)
    for i in perm_list:
        print i
    
def trythis():
    dataSet=mOp.tableasrows("finalExpr.csv", ",", autoconvert=True) 
    #print "dataset::"
    #print np.array(dataSet)
    
    geneModulesOutput1=kMeansclustering.getCoherentGeneModules(dataSet)
    #print "0th element of genemodules after clustering (threshold c1)::"
    #print geneModulesOutput1[0]
    geneModulesOutput1.pop(0)
    #print "module set before checking for threshold c2::"
    #print np.array(geneModulesOutput1)
    
    
    geneModulesFinal=kMeansclustering.calculatePairwiseModuleCorrelation(geneModulesOutput1)
    #print "final coherent modules:"
    #print np.array(geneModulesFinal)
    print len(geneModulesFinal)
    
    mst=progressionSimilarity.getMSTlist(geneModulesFinal)
    #print np.array(mst)
    concDict=progressionSimilarity.getProgressionSimilarityDict(geneModulesFinal,mst)
    progMat=progressionSimilarity.getProgressionSimilarityMatrix(geneModulesFinal,concDict)
    #np.set_printoptions(threshold=np.inf)
    print np.array(progMat)
    print len(progMat)
    draw(progMat)
    
#     distSquareMatrix=progressionSimilarity.reorderProgressionSimilarityMatrix(progMat)
#     print np.array(distSquareMatrix)
    
def draw(mat):
#     H = np.array([[1, 2, 3, 4],
#               [5, 6, 7, 8],
#               [9, 10, 11, 12],
#               [13, 14, 15, 16]])  # added some commas and array creation code

    fig = plt.figure(figsize=(6, 3.2))
    
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(mat)
    #ax.set_aspect('equal')
    plt.colorbar()
    plt.show()


@app.route("/",methods=['GET','POST'])
def main():
    
    input_dict={}
    output_dict=OrderedDict()
    order, input_data=trythisMag()
    print order
    order_list=list(order)
    order_list=[int(x) for x in order_list]
    
    print ""
    print "input data::"
    
    for i in range(len(input_data)):
        print i
        temp_list=list(input_data[i])
        temp_list=[float(x) for x in temp_list]
        input_dict[i]=temp_list
    
    print input_dict
    
    
    print ""
    print "output data::"
    
    
    
    return render_template('try.html',input=input_dict,order=order_list)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
 
    #session.init_app(app)
    app.run(debug=False)      

