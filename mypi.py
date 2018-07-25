'''
Created on Jun 4, 2018

@author: ALI student
'''
from flask import Flask, render_template
import networkx as nx
import json
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import implementations.executeMethods as ex
import io
import base64

#%matplotlib inline

app = Flask(__name__)

@app.route("/")
def index(chartID = 'chart_ID', chart_type = 'spline', chart_height = 500):
    
    #dPath="[2,3,4,5,6]"
    resultFile="graph.png"
    or_list=[]
    dPath,edges=ex.executeBasicMST("jellyrolltest.txt","option1")
    print dPath
    dPath=[int(i) for i in dPath]
    
    str_dPath=''.join(str(e) for e in dPath)
    
    for i in range(len(dPath)):
        or_list.append(i)
    or_list.sort()
    print or_list
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    #series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    series = [{"data": eval(str_dPath)}]
    title = {"text": 'Time Order'}
    xAxis = {}#{"labels":{"enabled":False}}
    yAxis = {"title": {"text": 'yAxis Label'}}
    
    y = [0,1,2,3,4]
    x = [2,3,4,5,6]
    plt.plot(x,y)
    plt.savefig("static/graph.png")
    
    
#     data: [{
#                     x: 0,
#                     y: 5
#                  }, {
#                     x: 5,
#                     y: 10
#                  }, {
#                     x: 8,
#                     y: 5
#                  }, {
#                     x: 15,
#                     y: 0
#                  }]
#    
   
   
   

    return render_template('try1.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, plot_url=resultFile)

    #return p

if __name__ == "__main__":
    app.run(debug=True)

#print index()