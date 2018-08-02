#import cst_lib as cst
from implementations import kMeansClustering as km
from implementations import matrixOperations as mop
from implementations import executeMethods as ex
from flask import Flask, session,request
from flask.templating import render_template
from flaskTrial import mst
import numpy as np
from sklearn.decomposition import PCA as sklearnPCA
import json
app = Flask(__name__)


def main():
    
    #dataset=mop.tableasrows("dataC.csv",",", autoconvert=True)
    
    #print "dataset:"
    #print dataset
    data=ex.readFromFile("alphamod.txt","option1","label")
    c_dpath,cst_edges,label_dict,graph=ex.cst(data)
    
    cst_n,cst_i=ex.get_path_stats(graph)
    
   
    #print ""
    #print "tcsr edges:"
    #print cst_edges
    
    print "cst diampath:"
    print c_dpath
    print "cst stats:"
    print cst_n,cst_i
    #print "cst path length:"
    #print len(cst_path)
    
    
    #ex.executeClusterMST(dataset)
################################################################label management##########################################################################   
#     label_dict={}
#     
#     alpha=ex.readFromFile("alphamod.txt","option1","label")
#     labels=alpha.rownames
#     unique_labels=list(set(alpha.rownames))
#     print labels
#     print unique_labels
#     
#     for lab in range(len(unique_labels)):
#         
#         temp_label_list=[]
#         
#         for l in range(len(labels)):
#             
#             if(labels[l]==unique_labels[lab]):
#                 temp_label_list.append(int(l))
#     
#         label_dict[lab]=list(temp_label_list)
#     print ""
#     print "label_dict:"
#     print label_dict
#     labels_info=json.dumps(label_dict)
#######################################################################################################################################################
    
    diamPath,edges,resultGraph,branch,label_dict=ex.executeBasicMST(data)
    mst_n,mst_i=ex.get_path_stats(resultGraph)
    #result_dataset=list(list(d) for d in dataset)
    #print ""
    #print "result graph:"
    #print resultGraph
    #print "mst edges:"
    #print edges
    print "mst diampath:"
    print diamPath
    print "mst graph"
    print resultGraph
    print "mst stats:"
    print mst_n,mst_i
    #print "diampath length:"
    #print len(diamPath)
#     ex.executePQtree("alpha.txt", "option1")
    param_dict={}
    param_dict["L"]=10
    param_dict["c"]=0.8
    param_dict["p"]=0.002
    param_dict["mod"]=5
    param_dict=json.dumps(param_dict)
    dpath,spd_edges,label_dict,result_progMat,s_graph=ex.spd(data,param_dict)
    spd_n,spd_i=ex.get_path_stats(s_graph)
    #newmst=spd_edges.toarray()
    print ""
    print "spd diameter path:"
    print dpath
    print "spd mst:"
    print s_graph
    print "spd stats:"
    print spd_n,spd_i
#     print "spd path length:"
#     print len(spd_path)
#     print "mst:"
#     print newmst
#     print "type of mst:"
#     print type(newmst)
#     print "len of mst:"
#     print len(newmst)
    labels_info=json.dumps(label_dict)
    e_cst,nodes_cst=ex.get_nodes_and_edges(cst_edges)
    e_spd,nodes_spd=ex.get_nodes_and_edges(spd_edges)
    e_mst,nodes_mst=ex.get_nodes_and_edges(edges)
    
    
    
    #return render_template('signup.html')

    #return render_template('tryall.html',dataset=result_dataset,labels=labels_info,cst_path=e_cst,cst_nodes=nodes_cst,spd_path=e_spd,spd_nodes=nodes_spd,mst_path=e_mst,mst_nodes=nodes_mst)

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
@app.route("/",methods=['GET','POST'])
def pca():
    
    data=[[1,2.3,4,-5.7],[3,5.8,-2.0,1],[7.9,6,10,1.7]]
    sklearn_pca = sklearnPCA(n_components=3)
    Y_sklearn = sklearn_pca.fit_transform(data)
    print "pca:"
    print Y_sklearn
    print type(Y_sklearn)
    print type(Y_sklearn[0])
    print type(Y_sklearn[0][0])
    data_new=list(list(float(f) for f in d) for d in Y_sklearn)
    print data_new
    return render_template('signUp.html',data=data_new)
    
#@app.route("/",methods=['GET','POST'])
def signUp():
    dataset=[[1,2,3],[4,5,6]]
    r_dataset=list(list(d) for d in dataset)
    pqDict={}
    pqDict[0]=23
    pqDict[1]=14
    print "pqDict before going to html:"
    print pqDict
    json.dumps(pqDict)
    return render_template('signUp.html',dataset=r_dataset,pqDict=pqDict)

@app.route('/ajaxTrial', methods=['POST'])
def ajaxTrial():
    
    request_data = json.loads(request.data)
    dataset = request_data["dataset"]
    pqDict = request_data["pqDict"]
    print "ajax dataset after getting ajax request:"
    print dataset
    print "ajax pqDict after getting ajax request:"
    print pqDict
    pqPerm={}
    pqPerm[0]=12.5
    pqPerm[1]=2
    response_data={}
    response_data["pqperm"]=pqPerm
    response_data["status"]="ok"
    return json.dumps(response_data);

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

   
    
if __name__ == "__main__": 
    app.run(debug=False)
#main()