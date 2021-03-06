'''
Created on 18-Dec-2017

@author: Neharika Mazumdar
'''
import os,ast,shutil
import json
import importlib
from flask import Flask, session, Blueprint
from flask.templating import render_template
from flask import request, redirect, url_for,flash,send_from_directory,send_file
from werkzeug.utils import secure_filename
from implementations import executeMethods as ex
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import path
from sklearn.decomposition import PCA as sklearnPCA
from implementations.executeMethods import get_indecisive_backbone,get_decisive_indecisive_nodes
import faulthandler
from implementations import config


ALLOWED_EXTENSIONS = set(['txt','csv', 'fa','fas','fasta'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
#app.config['SERVER_NAME']='localhost:9000'

url_extn=config.URL_EXTENSION


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
        option=request.form['options']
        session['filetype']=option
        method_name=request.form['methodoptions']
        session['method']=method_name
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        
        file_list=request.files.getlist('file')
        
        for item in file_list:
            if item.filename == '':
                flash('No selected file')
                return redirect(request.url)
        
        if(option=='option4'):
            
            uploads_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'hostfiles')
            session['filepath']=uploads_dir
            
            if os.path.exists(uploads_dir) and os.path.isdir(uploads_dir):
                shutil.rmtree(uploads_dir)
            
            os.makedirs(uploads_dir)
            
            for item in file_list: 
                if item and allowed_file(item.filename):
                    filename = secure_filename(item.filename)
                    item.save(os.path.join(uploads_dir, filename))

        
        else:
            data_file = file_list[0]
            if data_file and allowed_file(data_file.filename):
                filename = secure_filename(data_file.filename)
                session['filename']=filename
                filePath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                session['filepath']=filePath
                data_file.save(filePath)
        
            
        return redirect(url_extn+url_for('exec_method_final',method=method_name))
    
    else:
        return render_template('home.html')

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)

@app.route('/visualize')
def visualize():
    filePath=os.path.join(app.config['UPLOAD_FOLDER'], "jellyroll.txt")
    session['filepath']=filePath
    
    session['label']='nolabel'
    session['filetype']='option1'
    session['method']='all'
    
    return redirect(url_extn+url_for('exec_method_final',method='all'))

@app.route("/citation")
def citation():
    return render_template('citation.html')

@app.route("/help")
def help():
    return render_template('help.html')

@app.route("/error/<errorMessage>")
def error(errorMessage):
    return render_template('error.html',errorMessage=errorMessage)


@app.route('/show_scree_plot_page')
def show_scree_plot_page():
    return render_template('screePlot.html')


@app.route('/exec_method_final/<method>')
def exec_method_final(method):
    
    #print "method:"
    #print method
    param_dict={}
    param_dict["L"]= 10
    param_dict["c"]= 0.8
    param_dict["p"]= 0.002
    param_dict["mod"]= 5
    param_json = json.dumps(param_dict)
    filetype=session['filetype']

    if(method=='all'):
        return render_template('finalResults_new.html',paramDict=param_json,method_name=method,file_type=filetype)



@app.route('/get_serialization_values',methods=['POST'])
def get_serialization_values():
    
    request_data = json.loads(request.data)
    param_dict = request_data["param_dict"]
    method_name=request_data["method_name"]
    distance_type=request_data["distance_type"]
    dimension_factor=request_data["dimension_factor"]
    
    response_data={}
    mst_values={}
    cst_values={}
    spd_values={}
    
    if(method_name=="mst"):
        
        mst_branch,mst_graph,mst_progMat,mst_labels_info,mst_dPath,mst_nodes,mst_e,mst_noise,mst_intensity,mst_dlen=getSerialization("mst", param_dict,distance_type,dimension_factor)
        
        mst_values["branch"]=mst_branch
        mst_values["graph"]=mst_graph
        mst_values["progmat"]=mst_progMat
        mst_values["labels"]=mst_labels_info
        mst_values["dpath"]=mst_dPath
        mst_values["nodes"]=mst_nodes
        mst_values["edges"]=mst_e
        mst_values["noise"]=mst_noise
        mst_values["intensity"]=mst_intensity
        
        response_data["mst"]=mst_values
        
    elif(method_name=="cst"):
        
        cst_branch,cst_graph,cst_progMat,cst_labels_info,cst_dPath,cst_nodes,cst_e,cst_noise,cst_intensity,cst_dlen=getSerialization("cst", param_dict,distance_type,dimension_factor)
        
        cst_values["branch"]=cst_branch
        cst_values["graph"]=cst_graph
        cst_values["progmat"]=cst_progMat
        cst_values["labels"]=cst_labels_info
        cst_values["dpath"]=cst_dPath
        cst_values["nodes"]=cst_nodes
        cst_values["edges"]=cst_e
        cst_values["noise"]=cst_noise
        cst_values["intensity"]=cst_intensity
        
        response_data["cst"]=cst_values
        
    elif(method_name=="spd"):
        
        spd_branch,spd_graph,spd_progMat,spd_labels_info,spd_dPath,spd_nodes,spd_e,spd_noise,spd_intensity,spd_dlen=getSerialization("spd", param_dict,distance_type,dimension_factor)
        
        spd_values["branch"]=spd_branch
        spd_values["graph"]=spd_graph
        spd_values["progmat"]=spd_progMat
        spd_values["labels"]=spd_labels_info
        spd_values["dpath"]=spd_dPath
        spd_values["nodes"]=spd_nodes
        spd_values["edges"]=spd_e
        spd_values["noise"]=spd_noise
        spd_values["intensity"]=spd_intensity
        
        response_data["spd"]=spd_values
    
    elif(method_name=="all"):
        
        mst_branch,mst_graph,mst_progMat,mst_labels_info,mst_dPath,mst_nodes,mst_e,mst_noise,mst_intensity,mst_dlen=getSerialization("mst", param_dict,distance_type,dimension_factor)
        cst_branch,cst_graph,cst_progMat,cst_labels_info,cst_dPath,cst_nodes,cst_e,cst_noise,cst_intensity,cst_dlen=getSerialization("cst", param_dict,distance_type,dimension_factor)
        spd_branch,spd_graph,spd_progMat,spd_labels_info,spd_dPath,spd_nodes,spd_e,spd_noise,spd_intensity,spd_dlen=getSerialization("spd", param_dict,distance_type,dimension_factor)
        
        mst_values["branch"]=mst_branch
        mst_values["graph"]=mst_graph
        mst_values["progmat"]=mst_progMat
        mst_values["labels"]=mst_labels_info
        mst_values["dpath"]=mst_dPath
        mst_values["nodes"]=mst_nodes
        mst_values["edges"]=mst_e
        mst_values["noise"]=mst_noise
        mst_values["intensity"]=mst_intensity
        mst_values["dlen"]=mst_dlen
        
        cst_values["branch"]=cst_branch
        cst_values["graph"]=cst_graph
        cst_values["progmat"]=cst_progMat
        cst_values["labels"]=cst_labels_info
        cst_values["dpath"]=cst_dPath
        cst_values["nodes"]=cst_nodes
        cst_values["edges"]=cst_e
        cst_values["noise"]=cst_noise
        cst_values["intensity"]=cst_intensity
        cst_values["dlen"]=cst_dlen
        
        spd_values["branch"]=spd_branch
        spd_values["graph"]=spd_graph
        spd_values["progmat"]=spd_progMat
        spd_values["labels"]=spd_labels_info
        spd_values["dpath"]=spd_dPath
        spd_values["nodes"]=spd_nodes
        spd_values["edges"]=spd_e
        spd_values["noise"]=spd_noise
        spd_values["intensity"]=spd_intensity
        spd_values["dlen"]=spd_dlen
        
        response_data["mst"]=mst_values
        response_data["cst"]=cst_values
        response_data["spd"]=spd_values
        
    response_data["method_name"]=method_name
    writeResultToFile(response_data)
    
    return json.dumps(response_data)
        
def writeResultToFile(response):
    
    method_name=response["method_name"]
    filePath=os.path.join(app.config['UPLOAD_FOLDER'], "results.txt")
    exists = os.path.isfile(filePath)
    if exists:
        f = open(filePath, "a")
    else:
        f = open(filePath, "w")
    if method_name=="all":
        
        methodValues_mst=response["mst"];
        f.write("mst method:\n")
        f.write("graph created:"+"\n")
        node_tuple_list_mst=ex.get_node_pairs(methodValues_mst["graph"])
        
        for node_tup in node_tuple_list_mst:
            f.write(str(node_tup[0])+"-"+str(node_tup[1])+"\n")
        
        f.write("diameter path ordering:"+str(methodValues_mst["dpath"])+"\n")
        f.write("diameter path length:"+str(methodValues_mst["dlen"])+"\n")
        f.write("noise percentage:"+str(methodValues_mst["noise"])+"\n")
        f.write("sampling intensity:"+str(methodValues_mst["intensity"])+"\n")
        f.write("\n")
        
        methodValues_cst=response["cst"];
        f.write("cst method:\n")
        
        f.write("graph created:"+"\n")
        node_tuple_list_cst=ex.get_node_pairs(methodValues_cst["graph"])
        
        for node_tup in node_tuple_list_cst:
            f.write(str(node_tup[0])+"-"+str(node_tup[1])+"\n")
        
        
        f.write("diameter path ordering:"+str(methodValues_cst["dpath"])+"\n")
        f.write("diameter path length:"+str(methodValues_cst["dlen"])+"\n")
        f.write("\n")
        
        methodValues_spd=response["spd"];
        f.write("spd method:\n")
        
        f.write("graph created:"+"\n")
        node_tuple_list_spd=ex.get_node_pairs(methodValues_spd["graph"])
        
        for node_tup in node_tuple_list_spd:
            f.write(str(node_tup[0])+"-"+str(node_tup[1])+"\n")
        
        
        f.write("diameter path ordering:"+str(methodValues_spd["dpath"])+"\n")
        f.write("diameter path length:"+str(methodValues_spd["dlen"])+"\n")
        f.write("\n")
    else:
        methodValues=response[method_name];
        f.write(method_name+"method:\n")
        f.write("graph created:"+str(methodValues["graph"])+"\n")
        f.write("diameter path ordering:"+str(methodValues["dpath"])+"\n")
        f.write("noise percentage:"+str(methodValues["noise"])+"\n")
        f.write("sampling intensity:"+str(methodValues["intensity"])+"\n")
        f.write("\n")
    
    f.close() 


##Takes in  5 parameters: method name, parameters for SPD, distance type for sequence data (default is hamming), the dimension count for MDS embedding (default is 3)
##argument param_dict is a dictionary that will have the following parameter specifications:
##L (key) : number of iterations for consensus clustering (value)
##c (key) = threshold for cluster merging (value)
##p (key) = threshold for concordance measure (value)
##mod (key) = number of final modules for the seriation (value)
##Standard values for above SPD parameters:
##L:100; c:0.8; p:0.0002; mod:5
def getSerialization(method_name,param_dict,distance_type,dimension_factor):
    
    progMat=[]
    input_dict={}
    filename=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
     
    dataset=ex.readFromFile(filename, filetype, labeltype,distance_type,dimension_factor)
    

    if(method_name=="mst"):
        dPath,edges,mst,branch,label_dict,dlen=ex.executeBasicMST(dataset)
        
    
    elif(method_name=="cst"):
        
        dPath,edges,label_dict,mst,branch,dlen=ex.cst(dataset)
 
        
    elif(method_name=="spd"):
        
        dPath,edges,label_dict,progMat,mst,branch,dlen=ex.spd(dataset,param_dict)
     
    
    dataset=np.array(dataset)
    labels_info=json.dumps(label_dict)
     
    mst_graph={int(k):{int(i):float(j) for i,j in v.items()} for k,v in mst.items()}
    dPath=[int(i) for i in dPath]
    e,nodes=ex.get_nodes_and_edges(edges)
    noise,intensity=ex.get_path_stats(mst,dPath,dlen)
     
    for i in range(len(dataset)):
        temp_list=list(dataset[i])
        temp_list=[float(x) for x in temp_list]
        input_dict[i]=temp_list
        
    return branch,mst_graph,progMat,labels_info,dPath,nodes,e,noise,intensity,dlen


def analyze_final(order,graph,distance_type,dimension_factor):
    
    result={}
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    order=list(int(k) for k in order)
    
    
    alpha=ex.readFromFile(filepath, filetype, labeltype,distance_type,dimension_factor)
    graph_new={int(k):{int(i):float(j) for i,j in v.items()} for k,v in graph.items()}
    dataset=np.array(alpha)
    
    distmat=ex.get_order_dist_mat(dataset, order)
    dimension_reading=ex.get_order_dimension_readings(dataset, order)
   
    backbone=get_indecisive_backbone(graph_new,order)
    di=get_decisive_indecisive_nodes(graph_new)
    
    edges=ex.get_edges(graph_new)
    e,nodes=ex.get_nodes_and_edges(edges)
    di_json=json.dumps(di)
    
    result["distmat"]=distmat
    result["dimensions"]=dimension_reading
    result["backbone"]=backbone
    result["di"]=di_json
    result["nodes"]=nodes
    result["edges"]=e
    
    filePath=os.path.join(app.config['UPLOAD_FOLDER'], "results.txt")
    f = open(filePath, "a")
    f.write("Pairwise distance matrix for each row in the input data for the ordering"+str(order)+":\n")
    f.write(str(distmat)+"\n")
    f.write("Maximum distance value:"+str(np.array(distmat).max())+","+"Minimum distance value:"+str(np.array(distmat).min())+"\n\n")
    f.close()
    
    return result

@app.route('/get_unordered_analysis_data',methods=['POST'])
def get_unordered_analysis_data():
    
    unordered=[]
    request_data = json.loads(request.data)
    distance_type=request_data["distance_type"]
    dimension_factor=request_data["dimension_factor"]
    response_data={}
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    alpha=ex.readFromFile(filepath, filetype, labeltype,distance_type,dimension_factor)
    dataset=np.array(alpha)
    
    for i in range(len(dataset)):
        unordered.append(i)

    distmat_unordered=ex.get_order_dist_mat(dataset, unordered)
    dimension_reading_unordered=ex.get_order_dimension_readings(dataset, unordered)
    
    response_data["distmat_unordered"]=distmat_unordered
    response_data["dimension_reading_unordered"]=dimension_reading_unordered
    response_data["unordered"]=unordered
   
    return json.dumps(response_data)
   
    
@app.route('/analyze_all_final',methods=['POST']) 
def analyze_all_final():
    
    request_data = json.loads(request.data)
    ordering=request_data["ordering"]
    graph=request_data["graph"]
    distance_type=request_data["distance_type"]
    dimension_factor=request_data["dimension_factor"]
    
    response=analyze_final(ordering,graph,distance_type,dimension_factor)
    
    return json.dumps(response)  


@app.route('/pca', methods=['POST'])
def get_pca():
    
    pca_matrix=[]
    error=0
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    request_data = json.loads(request.data)
    #print "request data in /pca:"
    #print request_data
    ordering = request_data["order"]
    distance_type=request_data["distance_type"]
    dimension_factor=request_data["dimension_factor"]
    pca_dimension_count=request_data["pca_dimension_count"]
    
    order=ex.parse_order(ordering)
    order=list(int(k) for k in order)
   
    alpha=ex.readFromFile(filepath, filetype, labeltype,distance_type,dimension_factor)
    dataset=np.array(alpha)
    
    for orderno in order:
        
        pca_matrix.append(dataset[orderno])
    
    
    data_columns=len(pca_matrix[0])
    if (data_columns >= pca_dimension_count):
        sklearn_pca = sklearnPCA(n_components=pca_dimension_count)
        Y_sklearn = sklearn_pca.fit_transform(pca_matrix)
        final_pca_values=np.transpose(Y_sklearn)
        final_pca_values=list(list(float(f) for f in d) for d in final_pca_values)
    elif(data_columns == 2):
        sklearn_pca = sklearnPCA(n_components=2)
        Y_sklearn = sklearn_pca.fit_transform(pca_matrix)
        final_pca_values=np.transpose(Y_sklearn)
        final_pca_values=list(list(float(f) for f in d) for d in final_pca_values)
    else:
        error=1
        final_pca_values=[]
    
    
    #print "final pca values:"
    #print np.array(final_pca_values)
    filePath=os.path.join(app.config['UPLOAD_FOLDER'], "results.txt")
    f = open(filePath, "a")
    f.write("PCA matrix for the ordering"+str(order)+"for "+str(len(final_pca_values))+"principal components:\n")
    f.write(str(np.transpose(final_pca_values))+"\n\n")
    f.close()
    
    response_data={}
    response_data["pca_values"]=final_pca_values
    response_data["error_value"]=error
   
    return json.dumps(response_data)


@app.route('/getTransposedDistance', methods=['POST'])
def get_transposed_distance_mat():
    
    ordering_matrix=[]
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    request_data = json.loads(request.data)
    ordering = request_data["order"]
    distance_type=request_data["distance_type"]
    dimension_factor=request_data["dimension_factor"]
    
    order=ex.parse_order(ordering)
    order=list(int(k) for k in order)
    
    alpha=ex.readFromFile(filepath, filetype, labeltype,distance_type,dimension_factor)
    dataset=np.array(alpha)
    
    
    for orderno in order:
        
        ordering_matrix.append(dataset[orderno])
    
    trans_ordering_matrix=np.transpose(ordering_matrix)
    
    distmat_new=ex.get_distance_mat(trans_ordering_matrix)
    
    distmat_new=list(list(float(d) for d in r) for r in distmat_new)
    response_data={}
    response_data["distmat"]=distmat_new
    return json.dumps(response_data)


@app.route('/get_only_distMat', methods=['POST'])
def get_only_distMat():
    
    ordering_matrix=[]
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    request_data = json.loads(request.data)
    ordering = request_data["order"]
    distance_type=request_data["distance_type"]
    dimension_factor=request_data["dimension_factor"]
    
    order=ex.parse_order(ordering)
    order=list(int(k) for k in order)
    
    alpha=ex.readFromFile(filepath, filetype, labeltype,distance_type,dimension_factor)
    dataset=np.array(alpha)
    
    distmat=ex.get_order_dist_mat(dataset, order)
    
    distmat=list(list(float(d) for d in r) for r in distmat)
    response_data={}
    response_data["distmat"]=distmat
    return json.dumps(response_data)

@app.route('/get_scree_coordinates', methods=['POST'])
def get_scree_coordinates():
    
    filepath=session['filepath']
    request_data = json.loads(request.data)
    distance_type=request_data["distance_type"]
    
    eigenvals,dimension_count=ex.fetchScreeCoordinates(filepath,distance_type)
    
    eigenvals=list(float(k) for k in eigenvals)
    
    response_data={}
    response_data["eigenvals"]=eigenvals
    response_data["dimension_count"]=int(dimension_count)
    
    return json.dumps(response_data)
    

@app.route('/enteredOrdering', methods=['POST'])
def in_place_analysis():
    
    filepath=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    
    request_data = json.loads(request.data)
    #print "request data in /enteredOrdering:"
    #print request_data
    order = request_data["order"]
    distance_type=request_data["distance_type"]
    dimension_factor=request_data["dimension_factor"]
    #order=ex.parse_order(ordering)
    order=list(int(k) for k in order)
    
    alpha=ex.readFromFile(filepath, filetype, labeltype,distance_type,dimension_factor)
    
    #graph_new={int(k):{int(i):float(j) for i,j in v.items()} for k,v in graph.items()}
    dataset=np.array(alpha)
    
    distmat=ex.get_order_dist_mat(dataset, order)
    dimension_reading=ex.get_order_dimension_readings(dataset, order)
    

    response_data={}
    response_data["distmat"]=distmat
    response_data["dimension_reading"]=dimension_reading
    response_data["order"]=order
    return json.dumps(response_data)

@app.route('/computePQFinal', methods=['POST'])   
def exec_pq_trees_final():
    
    pq_orderings={}
    request_data = json.loads(request.data)
    pqnum = request_data["pqnum"]
    method_name=request_data["methodName"]
    param_dict=request_data["param_dict"]
    distance_type=request_data["distance_type"]
    dimension_factor=request_data["dimension_factor"]
    
    
    filePath=os.path.join(app.config['UPLOAD_FOLDER'], "results.txt")
    f = open(filePath, "a")
    f.write("Alternate orderings using PQ trees:")
    
    if method_name=="mst":
        branch,graph_new,progMat,labels_info,dpath,nodes,e,noise,intensity,dlen=getSerialization("mst", param_dict,distance_type,dimension_factor)  
    elif method_name=="cst":
        branch,graph_new,progMat,labels_info,dpath,nodes,e,noise,intensity,dlen=getSerialization("cst", param_dict,distance_type,dimension_factor)
    elif method_name=="spd":
        branch,graph_new,progMat,labels_info,dpath,nodes,e,noise,intensity,dlen=getSerialization("spd", param_dict,distance_type,dimension_factor)
        
    filename=session['filepath']
    filetype=session['filetype']
    labeltype=session['label']
    pq_ranks,total_paths,total_perms,path_length_list=ex.executePQtree(filename,filetype,labeltype,graph_new,dpath,int(pqnum),distance_type,dimension_factor)
    f.write("Total number of alternate orderings generated: "+str(total_paths)+"\n")
    f.write("Orderings:"+"\n")
    
    if pq_ranks:
        for pqorder in range (len(pq_ranks)):
            
            currentOrder=ex.get_complete_ordering(pq_ranks[pqorder],graph_new)
            pq_orderings[pqorder]=currentOrder        
        #print "pq_orderings:"
        #print pq_orderings
        
    if total_perms:
        for perm in total_perms:
            f.write(str(perm)+",")
            f.write(str(path_length_list[total_perms.index(perm)])+"\n")
    
    pq_orders=json.dumps(pq_orderings)
    pq=json.dumps(pq_ranks)
    f.write("\n")
    f.close()

    response_data={}
    response_data["pqranks"]=pq
    response_data["pqorders"]=pq_orders
    response_data["totalpq"]=total_paths
    return json.dumps(response_data)


#trythis()
if __name__ == '__main__':
    faulthandler.enable()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
 
    #session.init_app(app)
    app.run(host=config.DEFAULT_HOST, port=config.DEFAULT_PORT)