var globalNodelist=[];
var globalEdges=[];
var globalDPath=[];

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
	//console.log("order tree");
	//console.log(dPath);
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
		//var index=i;
		order_edges[i]=tempList;
	}
	
	//console.log(order_edges);
	
	for (var i = 0; i < arrayLength; i++) {
		
		//Do something
		//console.log(nodes[i]);
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
	
	//console.log(dict)
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
	
	
	/*for (var i = 0; i < edgeOrderArrayLen; i++) {

		console.log(order_edges[i]);
		console.log(order_edges[i][0]);
		console.log(order_edges[i][1]);
		edge_dict.push({
			from:   order_edges[i][0],
			to: order_edges[i][1],
			arrows:"to"
		});
		//console.log(edge_dict);

	}*/
	
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
	//console.log(globalNodelist);
	//console.log(globalEdges);
}


function drawWithLabels(nodes,edges,dPath,labels,divName){
	//console.log("grouped tree");
	colors = ["red","blue","green","yellow","orange","black"];
	var dict = [];
	var arrayLength = nodes.length;
	var result_labels=JSON.parse(labels);
	//console.log(result_labels);
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
	
	
	
	//console.log(dict)
	// create an array with nodes
	var final_nodes = new vis.DataSet(dict);
	
	// create an array with edges
	
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
	// create a network
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


function drawBackbone(nodes,edges,backbone,di){
	
	var dict = [];
	//console.log(edges)
	var result_edges=JSON.parse(edges);
	var result_di=JSON.parse(di);
	
	//console.log(result_edges);
	//console.log(result_di);
	//console.log(backbone);
	//console.log(nodes);
	
	var arrayLength = nodes.length;
	var decisive=result_di["d"];
	var indecisive=result_di["i"];
	
	//console.log(decisive);
	//console.log(indecisive);
	
	
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
	var container = document.getElementById('backbone');
	
	// provide the data in the vis format
	var data = {
	    nodes: final_nodes,
	    edges: final_edges
	};
	var options = {};
	
	// initialize your network!
	var network = new vis.Network(container, data, options);
	
}



function tableFunctOp(ord,ipDict){
	
	var myTable = document.getElementById("op-table");
	//console.log(ord);
	var order=JSON.parse(ord);
	
	var header = myTable.createTHead();
	
	var row0 = header.insertRow(0);
	var cell0 = row0.insertCell(0);
	var cell01 = row0.insertCell(1);
	var cell02 = row0.insertCell(2);
	cell02.innerHTML = "Dimensions";
    
	var row = header.insertRow(1);
    var cell = row.insertCell(0);
    cell.innerHTML = "Order";
    var cell1 = row.insertCell(1);
    cell1.innerHTML = "Samples";
    
    var dimensionLen = ipDict[0].length;
    
    for(var i=0;i<dimensionLen;i++){
    	
    	var tempCell = row.insertCell(i+2);
    	tempCell.innerHTML = "Dimension"+i;
    }
    
    var orderArrayLen=Object.keys(order).length;
	
    for (var i in order) {
		
		orderList=order[i];
		
		for (var k=0;k<orderList.length;k++){
				
			var tr = document.createElement("tr");
			var tdOrder = document.createElement("td");
			var txtOrder = document.createTextNode(i);
			tdOrder.appendChild(txtOrder);
			tr.appendChild(tdOrder);
			var td0 = document.createElement("td");
			var txt0 = document.createTextNode("Sample"+orderList[k]);
			td0.appendChild(txt0);
			tr.appendChild(td0);
			
			var tempDimList = ipDict[k];
			//console.log(tempDimList);
			//console.log(tempDimList.length);
			
			for(var j=0;j<tempDimList.length;j++){
				
				var td = document.createElement("td");
				var txt = document.createTextNode(tempDimList[j]);
				td.appendChild(txt);
				tr.appendChild(td);
			}
			myTable.appendChild(tr);
		}
		

	}
}

function tableFunctIp(ipDict){
	
	var myTable = document.getElementById("ip-table");
	var header = myTable.createTHead();
	
	var row0 = header.insertRow(0);
	var cell0 = row0.insertCell(0);
	var cell01 = row0.insertCell(1);
	var cell02 = row0.insertCell(2);
	cell02.innerHTML = "Dimensions";
	
    var row = header.insertRow(1);
    var cell = row.insertCell(0);
    cell.innerHTML = "Order";
    var cell1 = row.insertCell(1);
    cell1.innerHTML = "Samples";
    
    var dimensionLen = ipDict[0].length;
    
    for(var i=0;i<dimensionLen;i++){
    	
    	var tempCell = row.insertCell(i+2);
    	tempCell.innerHTML = "Dimension"+i;
    }
    
    var ipDictLen= Object.keys(ipDict).length;
	
	for(var i=0; i<ipDictLen; i++){
		
		var tr = document.createElement("tr");
		var tdOrder = document.createElement("td");
		var txtOrder = document.createTextNode(i);
		tdOrder.appendChild(txtOrder);
		tr.appendChild(tdOrder);
		
		var td0 = document.createElement("td");
		var txt0 = document.createTextNode("Sample"+i);
		td0.appendChild(txt0);
		tr.appendChild(td0);
		
		var tempDimList = ipDict[i];
		//console.log(tempDimList);
		//console.log(tempDimList.length);
		
		for(var j=0;j<tempDimList.length;j++){
			
			var td = document.createElement("td");
			var txt = document.createTextNode(tempDimList[j]);
			td.appendChild(txt);
			tr.appendChild(td);
		}
		
		myTable.appendChild(tr);

	}
}

function displayPQ(nodeList,response,pqOrderDivName,orderDivName,pqDivID,orderedDrawDiv,unorderedDrawDiv) {
	
	var res_response=JSON.parse(response);
	var pqPaths=JSON.parse(res_response["pqranks"]);
	var orders=JSON.parse(res_response["pqorders"]);
	var pqArrayLen=Object.keys(pqPaths).length;
	var arrStr = encodeURIComponent(JSON.stringify(nodeList));
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
	noneRadio.onclick = function(){ tempSaveOrder(pqOrderDivName,orderedDrawDiv,unorderedDrawDiv); };
	
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
		aTag.onclick = function(){ tempSaveOrder(pqOrderDivName,orderedDrawDiv,unorderedDrawDiv); };
		
		label.appendChild(aTag);
		label.appendChild(document.createTextNode("path"+(i+1)));
		para.appendChild(label);
		para.appendChild(br);
			
	}
	
	
}

function tempSaveOrder(pqOrderDivName,orderedDrawDiv,unorderedDrawDiv){

	order=document.querySelector('input[name="pqperms"]:checked').value
	//console.log(order);
	orderList=[];
	
	orderArray=order.split(",");
	for(var i=0; i<orderArray.length; i++) { 
		//orderArray[i] = +myArray[i]; 
		orderList.push(parseInt(orderArray[i], 10));
	} 
	//console.log(orderList);
	document.getElementById('savedorder').value=order;
	document.getElementById(pqOrderDivName).innerHTML=order;
	
	drawWithoutLabels(globalNodelist,globalEdges,orderList,orderedDrawDiv);
	
	document.getElementById(unorderedDrawDiv).style.visibility="hidden";
	document.getElementById(orderedDrawDiv).style.visibility="visible";
}

function drawCurrentChart(order,nodeList){
	
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

function sliderFunction(noise,sliderName,pqDivName,msgDivID){
	
	var slide = document.getElementById(sliderName).value;
	//console.log(noise);
	//console.log(slide);
	
	if (noise<slide){
		
		document.getElementById(msgDivID).innerHTML="Noise ratio below threshold. Diameter path best order estimate";
	}
	else{
		
		document.getElementById(pqDivName).style.visibility="visible";
		//displayPQ(counts,pqPerm,pqOrders);
		
	}
	
}

function enteredOrdering(dim_divId,dist_divID,textID){
	
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
}

function computePQ(counts,dpath,graph,pqTextName,pqOrderDivName,orderDivName,pqDivID,orderedDrawDiv,unorderedDrawDiv){
	
	//console.log(counts);
	var graph_dict=JSON.parse(graph);
	//console.log(graph_dict);
	var pqnum = document.getElementById(pqTextName).value;
	//console.log(pqnum)
	post_data = {}
    post_data["pqnum"] = pqnum
    post_data["dpath"] = dpath
    post_data["graph"] = graph_dict
	
	$.ajax({
        url: '/computePQ',
        data:JSON.stringify(post_data),
        type: 'POST',
        contentType:"text/json",  
        success: function(response){
        	displayPQ(counts,response,pqOrderDivName,orderDivName,pqDivID,orderedDrawDiv,unorderedDrawDiv);
        },
        error: function(error) {
            console.log(error);
        }
    });
	
}

function inPlaceAnalysis(response,dim_divID,dist_divID){
	
	//console.log(response);
	var res_response=JSON.parse(response);
	var distmat=res_response["distmat"];
	var dimension=res_response["dimension_reading"];
	var order=res_response["order"];
	
	showDimensions(dimension,order,dim_divID);
	drawDistMat(distmat,dist_divID);
	document.getElementById("changeDistMat").checked = false;
}



function showDimensions(dimRead,order,divID){
	
	//console.log(dimRead);
	//console.log(order);
	
	var data=[];
	var xaxis=[];
	
	var orderLen=order.length;
	//console.log(orderLen);
	var dimensionLen=dimRead.length;
	
	for(var i=0;i<orderLen;i++){
		xaxis.push(i+1);
	}
	//console.log(xaxis);
	
	for(var j=0;j<dimensionLen;j++){
		
		var trace= {
				x:xaxis,
				y:dimRead[j],
				type: 'scatter'
		};
		
		data.push(trace);
	}
	
		
	Plotly.newPlot(divID, data);	
	
}

function drawDistMat(distmat,divID){
	
	var data = [
		{
			//z: [[1, 20, 30], [20, 1, 60], [30, 60, 1]],
		    z: distmat,
		    type: 'heatmap'
		}
	];

	Plotly.newPlot(divID, data);
}

function getPCAForOrder(order,pcaDivID){
	
	var ordering = String("["+String(order)+"]");
	
	post_data = {}
    post_data["order"] = ordering
    //post_data["graph"] = graph_dict
    
    
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
	var data=res_response["pca_values"];
	//var x = [1,2,3,4,5];
	//var y = [3,4,5,7,8];
	//var z = [5,10,2,3,4]; 
	var c = ["red","green","yellow"];
	
	/*var trace={
			type: 'scatter3d',
			//mode: 'lines',
			x: data[0],
			y: data[1],
			z: data[2],
			opacity: 1,
			line: {
				width: 6,
				color: ,
				reversescale: false
			  }	
	}
	data.push(trace);*/
	
	
	Plotly.plot(pcaDivID, [{
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
	}]);/*, {
	  height: 640
	});*/
	//Plotly.plot('pca',data);
}

function dimensionChange(order,distmat,distDivID){
	
	var checkBox = document.getElementById("changeDistMat");
	var ordering = String("["+String(order)+"]");
	
	if (checkBox.checked == true) {
		
		drawTransposedMatrix(ordering,distDivID)
		//newDistMat=(distmat[0].map((col, i) => distmat.map(row => row[i])));
		//console.log(newDistMat);
		//drawDistMat(newDistMat);
	}
	else if(checkBox.checked == false){
		//console.log(distmat);
		drawDistMat(distmat,distDivID);
	}
	
}

function drawTransposedMatrix(order,distDivID){
	
	post_data = {}
    post_data["order"] = order
    
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

function getAnalysisValues(mst_dpath,cst_dpath,spd_dpath,un_dpath){
	
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
	
	
	
}

function drawAnalysisAll(response,mst_dpath,cst_dpath,spd_dpath,un_dpath){
	
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


/*function allParamsProcess(params){
	
	var res_params=JSON.parse(params);
	console.log(res_params);
	mstParams=res_params['mst'];
	
	drawWithLabels(mstParams['nodes'],mstParams['edges'],mstParams['dpath'],mstParams['labels'],"mynetwork-mst");
	drawWithoutLabels(mstParams['nodes'],mstParams['edges'],mstParams['dpath'],"myorderednetwork-mst");
	document.getElementById("mstNoise").innerHTML = mstParams['noise'] ;
	document.getElementById("mstIntensity").innerHTML = mstParams['intensity'] ;
	
	cstParams=res_params['cst'];
	spdParams=res_params['spd'];
	
	
}*/

function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

