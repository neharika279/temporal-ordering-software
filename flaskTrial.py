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
            return render_template('method_select.html')
    
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
    if request.method == 'POST':
        param_dict={}
        #filePath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        param_dict["L"]= int(request.form["L"])
        param_dict["c"]= float(request.form["c"])
        param_dict["p"]= float(request.form["p"])
        param_dict["mod"]= int(request.form["mod"])
        p_dict=json.dumps(param_dict)
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


@app.route('/mstUploads')
def exec_mst():
    
    msg=""
    progMat=[[]]
    pq_orderings={}
    input_dict={}
    filename=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    dataset=ex.readFromFile(filename, filetype, labeltype)
    dPath,edges,mst,branch,label_dict=ex.executeBasicMST(dataset)
    
    dataset=np.array(dataset)
    
    labels_info=json.dumps(label_dict)
    
    mst={int(k):{int(i):float(j) for i,j in v.items()} for k,v in mst.items()}
    mst_graph=json.dumps(mst)
    
    dPath=[int(i) for i in dPath]
    
    e,nodes=ex.get_nodes_and_edges(edges)
    ordering=ex.get_complete_ordering(dPath,mst)
    
    o=json.dumps(ordering)
    
    noise,intensity=ex.get_path_stats(mst)
    
    
    for i in range(len(dataset)):
        #print i
        temp_list=list(dataset[i])
        temp_list=[float(x) for x in temp_list]
        input_dict[i]=temp_list
    
    return render_template('results.html',branch=branch,mstgraph=mst_graph,progMat=progMat,mtd="mst", labels_info=labels_info,value=dPath,nodes=nodes,edges=e,ordering=o,noise=noise,intensity=intensity,filename=filename,filetype=filetype,msg=msg)
    #return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    
@app.route("/noiseThreshold/<filename>/<filetype>/<noise>", methods=["POST"])
def noiseThreshold(filename,filetype,noise):
    
    msg=""
    pq_orderings={}
    dPath,edges,mst=ex.executeBasicMST(filename,filetype)
    dPath=[int(i) for i in dPath]
    e,nodes=ex.get_nodes_and_edges(edges)
    ordering=ex.get_complete_ordering(dPath,mst)
    o=json.dumps(ordering)
    noise,intensity=ex.get_path_stats(filename, filetype)

    slider_value= request.form["name_of_slider"]
    
    
    if float(noise)<float(slider_value):
        
        msg="Noise ratio below threshold. Diameter path best order estimate"
        
        return render_template('results.html', value=dPath,nodes=nodes,edges=e,ordering=o,noise=noise,intensity=intensity,filename=filename,filetype=filetype,msg=msg)
    else:
        
        pq_ranks=exec_pq_trees(filename, filetype)
        pq=json.dumps(pq_ranks)
        
        #print ""
        #print "pq ranks:"
        
        for o in range (len(pq_ranks)):
            print pq_ranks[o]
            pq_orderings[o]=ex.get_complete_ordering(pq_ranks[o],mst)
            
        print ""
        print "ordering for each option::"
        print pq_orderings
        pq_orders=json.dumps(pq_orderings)
        return render_template('resultspq.html',value=dPath,nodes=nodes,edges=e,ordering=o,noise=noise,intensity=intensity,filename=filename,filetype=filetype,msg=msg,pq=pq,pq_orders=pq_orders)
    #return slider_value
            
@app.route('/clusterMSTUploads/<param_dict>')    
def exec_clusterMST(param_dict):
    
    mtd="spd"
    o={}
    msg=""
    filename=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    dataset=ex.readFromFile(filename, filetype, labeltype)
    
    dpath,edges,label_dict,progMat,graph,branch=ex.spd(dataset,param_dict)
    
    result_graph=json.dumps(graph)
    noise,intensity=ex.get_path_stats(graph)
    
    labels_info=json.dumps(label_dict)
    e,nodes=ex.get_nodes_and_edges(edges)
    
    return render_template('results.html',branch=branch,mstgraph=result_graph,progMat=progMat,mtd=mtd,labels_info=labels_info,value=dpath,nodes=nodes,edges=e,ordering=o,noise=noise,intensity=intensity,filename=filename,filetype=filetype,msg=msg)

@app.route('/clusterOrderingUploads')    
def exec_clusterOrdering():
    
    progMat=[[]]
    o={}
    noise=0
    intensity=0
    msg=""
    filename=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    dataset=ex.readFromFile(filename, filetype, labeltype)
    
    dpath,edges,label_dict,graph,branch=ex.cst(dataset)
    
    result_graph=json.dumps(graph)
    noise,intensity=ex.get_path_stats(graph)
    labels_info=json.dumps(label_dict)
    e,nodes=ex.get_nodes_and_edges(edges)
    return render_template('results.html',branch=branch,mstgraph=result_graph,progMat=progMat,mtd="cst",labels_info=labels_info,value=dpath,nodes=nodes,edges=e,ordering=o,noise=noise,intensity=intensity,filename=filename,filetype=filetype,msg=msg)

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
 
    return render_template('analyzeResults.html',orderDistMat=distmat,dimRead=dimension_reading,order=order,nodes=nodes,edges=e,backbone=backbone,d_i=di_json)

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
    app.run(debug=False)