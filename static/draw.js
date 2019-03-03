var globalNodelist=[];
var globalEdges=[];
var globalDPath=[];

/************************************************MAIN REPRESENTATIONS**************************************/
function treeView(orderedDivName,divName,checkBoxName){//(nodes,edges,dPath,labels){
	
	var checkBox = document.getElementById(checkBoxName);
	var orderedDiv=document.getElementById(orderedDivName);
	var groupedDiv=document.getElementById(divName);
	if (checkBox.checked == true) {
		//drawWithoutLabels(nodes,edges,dPath);
		groupedDiv.style.visibility="hidden";
		orderedDiv.style.visibility="visible";
		
		}
	else if(checkBox.checked == false){
		//drawWithLabels(nodes,edges,dPath,labels);
		groupedDiv.style.visibility="visible";
		orderedDiv.style.visibility="hidden";
	}
}

function drawWithoutLabels(nodes,edges,dPath,orderedDivName){
	
	globalNodelist=nodes;
	globalEdges=edges;
	globalDPath=dPath;
	
	var dict = []; // create an empty array
	var arrayLength = nodes.length;
	var order_edges={};
	var orderLen=dPath.length;
	
	for (var i = 0; i < orderLen-1; i++) {
		tempList=[];
		tempList.push(dPath[i]);
		tempList.push(dPath[i+1]);
		order_edges[i]=tempList;
	}
	for (var i = 0; i < arrayLength; i++) {
		if(dPath.includes(nodes[i])){
			dict.push({
		    id:   nodes[i],
		    label: String(nodes[i]),
		    color: {
		        border: '#00CC66',
		        background: '#00CC66'
		      }
			});
		}
		else{
			dict.push({
		    id:   nodes[i],
		    label: String(nodes[i]),
		    color: {
		        border: '#C0C0C0',
		        background: '#C0C0C0'
		      }
			});
		}		
	}
	// create an array with nodes
	var final_nodes = new vis.DataSet(dict);	
	// create an array with edges
	var result_edges=JSON.parse(edges);	
	var edge_dict=[];
	var edgeArrayLen=Object.keys(result_edges).length;
	var edgeOrderArrayLen=Object.keys(order_edges).length;

	for (var i = 0; i < edgeArrayLen; i++) {	
		edge_dict.push({
		from:   result_edges[i][0],
	    to: result_edges[i][1],
	    //arrows:"from"
		});
		
	}
	var final_edges = new vis.DataSet(edge_dict);
	// create a network
	var container = document.getElementById(orderedDivName);
	// provide the data in the vis format
	var data = {
	    nodes: final_nodes,
	    edges: final_edges
	};
	var options = {};
	// initialize your network!
	var network = new vis.Network(container, data, options);
	
}


function drawWithLabels(nodes,edges,dPath,labels,divName){
	
	colors = ["red","blue","green","yellow","orange","black"];
	var dict = [];
	var arrayLength = nodes.length;
	var result_labels=JSON.parse(labels);
	var labelArrayLen=Object.keys(result_labels).length;
	
	if(isEmpty(result_labels)){
		for (var i = 0; i < arrayLength; i++) {
			dict.push({
				id:   nodes[i],
				label: String(nodes[i]),
				color: {
					border: '#C0C0C0',
					background: '#C0C0C0'
				}
			});
		}
	}
	else{
		for (var i = 0; i < labelArrayLen; i++) {
			var labelList=result_labels[i];
			var labelArrayLength = labelList.length;
			
			for (var j = 0; j < labelArrayLength; j++) {
				dict.push({
				id:   labelList[j],
				label: String(labelList[j]),
				color: {
					border: colors[i],
				    background: colors[i]
				    }
				});	
			}	
		}
	}
	var final_nodes = new vis.DataSet(dict);
	var result_edges=JSON.parse(edges);
	var edge_dict=[];
	var edgeArrayLen=Object.keys(result_edges).length;
	
	for (var i = 0; i < edgeArrayLen; i++) {
		edge_dict.push({
		from:   result_edges[i][0],
	    to: result_edges[i][1]
		});
	}
	
	var final_edges = new vis.DataSet(edge_dict);
	var container = document.getElementById(divName);
	
	// provide the data in the vis format
	var data = {
	    nodes: final_nodes,
	    edges: final_edges
	};
	var options = {};
	
	// initialize your network!
	var network = new vis.Network(container, data, options);
}

function recomputePCA(pcaDivID,savedorderID,PCA_selectID){
	
	var PCA_dim = document.getElementById(PCA_selectID);
	var selected_dim = PCA_dim.options[PCA_dim.selectedIndex].value;
	//console.log(selected_dim);
	order=document.getElementById(savedorderID).value;
	selected_distance=document.getElementById("saved_distanceType").value;
	dimension_factor=document.getElementById("saved_dimensionFactor").value;
	getPCAForOrder(order,pcaDivID,selected_distance,dimension_factor,parseInt(selected_dim));
}

function getPCAForOrder(order,pcaDivID,selected_distance,dimension_factor,pca_dimension_count){
	
	var ordering = String("["+String(order)+"]");
	
	post_data = {}
    post_data["order"] = ordering;
    //post_data["graph"] = graph_dict
    post_data["distance_type"] = selected_distance;
    post_data["dimension_factor"] = parseInt(dimension_factor);
    post_data["pca_dimension_count"] = parseInt(pca_dimension_count);
    
    $.ajax({
        url: '/pca',
        data:JSON.stringify(post_data),
        type: 'POST',
        contentType:"text/json",  
        success: function(response){
        	//console.log(response);
        	drawPCA(response,pcaDivID);
        },
        error: function(error) {
            console.log(error);
        }
    });
	
}

function drawPCA(response,pcaDivID){
	
	var chartData=[];
	var res_response=JSON.parse(response);
	//console.log(res_response);
	var data=res_response["pca_values"];
	var error=res_response["error_value"];
	var c = ["red","green","yellow"];
	
	if(parseInt(error)===1){
		
		var para = document.createElement("P");   
		var t = document.createTextNode("Too few columns in original dataset"); 
		para.appendChild(t); 
		document.getElementById(para).style.color = "black";
		document.getElementById(pcaDivID).appendChild(para);
	}
	else{
		var layout = {
				autosize: false,
				width: 500,
				height: 300,
				margin: {
					b: 10,
				    t: 20,
				    pad:4
				},
				xaxis: {
				    title: 'PC1',
				    automargin: true,
				    titlefont: {
				      family: 'Courier New, monospace',
				      size: 18,
				      color: 'black'
				    }
				 },
				 yaxis: {
					    title: 'PC2',
					    automargin: true,
					    titlefont: {
					      family: 'Courier New, monospace',
					      size: 18,
					      color: 'black'
					    }
				},
				zaxis: {
					    title: 'PC3',
					    automargin: true,
					    titlefont: {
					      family: 'Courier New, monospace',
					      size: 18,
					      color: 'black'
					    }
				}
			};
			var dataLen=data.length;
			//console.log(dataLen);
			if(dataLen==3){
				var PCAdata=[{
					  type: 'scatter3d',
					  //mode: 'lines',
					  x: data[0],
					  y: data[1],
					  z: data[2],
					  opacity: 1,
					  line: {
					    width: 6,
					    color: "yellow",
					    reversescale: false
					  }
					}];
			}
			else if(dataLen==2){
				var PCAdata=[{
					  type: 'scatter',
					  mode: 'lines+markers',
					  x: data[0],
					  y: data[1],
					  opacity: 1,
					  marker: {
						  color: 'yellow',
						  size: 10,
						  line: {
						    width: 4,
						    color: "yellow",
						    reversescale: false
						  }
					  }
					}];
			}
			
			Plotly.newPlot(pcaDivID,PCAdata,layout);

	}
	
	
		
}


/********************************************PQ TREE DISPLAY******************************************************/
function displayPQ(response,pqOrderDivName,orderDivName,pqDivID,orderedDrawDiv,unorderedDrawDiv,pcaDivName,distmatDiv,
		dimensionDiv,distMatCheckbox,tempOrder,selected_distanceType,selected_dimensionFactor) {
	
	var res_response=JSON.parse(response);
	var pqPaths=JSON.parse(res_response["pqranks"]);
	var orders=JSON.parse(res_response["pqorders"]);
	var pqArrayLen=Object.keys(pqPaths).length;
	//var arrStr = encodeURIComponent(JSON.stringify(nodeList));
	var outerpara=document.getElementById(pqDivID);
	document.getElementById(pqOrderDivName).innerHTML="";
	
	if (document.contains(document.getElementById(orderDivName))) {
		//document.getElementById("submitbutton").remove();
		var para=document.getElementById(orderDivName);
		para.innerHTML = "";
	}   else {
		var para = document.createElement("div"); 
		para.id = orderDivName;
		outerpara.appendChild(para);
	}
	
	var nonelabel = document.createElement("label");
	var noneRadio=document.createElement("INPUT");
	noneRadio.setAttribute("type", "radio");
	var br = document.createElement('br');
	noneRadio.setAttribute("value", globalDPath);
	noneRadio.setAttribute("name", "pqperms");
	noneRadio.onclick = function(){ tempSaveOrder(pqOrderDivName,orderedDrawDiv,unorderedDrawDiv,pcaDivName,distmatDiv,
			dimensionDiv,distMatCheckbox,tempOrder,selected_distanceType,selected_dimensionFactor); };
	
	nonelabel.appendChild(noneRadio);
	nonelabel.appendChild(document.createTextNode("Diameter Path"));
	para.appendChild(nonelabel);
	para.appendChild(br);
	
	for (var i = 0; i < pqArrayLen; i++) {
		
		var jsonOrder=JSON.stringify(orders[i]);
		
		var label = document.createElement("label");
		var aTag=document.createElement("INPUT");
		aTag.setAttribute("type", "radio");
		var br = document.createElement('br');
		
		//aTag.setAttribute('href','javascript:drawCurrentChart(\''+jsonOrder+'\',\''+arrStr+'\')');
		//aTag.setAttribute('onclick', 'drawChart(jsonOrder,pqPaths[i])');
		
		aTag.setAttribute("value", pqPaths[i]+"");
		aTag.setAttribute("name", "pqperms");
		//console.log(aTag.value);
		aTag.onclick = function(){ tempSaveOrder(pqOrderDivName,orderedDrawDiv,unorderedDrawDiv,pcaDivName,distmatDiv,
				dimensionDiv,distMatCheckbox,tempOrder,selected_distanceType,selected_dimensionFactor); };
		
		label.appendChild(aTag);
		label.appendChild(document.createTextNode("path"+(i+1)));
		para.appendChild(label);
		para.appendChild(br);
			
	}
}

function tempSaveOrder(pqOrderDivName,orderedDrawDiv,unorderedDrawDiv,pcaDivName,distmatDiv,
		dimensionDiv,distMatCheckbox,tempOrder,selected_distanceType,selected_dimensionFactor){

	order=document.querySelector('input[name="pqperms"]:checked').value
	//console.log(order);
	orderList=[];
	
	orderArray=order.split(",");
	for(var i=0; i<orderArray.length; i++) { 
		//orderArray[i] = +myArray[i]; 
		orderList.push(parseInt(orderArray[i], 10));
	} 
	//console.log(orderList);
	document.getElementById(tempOrder).value=order;
	document.getElementById(pqOrderDivName).innerHTML=order;
	
	drawWithoutLabels(globalNodelist,globalEdges,orderList,orderedDrawDiv);
	
	document.getElementById(unorderedDrawDiv).style.visibility="hidden";
	document.getElementById(orderedDrawDiv).style.visibility="visible";
	
	getPCAForOrder(orderList,pcaDivName,selected_distanceType,selected_dimensionFactor,3);
	inPlaceAnalysis(orderList,distmatDiv,dimensionDiv,distMatCheckbox,selected_distanceType,selected_dimensionFactor);
}

/*function drawCurrentChart(order,nodeList){
	
	var node=JSON.parse(nodeList);
	var c = document.getElementById("myChart1");
	var ctx = c.getContext("2d");
	ctx.clearRect(0,0,c.width,c.height);
	ctx.beginPath();
	drawChart(order,node);
	
}

function drawChart(order,nodeList){
	
	var ipOrderDict=[];
	var opOrderDict=[];
	var result_order=JSON.parse(order);
	
	
	var nodeListLen=nodeList.length;
	
	for(var i=0; i<nodeListLen; i++){
		
		ipOrderDict.push({
			x:   i,
			y: nodeList[i]
			});
	}
	
	var orderArrayLen=Object.keys(result_order).length;
		
	for (var i in result_order) {
		
		var nodeLen=result_order[i].length;
		
		for (var j = 0; j < nodeLen; j++) {
			
			opOrderDict.push({
			x:   i,
			y: result_order[i][j]
			});
			
		}
			
	}	
	console.log(opOrderDict)
	console.log(ipOrderDict)
	
	
	var x = new Chart(document.getElementById("myChart1"), {
		type: 'scatter',
	   	data: {
	   		datasets: [{
	   			label: "Result Ordering",
	   			data: opOrderDict,
		        fill: false,
		        showLine: true,
		        backgroundColor: 'rgb(30,144,255)',
		        borderColor: 'rgb(30,144,255)'
		     },
		     {
		   			label: "Input Ordering",
		   			data: ipOrderDict,
			        fill: false,
			        showLine: true,
			        backgroundColor: 'rgb(0, 0, 0)',
			        borderColor: 'rgb(0, 0, 0)'
			  }]	
	   	},
	   	options: {
	      responsive: true,
	      scales: {
	    	  yAxes: [{
	    		  scaleLabel: {
	    	      display: true,
	    	      labelString: 'Indices of samples'
	    	      }
	    	  }],
	    	  xAxes: [{
	    		  scaleLabel: {
	    	      display: true,
	    	      labelString: 'Ordering'
	    	      }
	    	  }]
	      }     
	   	}
	});
}
*/

function sliderFunction(noiseInputName,sliderName,pqDivName,msgDivID){
	
	var slide = document.getElementById(sliderName).value;
	var noise=parseFloat(document.getElementById(noiseInputName).value);
	//console.log(slide);
	
	if (noise<slide){
		
		document.getElementById(msgDivID).innerHTML="Noise ratio below threshold. Diameter path best order estimate";
	}
	else{
		
		document.getElementById(pqDivName).style.visibility="visible";
		//displayPQ(counts,pqPerm,pqOrders);
		
	}
}


function spdSliderFunction(divNum){
	
	var slideL = document.getElementById('Lslider').value;
	var slideC = document.getElementById('Cslider').value;
	var slideP = document.getElementById('Pslider').value;
	var num_mod=document.getElementById('mod_num').value;
	
	var selected_distanceType = document.getElementById('saved_distanceType').value;
	var selected_dimensionFactor = document.getElementById('saved_dimensionFactor').value;
	
	var param_dict = {}; // create an empty array

	param_dict["L"] = parseInt(slideL);
	param_dict["c"] = parseFloat(slideC);
	param_dict["p"] = parseFloat(slideP);
	param_dict["mod"] = parseInt(num_mod);
	
	param_dict_string=JSON.stringify(param_dict);
	
	recomputeResults(param_dict_string,'spd',divNum,selected_distanceType,selected_dimensionFactor);
}

/*function enteredOrdering(dim_divId,dist_divID,textID){
	
	//var graph_dict=JSON.parse(graph);
	var ordering = String("["+document.getElementById(textID).value+"]");
	
	post_data = {}
    post_data["order"] = ordering
    //post_data["graph"] = graph_dict
    
    
    $.ajax({
        url: '/enteredOrdering',
        data:JSON.stringify(post_data),
        type: 'POST',
        contentType:"text/json",  
        success: function(response){
        	inPlaceAnalysis(response,dim_divId,dist_divID);
        },
        error: function(error) {
            console.log(error);
        }
    });
}*/

//function computePQ(counts,dpath,graph,pqTextName,pqOrderDivName,orderDivName,pqDivID,orderedDrawDiv,unorderedDrawDiv){
//	
//	//console.log(counts);
//	var graph_dict=JSON.parse(graph);
//	//console.log(graph_dict);
//	var pqnum = document.getElementById(pqTextName).value;
//	//console.log(pqnum)
//	post_data = {}
//    post_data["pqnum"] = pqnum
//    post_data["dpath"] = dpath
//    post_data["graph"] = graph_dict
//	
//	$.ajax({
//        url: '/computePQ',
//        data:JSON.stringify(post_data),
//        type: 'POST',
//        contentType:"text/json",  
//        success: function(response){
//        	displayPQ(counts,response,pqOrderDivName,orderDivName,pqDivID,orderedDrawDiv,unorderedDrawDiv);
//        },
//        error: function(error) {
//            console.log(error);
//        }
//    });
//	
//}

function computePQFinal(paramDict,currentHiddenDiv,pqTextName,pqOrderDivName,orderDivName,pqDivID,orderedDrawDiv,unorderedDrawDiv,
		pcaDivName,distmatDiv,dimensionDiv,distMatCheckbox,tempOrder){
	
	var pqnum = document.getElementById(pqTextName).value;
	//console.log(pqnum)
	
	var selected_distanceType=document.getElementById("saved_distanceType").value;
	var selected_dimensionFactor=document.getElementById("saved_dimensionFactor").value;
	
	post_data = {}
    post_data["pqnum"] = pqnum
    post_data["param_dict"] = paramDict;
	post_data["methodName"] = document.getElementById(currentHiddenDiv).value;
	post_data["distance_type"] = selected_distanceType;
    post_data["dimension_factor"] = parseInt(selected_dimensionFactor);
	
	$.ajax({
        url: '/computePQFinal',
        data:JSON.stringify(post_data),
        type: 'POST',
        contentType:"text/json",  
        success: function(response){
        	displayPQ(response,pqOrderDivName,orderDivName,pqDivID,orderedDrawDiv,unorderedDrawDiv,pcaDivName,distmatDiv,
        			dimensionDiv,distMatCheckbox,tempOrder,selected_distanceType,selected_dimensionFactor);
        },
        error: function(error) {
            console.log(error);
        }
    });
	
}



/********************************************EXTRA ANALYSIS***********************************************/
function inPlaceAnalysis(order,distmatDiv,dimensionDiv,distMatCheckbox,selected_distanceType,selected_dimensionFactor){

	post_data = {}
    post_data["order"] = order;
    post_data["distance_type"] = selected_distanceType;
    post_data["dimension_factor"] = parseInt(selected_dimensionFactor);
  
    $.ajax({
        url: '/enteredOrdering',
        data:JSON.stringify(post_data),
        type: 'POST',
        contentType:"text/json",  
        success: function(response){
        	var res_response=JSON.parse(response);
        	var distmat=res_response["distmat"];
        	var dimension=res_response["dimension_reading"];
        	var res_order=res_response["order"];
        	
        	showDimensions(dimension,order,dimensionDiv);
        	drawDistMat(distmat,distmatDiv);
        	document.getElementById(distMatCheckbox).checked = false;
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function drawBackbone(nodes,edges,backbone,di,backboneDiv){
	
	var dict = [];
	//console.log(edges)
	var result_edges=JSON.parse(edges);
	var result_di=JSON.parse(di);
	var arrayLength = nodes.length;
	var decisive=result_di["d"];
	var indecisive=result_di["i"];
	
	for (var i = 0; i < arrayLength; i++) {
		if(indecisive.includes(nodes[i])){
			if(backbone.includes(nodes[i])){
				dict.push({
					id:   nodes[i],
					label: "I"+"("+String(nodes[i])+")",
					color: {
						border: 'green',
						background: 'green'
					}
				});
			}
			else{
				dict.push({
					id:   nodes[i],
					label: "I"+"("+String(nodes[i])+")",
					color: {
						border: '#C0C0C0',
						background: '#C0C0C0'
					}
				});
			}
		}
		else if(decisive.includes(nodes[i])){
			if(backbone.includes(nodes[i])){
				dict.push({
					id:   nodes[i],
					label: "D"+"("+String(nodes[i])+")",
					color: {
						border: 'green',
						background: 'green'
					}
				});
			}
			else{
				dict.push({
					id:   nodes[i],
					label: "D"+"("+String(nodes[i])+")",
					color: {
						border: '#C0C0C0',
						background: '#C0C0C0'
					}
				});
			}	
		}	
	}
	var final_nodes = new vis.DataSet(dict);
	var edge_dict=[];
	var edgeArrayLen=Object.keys(result_edges).length;
	
	for (var i = 0; i < edgeArrayLen; i++) {
		edge_dict.push({
		from:   result_edges[i][0],
	    to: result_edges[i][1]
		});
	}
	
	var final_edges = new vis.DataSet(edge_dict);
	// create a network
	var container = document.getElementById(backboneDiv);
	var data = {
	    nodes: final_nodes,
	    edges: final_edges
	};
	var options = {};
	
	// initialize your network!
	var network = new vis.Network(container, data, options);
}

function drawScree(response,divId){
	
	var eigenvals=response["eigenvals"];
	var dimension_count=response["dimension_count"];
	
	var data=[];
	var xaxis=[];
	
	for(var i=0;i<dimension_count;i++){
		xaxis.push(i+1);
	}
	
	var trace= {
			x:xaxis,
			y:eigenvals,
			type: 'scattergl',
			mode: 'lines+markers'
	};
	
	data.push(trace);
	
	var layout = {
		
		autosize: false,
		width: 500,
		height: 300,
		margin: {
		    b: 10,
		    t: 20,
		    pad: 4
		},		
		xaxis: {
		    title: 'Dimensions',
		    automargin: true,
		    titlefont: {
		      family: 'Courier New, monospace',
		      size: 18,
		      color: '#7f7f7f'
		    }
		 },
		 yaxis: {
		    title: 'Eigenvalues',
		    automargin: true,
		    titlefont: {
		      family: 'Courier New, monospace',
		      size: 18,
		      color: '#7f7f7f'
		    }
		}	
	};
	
	Plotly.newPlot(divId, data,layout);	
}

function showDimensions(dimRead,order,divID){

	var data=[];
	var xaxis=[];
	var orderLen=order.length;
	//console.log(orderLen);
	var dimensionLen=dimRead.length;
	
	for(var i=0;i<orderLen;i++){
		xaxis.push(i+1);
	}
	
	for(var j=0;j<dimensionLen;j++){
		
		var trace= {
				x:xaxis,
				y:dimRead[j],
				type: 'scattergl'
		};
		
		data.push(trace);
	}
	
	var layout = {
		
		autosize: false,
		width: 500,
		height: 300,
		margin: {
		    b: 10,
		    t: 20,
		    pad: 4
		},	
		xaxis: {
		    title: 'Dimensions',
		    automargin: true,
		    titlefont: {
		      family: 'Courier New, monospace',
		      size: 18,
		      color: 'black'
		    }
		 },
		 yaxis: {
		    title: 'Values',
		    automargin: true,
		    titlefont: {
		      family: 'Courier New, monospace',
		      size: 18,
		      color: 'black'
		    }
		}
		
	};
	
	Plotly.newPlot(divID, data,layout);	
}

function drawDistMat(distmat,divID){
	
	var data = [
		{
			//z: [[1, 20, 30], [20, 1, 60], [30, 60, 1]],
		    z: distmat,
		    type: 'heatmap'
		}
	];
	var layout = {
		autosize: false,
		width: 400,
		height: 300,
		margin: {
	    l: 50,
	    r: 10,
	    b: 25,
	    t: 20,
	    pad: 4
		}
	};

	Plotly.newPlot(divID, data,layout);
}


function drawTransposedMatrix(distDivID,tempOrder,checkbox){
	
	order=document.getElementById(tempOrder).value;
	
	selected_distanceType=document.getElementById("saved_distanceType").value;
	selected_dimensionFactor=document.getElementById("saved_dimensionFactor").value;
	
	post_data = {};
    post_data["order"] = '['+order+']';
    post_data["distance_type"] = selected_distanceType;
    post_data["dimension_factor"] = parseInt(selected_dimensionFactor);
    
    if(document.getElementById(checkbox).checked){
    	
    	 $.ajax({
    	        url: '/getTransposedDistance',
    	        data:JSON.stringify(post_data),
    	        type: 'POST',
    	        contentType:"text/json",  
    	        success: function(response){
    	        	//console.log(response)
    	        	var res_response=JSON.parse(response);
    	        	var distmat=res_response["distmat"];
    	        	drawDistMat(distmat,distDivID);
    	        },
    	        error: function(error) {
    	            console.log(error);
    	        }
    	    });
    }
    else{
    	$.ajax({
	        url: '/get_only_distMat',
	        data:JSON.stringify(post_data),
	        type: 'POST',
	        contentType:"text/json",  
	        success: function(response){
	        	//console.log(response)
	        	var res_response=JSON.parse(response);
	        	var distmat=res_response["distmat"];
	        	drawDistMat(distmat,distDivID);
	        },
	        error: function(error) {
	            console.log(error);
	        }
	    });
    }
   
}

/*function getAnalysisValues(mst_dpath,cst_dpath,spd_dpath,un_dpath){
	
	var leftDiv = document.getElementById("analysis_all_left");
	var rightDiv = document.getElementById("analysis_all_right");
	
	leftDiv.style.visibility="visible";
	rightDiv.style.visibility="visible";
	
	post_data = {};
    post_data["mst_dpath"] = mst_dpath;
    post_data["cst_dpath"] = cst_dpath;
    post_data["spd_dpath"] = spd_dpath;
    post_data["un_dpath"] = un_dpath;
    
    $.ajax({
        url: '/get_analyze_all_parameters',
        data:JSON.stringify(post_data),
        type: 'POST',
        contentType:"text/json",  
        success: function(response){
        	//console.log(response)
        	drawAnalysisAll(response,mst_dpath,cst_dpath,spd_dpath,un_dpath);
        },
        error: function(error) {
            console.log(error);
        }
    });
}*/


function getAnalysisFinal(ordering,graph,distmatDiv,dimensionDiv,backboneDiv,selected_distance,dimension_factor){
	
	post_data = {};
    post_data["ordering"] = ordering;
    post_data["graph"] = graph;
    post_data["distance_type"] = selected_distance;
    post_data["dimension_factor"] = parseInt(dimension_factor);
    
    $.ajax({
        url: '/analyze_all_final',
        data:JSON.stringify(post_data),
        type: 'POST',
        contentType:"text/json",  
        success: function(response){
        	//console.log(response)
        	drawAnalysisFinal(response,distmatDiv,dimensionDiv,backboneDiv,ordering);
        },
        error: function(error) {
            console.log(error);
        }
    });
	
	
}

function drawAnalysisFinal(response,distmatDiv,dimensionDiv,backboneDiv,ordering){
	
	var res_response=JSON.parse(response);
	
	var distmat=res_response["distmat"];
	drawDistMat(distmat,distmatDiv);
	
	var dimread=res_response["dimensions"];
	showDimensions(dimread,ordering,dimensionDiv);
	
	var nodes=res_response["nodes"];
	var edges=res_response["edges"];
	var backbone=res_response["backbone"];
	var di=res_response["di"];
	drawBackbone(nodes,edges,backbone,di,backboneDiv);
	
}




/*function drawAnalysisAll(response,mst_dpath,cst_dpath,spd_dpath,un_dpath){
	
	var res_response=JSON.parse(response);
	
	var distmat_unordered=res_response["distmat_unordered"];
	var distmat_mst=res_response["distmat_mst"];
	var distmat_cst=res_response["distmat_cst"];
	var distmat_spd=res_response["distmat_spd"];
	var distmat_un=res_response["distmat_un"];
	var unordered_list=res_response["unordered_list"];
	
	drawDistMat(distmat_unordered,'distmat-unordered');
	drawDistMat(distmat_mst,'distmat-mst');
	drawDistMat(distmat_cst,'distmat-cst');
	drawDistMat(distmat_spd,'distmat-spd');
	drawDistMat(distmat_un,'distmat-un');
	
	
	var dimread_unordered=res_response["dimension_reading_unordered"];
	var dimread_mst=res_response["dimension_reading_mst"];
	var dimread_cst=res_response["dimension_reading_cst"];
	var dimread_spd=res_response["dimension_reading_spd"];
	var dimread_un=res_response["dimension_reading_un"];
	

	showDimensions(dimread_unordered,unordered_list,'dimension-unordered');
	showDimensions(dimread_mst,mst_dpath,'dimension-mst');
	showDimensions(dimread_cst,cst_dpath,'dimension-cst');
	showDimensions(dimread_spd,spd_dpath,'dimension-spd');
	showDimensions(dimread_un,un_dpath,'dimension-un');
}
*/


/**********************************************NEW METHODS***************************************************/
function computeResultsFinal(paramDict,methodName){
	//console.log(methodName);
	//console.log(typeof paramDict);
	
	var dist = document.getElementById("distance");
	var selected_distance = dist.options[dist.selectedIndex].value;
	var dimension_factor = document.getElementById("dimension_factor").value;
	
	document.getElementById("saved_distanceType").value=selected_distance;
	document.getElementById("saved_dimensionFactor").value=dimension_factor;
	
	post_data = {};
    post_data["param_dict"] = paramDict;
    post_data["method_name"] = methodName;
    post_data["distance_type"] = selected_distance;
    post_data["dimension_factor"] = parseInt(dimension_factor);
    
    $.ajax({
    	url: '/get_serialization_values',
    	data:JSON.stringify(post_data),
    	type: 'POST',
    	contentType:"text/json",  
    	success: function(response){
    		//console.log(response)
    		drawResultsFinal(response,selected_distance,dimension_factor);
    	},
    	error: function(error) {
    		console.log(error);
    	}
    });
}



function recomputeResults(paramDict,methodName,divNum,selected_distanceType,selected_dimensionFactor){
	//console.log(methodName);
	//console.log(typeof paramDict);
	post_data = {};
    post_data["param_dict"] = paramDict;
    post_data["method_name"] = methodName;
    post_data["distance_type"] = selected_distanceType;
    post_data["dimension_factor"] = parseInt(selected_dimensionFactor);
    
    $.ajax({
    	url: '/get_serialization_values',
    	data:JSON.stringify(post_data),
    	type: 'POST',
    	contentType:"text/json",  
    	success: function(response){
    		//console.log(response)
    		var res_response=JSON.parse(response);
    		addDataToDivision(res_response,methodName,divNum,selected_distanceType,selected_dimensionFactor);
    	},
    	error: function(error) {
    		console.log(error);
    	}
    });
}


function drawResultsFinal(response,selected_distance,dimension_factor){
	
	var res_response=JSON.parse(response);
	//console.log(res_response);
	var methodName=res_response["method_name"];
	populateUnorderedAnalysis(selected_distance,dimension_factor);
	
	if(methodName==="all"){
		
		drawThumbnails(res_response,"mst",1);
		drawThumbnails(res_response,"cst",2);
		drawThumbnails(res_response,"spd",3);
		
		addDataToDivision(res_response,"mst",1,selected_distance,dimension_factor);
		addDataToDivision(res_response,"cst",2,selected_distance,dimension_factor);
		addDataToDivision(res_response,"spd",3,selected_distance,dimension_factor);
		
	}
	else{		
		addDataToDivision(res_response,methodName,1,selected_distance,dimension_factor);
	}
	
	
}

function drawThumbnails(parsed_response,methodName,divNum){
	
	var methodValues=parsed_response[methodName];
	var dpath=methodValues["dpath"];
	var nodes=methodValues["nodes"];
	var edges=methodValues["edges"];
	
	var thumbDiv = document.getElementById("myorderednetworkthumb"+String(divNum));
	thumbDiv.style.display="block";
	
	drawWithoutLabels(nodes,edges,dpath,"myorderednetworkthumb"+String(divNum));
}

function addDataToDivision(res_response,methodName,divNumber,selected_distance,dimension_factor){
	
	var methodValues=res_response[methodName];
	//console.log(methodValues);
	
	var branch=methodValues["branch"];
	var graph=methodValues["graph"];
	var progmat=methodValues["progmat"];
	var labels=methodValues["labels"];
	var dpath=methodValues["dpath"];
	var nodes=methodValues["nodes"];
	var edges=methodValues["edges"];
	var noise=methodValues["noise"];
	var progmat=methodValues["progmat"];
	//console.log(progmat);
	//console.log(noise);
	var intensity=methodValues["intensity"];
	
	var mainDiv1 = document.getElementById("mst"+String(divNumber));
	var hiddenInput = document.getElementById("mstmethod"+String(divNumber));
	var treeLabel = document.getElementById("mstLabel"+String(divNumber));
	var pcaLabel = document.getElementById("pcaLabel"+String(divNumber));
	
	if(methodName==="mst"){
		var noiseVal = document.getElementById("noise"+String(divNumber));
		var intensityVal = document.getElementById("intensity"+String(divNumber));
	}
	
	var tempOrder=document.getElementById("savedorder"+String(divNumber));
	if(methodName==="spd"){
		var progMatButton=document.getElementById("progMatButton"+String(divNumber));
	}
	//mainDiv1.style.display="block";
	hiddenInput.value=methodName;
	treeLabel.innerHTML="Minimum Spanning Tree-"+methodName;
	pcaLabel.innerHTML="Distance Matrix-"+methodName;
	
	if(methodName==="mst"){
		noiseVal.value=noise;
		intensityVal.value=intensity;
	}
	
	tempOrder.value=dpath;
	
	drawWithLabels(nodes,edges,dpath,labels,"mynetwork"+String(divNumber));
	drawWithoutLabels(nodes,edges,dpath,"myorderednetwork"+String(divNumber));
	getPCAForOrder(dpath,"pca"+String(divNumber),selected_distance,dimension_factor,3);
	getAnalysisFinal(dpath,graph,"distmat"+String(divNumber),"dimension"+String(divNumber),"backbone"+String(divNumber),selected_distance,dimension_factor);
	
	if(methodName==="spd"){
		progMatButton.style.display="block";
		drawProgMat(progmat,"progmat"+String(divNumber));
	}
}


function populateUnorderedAnalysis(selected_distance,dimension_factor){
	
	post_data = {};
	post_data["distance_type"] = selected_distance;
	post_data["dimension_factor"] = parseInt(dimension_factor);
    
    $.ajax({
    	url: '/get_unordered_analysis_data',
    	data:JSON.stringify(post_data),
    	type: 'POST',
    	contentType:"text/json",  
    	success: function(response){
    		var res_response=JSON.parse(response);
    		var distmat_unordered=res_response["distmat_unordered"];
    		var dimension_reading_unordered=res_response["dimension_reading_unordered"];
    		var unordered=res_response["unordered"];
    		document.getElementById('saved_unordered').value=unordered;
    		
    		showDimensions(dimension_reading_unordered,unordered,'dimension_unordered');
        	drawDistMat(distmat_unordered,'distmat_unordered');
    	},
    	error: function(error) {
    		console.log(error);
    	}
    });
}

function drawProgMat(progMat,progMatDiv){
	
	var data = [
		  {
		    //z: [[1, 20, 30], [20, 1, 60], [30, 60, 1]],
		    z: progMat,
		    type: 'heatmap'
		  }
		];
	var layout = {
			autosize: false,
			width: 400,
			height: 300,
			margin: {
		    l: 50,
		    r: 10,
		    b: 25,
		    t: 20,
		    pad: 4
			}
		};
	Plotly.newPlot(progMatDiv, data,layout);
}


function computeScree(){
	
	var dist = document.getElementById("distance_scree");
	var selected_distance = dist.options[dist.selectedIndex].value;
	post_data = {};
	post_data["distance_type"] = selected_distance;
	
    $.ajax({
    	url: '/get_scree_coordinates',
    	data:JSON.stringify(post_data),
    	type: 'POST',
    	contentType:"text/json",  
    	success: function(response){
    		var res_response=JSON.parse(response);
    		
        	drawScree(res_response,'scree');
    	},
    	error: function(error) {
    		console.log(error);
    	}
    });
}

function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

