'''
Created on 18-Dec-2017

@author: Neharika Mazumdar
'''
import os,ast
import json
import importlib
from flask import Flask, session
from flask.templating import render_template
from flask import request, redirect, url_for,flash,send_from_directory
from werkzeug.utils import secure_filename
from implementations import executeMethods as ex
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import path
from sklearn.decomposition import PCA as sklearnPCA
from implementations.executeMethods import get_indecisive_backbone,\
    get_decisive_indecisive_nodes

UPLOAD_FOLDER = 'C:\Users\Public'
#FILE_NAME=''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['FILE_NAME'] = FILE_NAME

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        
        session['label']=request.form['labeloptions']
        session['filetype']=request.form['options']
        session['method']=request.form['methodoptions']
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            session['filename']=filename
            filePath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            session['filepath']=filePath
            file.save(filePath)
            #return redirect(url_for('uploaded_file',filename=filename))
            #return render_template('method_select.html',value=filename,option=option,label_option=label_option)
           
            return redirect(url_for('exec_method'))
            
            #return render_template('method_select.html')
    
    else:
        return render_template('home.html')

@app.route('/get_file/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER)

@app.route("/citation")
def citation():
    return render_template('citation.html')

@app.route("/error/<errorMessage>")
def error(errorMessage):
    return render_template('error.html',errorMessage=errorMessage)

@app.route("/mst",methods=['GET', 'POST'])
def mst():
    print request.method
    if request.method == 'POST':
        #filePath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return redirect(url_for('exec_mst'))
    
    else:
        return render_template('mst.html')


@app.route("/pq_trees/<filename>/<filetype>",methods=['GET', 'POST'])
def pq_trees(filename,filetype):
    if request.method == 'POST':
        filePath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return redirect(url_for('exec_pq_trees',filename=filePath,filetype=filetype))
    
    else:
        return render_template('pq.html')


@app.route("/clusterMST",methods=['GET', 'POST'])
def clusterMST():
    
    method=session['method']
    
    if request.method == 'POST':
        param_dict={}
        #filePath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        param_dict["L"]= int(request.form["L"])
        param_dict["c"]= float(request.form["c"])
        param_dict["p"]= float(request.form["p"])
        param_dict["mod"]= int(request.form["mod"])
        
        print "took parameters. param dict::"
        print param_dict
        
        p_dict=json.dumps(param_dict)
        
        if(method=='all'):
            return redirect(url_for('exec_all',param_dict=p_dict))
        else:
            return redirect(url_for('exec_clusterMST',param_dict=p_dict))
    
    else:
        
        return render_template('clusterMST.html')

@app.route("/cluster_ordering",methods=['GET', 'POST'])
def cluster_ordering():
    if request.method == 'POST':
        #filePath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return redirect(url_for('exec_clusterOrdering'))
    
    else:
        return render_template('cluster_ordering.html')




@app.route('/exec_method')
def exec_method():
    
    method_type=session['method']
    
    if(method_type=='mst'):
        return redirect(url_for('exec_mst'))
    elif(method_type=='cst'):
        return redirect(url_for('exec_clusterOrdering'))
    else:
        return redirect(url_for('clusterMST')) 
    
@app.route('/exec_all/<param_dict>')    
def exec_all(param_dict):
    
    all_param={}
    print "reached exec all method"
    mst_branch,mst_graph,mst_progMat,mst_labels_info,mst_dPath,mst_nodes,mst_e,mst_noise,mst_intensity=getSerialization("mst", param_dict)
    cst_branch,cst_graph,cst_progMat,cst_labels_info,cst_dPath,cst_nodes,cst_e,cst_noise,cst_intensity=getSerialization("cst", param_dict)
    spd_branch,spd_graph,spd_progMat,spd_labels_info,spd_dPath,spd_nodes,spd_e,spd_noise,spd_intensity=getSerialization("spd", param_dict)
    
    all_param['mst']={'branch':mst_branch,'graph':mst_graph,'progmat':mst_progMat,'labels':mst_labels_info,'dpath':mst_dPath,'nodes':mst_nodes,'edges':mst_e,
                      'noise':mst_noise,'intensity':mst_intensity}
    
    all_param['cst']={'branch':cst_branch,'graph':cst_graph,'progmat':cst_progMat,'labels':cst_labels_info,'dpath':cst_dPath,'nodes':cst_nodes,'edges':cst_e,
                      'noise':cst_noise,'intensity':cst_intensity}
    
    all_param['spd']={'branch':spd_branch,'graph':spd_graph,'progmat':spd_progMat,'labels':spd_labels_info,'dpath':spd_dPath,'nodes':spd_nodes,'edges':spd_e,
                      'noise':spd_noise,'intensity':spd_intensity}
    
   
    
    params=json.dumps(all_param)
    return render_template('results_all.html',params=params)


def getSerialization(method_name,param_dict):
    
    progMat=[]
    input_dict={}
    filename=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
     
    dataset=ex.readFromFile(filename, filetype, labeltype)
    
    if(method_name=="mst"):
    
        dPath,edges,mst,branch,label_dict=ex.executeBasicMST(dataset)
    
    elif(method_name=="cst"):
        
        dPath,edges,label_dict,mst,branch=ex.cst(dataset)
        
    elif(method_name=="spd"):
        
        dPath,edges,label_dict,progMat,mst,branch=ex.spd(dataset,param_dict)
        
     
    
    dataset=np.array(dataset)
    labels_info=json.dumps(label_dict)
     
    mst={int(k):{int(i):float(j) for i,j in v.items()} for k,v in mst.items()}
    mst_graph=json.dumps(mst)
     
    dPath=[int(i) for i in dPath]
     
    e,nodes=ex.get_nodes_and_edges(edges)
    #ordering=ex.get_complete_ordering(dPath,mst)
     
    #o=json.dumps(ordering)
     
    noise,intensity=ex.get_path_stats(mst)
     
     
    for i in range(len(dataset)):
        #print i
        temp_list=list(dataset[i])
        temp_list=[float(x) for x in temp_list]
        input_dict[i]=temp_list
        
    return branch,mst_graph,progMat,labels_info,dPath,nodes,e,noise,intensity


@app.route('/mstUploads')
def exec_mst():
    
    param_dict={}
    branch,mst_graph,progMat,labels_info,dPath,nodes,e,noise,intensity=getSerialization("mst",param_dict)
    return render_template('results.html',branch=branch,mstgraph=mst_graph,progMat=progMat,mtd="mst", labels_info=labels_info,value=dPath,nodes=nodes,edges=e,noise=noise,intensity=intensity)
    #return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    
            
@app.route('/clusterMSTUploads/<param_dict>')    
def exec_clusterMST(param_dict):
    
    branch,mst_graph,progMat,labels_info,dPath,nodes,e,noise,intensity=getSerialization("spd", param_dict)
    return render_template('results.html',branch=branch,mstgraph=mst_graph,progMat=progMat,mtd="spd",labels_info=labels_info,value=dPath,nodes=nodes,edges=e,noise=noise,intensity=intensity)

@app.route('/clusterOrderingUploads')    
def exec_clusterOrdering():
    
    param_dict={}
    branch,mst_graph,progMat,labels_info,dPath,nodes,e,noise,intensity=getSerialization("spd", param_dict)
    return render_template('results.html',branch=branch,mstgraph=mst_graph,progMat=progMat,mtd="cst",labels_info=labels_info,value=dPath,nodes=nodes,edges=e,noise=noise,intensity=intensity)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print "in upload file method"
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


@app.route('/displayResultsPQ/<dPath>/<pq_perm>/<edges>')
def displayResultsPQ(dPath,pq_perm,edges,chartID = 'chart_ID', chart_type = 'spline', chart_height = 500):
    node_list=session.pop('node_list', [])
    
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"data": eval(dPath)}]
    title = {"text": 'Time Order'}
    xAxis = {}#{"labels":{"enabled":False}}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('resultspq.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, value=dPath,nodes=node_list,pq=pq_perm,edges=edges)
 
@app.route('/analyze/<ordering>/<mstgraph>') 
def analyze(ordering,mstgraph):
    
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    order=ex.parse_order(ordering)
    order=list(int(k) for k in order)
    
    distmat_unordered,dimension_reading_unordered,unordered=get_unordered_analysis_data()
    
    alpha=ex.readFromFile(filepath, filetype, labeltype)
    graph=ast.literal_eval(mstgraph)
    graph_new={int(k):{int(i):float(j) for i,j in v.items()} for k,v in graph.items()}
    dataset=np.array(alpha)
    
    distmat=ex.get_order_dist_mat(dataset, ordering)
    dimension_reading=ex.get_order_dimension_readings(dataset, ordering)
    backbone=get_indecisive_backbone(graph_new,order)
    di=get_decisive_indecisive_nodes(graph_new)
    
    edges=ex.get_edges(graph_new)
    e,nodes=ex.get_nodes_and_edges(edges)
    di_json=json.dumps(di)
    graph_json=json.dumps(graph_new)
    #print "bacnkbone:"
    #print backbone
 
    return render_template('analyzeResults.html',orderDistMat=distmat,dimRead=dimension_reading,order=order,nodes=nodes,edges=e,backbone=backbone,d_i=di_json,
                           unordered=unordered,distmat_unordered=distmat_unordered,dimension_reading_unordered=dimension_reading_unordered)


def get_unordered_analysis_data():
    
    unordered=[]
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    alpha=ex.readFromFile(filepath, filetype, labeltype)
    dataset=np.array(alpha)
    
    for i in range(len(dataset)):
        unordered.append(i)

    distmat_unordered=ex.get_order_dist_mat(dataset, unordered)
    dimension_reading_unordered=ex.get_order_dimension_readings(dataset, unordered)
    
    
    return distmat_unordered,dimension_reading_unordered,unordered
    

@app.route('/analyze_all/<params>') 
def analyze_all(params):
    
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    params_new=ast.literal_eval(params)
    
    mst_dpath=params_new["mst"]["dpath"]
    mst_dpath=[int(i) for i in mst_dpath]
    
    cst_dpath=params_new["cst"]["dpath"]
    cst_dpath=[int(i) for i in cst_dpath]
    
    spd_dpath=params_new["spd"]["dpath"]
    spd_dpath=[int(i) for i in spd_dpath]
    
    un_dpath=params_new["spd"]["dpath"]
    un_dpath=[int(i) for i in un_dpath]

    return render_template('analyze_all.html',mst_dpath=mst_dpath,cst_dpath=cst_dpath,spd_dpath=spd_dpath,un_dpath=un_dpath)


@app.route('/get_analyze_all_parameters', methods=['POST']) 
def get_analyze_all_parameters():
    
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    alpha=ex.readFromFile(filepath, filetype, labeltype)
    dataset=np.array(alpha)
    
    distmat_unordered,dimension_reading_unordered,unordered=get_unordered_analysis_data();
    
    request_data = json.loads(request.data)
    mst_dpath = request_data["mst_dpath"]
    cst_dpath = request_data["cst_dpath"]
    spd_dpath = request_data["spd_dpath"]
    un_dpath = request_data["un_dpath"]
    

    distmat_mst=ex.get_order_dist_mat(dataset, mst_dpath)
    dimension_reading_mst=ex.get_order_dimension_readings(dataset, mst_dpath)
    
    distmat_cst=ex.get_order_dist_mat(dataset, cst_dpath)
    dimension_reading_cst=ex.get_order_dimension_readings(dataset, cst_dpath)
    
    distmat_spd=ex.get_order_dist_mat(dataset, spd_dpath)
    dimension_reading_spd=ex.get_order_dimension_readings(dataset, spd_dpath)
    
    distmat_un=ex.get_order_dist_mat(dataset, un_dpath)
    dimension_reading_un=ex.get_order_dimension_readings(dataset, un_dpath)
    
    response_data={}
    
    response_data["unordered_list"]=unordered
    response_data["distmat_unordered"]=distmat_unordered
    response_data["dimension_reading_unordered"]=dimension_reading_unordered
    
    response_data["distmat_mst"]=distmat_mst
    response_data["dimension_reading_mst"]=dimension_reading_mst
    
    response_data["distmat_cst"]=distmat_cst
    response_data["dimension_reading_cst"]=dimension_reading_cst
    
    response_data["distmat_spd"]=distmat_spd
    response_data["dimension_reading_spd"]=dimension_reading_spd
    
    response_data["distmat_un"]=distmat_un
    response_data["dimension_reading_un"]=dimension_reading_un
    
    return json.dumps(response_data)


@app.route('/pca', methods=['POST'])
def get_pca():
    
    pca_matrix=[]
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    request_data = json.loads(request.data)
    ordering = request_data["order"]
    order=ex.parse_order(ordering)
    order=list(int(k) for k in order)
    #print "order:"
    #print order
    alpha=ex.readFromFile(filepath, filetype, labeltype)
    
    dataset=np.array(alpha)
    #print "original dataset:"
    #print  dataset
    
    for orderno in order:
        
        pca_matrix.append(dataset[orderno])
    
    #print "pca_matrix:"
    #print pca_matrix
    
    sklearn_pca = sklearnPCA(n_components=3)
    Y_sklearn = sklearn_pca.fit_transform(pca_matrix)
    
    final_pca_values=np.transpose(Y_sklearn)
    final_pca_values=list(list(float(f) for f in d) for d in final_pca_values)
    response_data={}
    response_data["pca_values"]=final_pca_values
    return json.dumps(response_data)


@app.route('/getTransposedDistance', methods=['POST'])
def get_transposed_distance_mat():
    
    ordering_matrix=[]
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    request_data = json.loads(request.data)
    ordering = request_data["order"]
    order=ex.parse_order(ordering)
    order=list(int(k) for k in order)
    
    alpha=ex.readFromFile(filepath, filetype, labeltype)
    dataset=np.array(alpha)
    
    
    for orderno in order:
        
        ordering_matrix.append(dataset[orderno])
    
    trans_ordering_matrix=np.transpose(ordering_matrix)
    
    distmat_new=ex.get_distance_mat(trans_ordering_matrix)
    
    distmat_new=list(list(float(d) for d in r) for r in distmat_new)
    response_data={}
    response_data["distmat"]=distmat_new
    return json.dumps(response_data)


@app.route('/enteredOrdering', methods=['POST'])
def in_place_analysis():
    
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    request_data = json.loads(request.data)
    ordering = request_data["order"]
    order=ex.parse_order(ordering)
    order=list(int(k) for k in order)
    
    alpha=ex.readFromFile(filepath, filetype, labeltype)
    
    #graph_new={int(k):{int(i):float(j) for i,j in v.items()} for k,v in graph.items()}
    dataset=np.array(alpha)
    
    distmat=ex.get_order_dist_mat(dataset, ordering)
    dimension_reading=ex.get_order_dimension_readings(dataset, ordering)
    

    response_data={}
    response_data["distmat"]=distmat
    response_data["dimension_reading"]=dimension_reading
    response_data["order"]=order
    return json.dumps(response_data)

    
@app.route('/computePQ', methods=['POST'])   
def exec_pq_trees():
    
    pq_orderings={}
    request_data = json.loads(request.data)
    pqnum = request_data["pqnum"]
    graph=request_data["graph"]
    dpath=request_data["dpath"]
    
    graph_new={int(k):{int(i):float(j) for i,j in v.items()} for k,v in graph.items()}
   
    filename=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    pq_ranks,total_paths=ex.executePQtree(filename,filetype,labeltype,graph_new,dpath,int(pqnum))
    
    print "pqranks:"
    print pq_ranks
    print "total pq:"
    print total_paths
    
    if pq_ranks:
        for pqorder in range (len(pq_ranks)):
            
            pq_orderings[pqorder]=ex.get_complete_ordering(pq_ranks[pqorder],graph_new)
                
        #print "pq_orderings:"
        #print pq_orderings
    
    pq_orders=json.dumps(pq_orderings)
    pq=json.dumps(pq_ranks)

    response_data={}
    response_data["pqranks"]=pq
    response_data["pqorders"]=pq_orders
    response_data["totalpq"]=total_paths
    return json.dumps(response_data)


#trythis()
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
 
    #session.init_app(app)
    app.run(debug=True)