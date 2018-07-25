function myFunction(nodes,edges,dPath,labels) {
	
	var result_labels=JSON.parse(labels);
	
	if(isEmpty(result_labels)){
		drawWithoutLabels(nodes,edges,dPath);
	}
	else{
		drawWithLabels(nodes,edges,dPath,labels)	
	}
	
}

function drawWithoutLabels(nodes,edges,dPath){
	
	var dict = []; // create an empty array
	var arrayLength = nodes.length;
	
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
	
	for (var i = 0; i < edgeArrayLen; i++) {
		
		edge_dict.push({
		from:   result_edges[i][0],
	    to: result_edges[i][1]
		});
		
	}
	
	var final_edges = new vis.DataSet(edge_dict);
	// create a network
	var container = document.getElementById('mynetwork');
	
	// provide the data in the vis format
	var data = {
	    nodes: final_nodes,
	    edges: final_edges
	};
	var options = {};
	
	// initialize your network!
	var network = new vis.Network(container, data, options);
}

function drawWithLabels(nodes,edges,dPath,labels){
	
	colors = ["red","blue","green","yellow","orange","black"];
	var dict = [];
	var result_labels=JSON.parse(labels);
	//console.log(result_labels);
	var labelArrayLen=Object.keys(result_labels).length;
	
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
	var container = document.getElementById('mynetwork');
	
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

function displayPQ(nodeList,response) {
	
	//console.log(nodeList);
	var res_response=JSON.parse(response);
	var pqPaths=JSON.parse(res_response["pqranks"]);
	//console.log(res_response["pqranks"]);
	var orders=JSON.parse(res_response["pqorders"]);
	console.log(pqPaths);
	console.log(orders);
	var pqArrayLen=Object.keys(pqPaths).length;
	var arrStr = encodeURIComponent(JSON.stringify(nodeList));
	var para=document.getElementById("pq");
	for (var i = 0; i < pqArrayLen; i++) {
		
		var jsonOrder=JSON.stringify(orders[i]);
		//printThis += pqPaths[i]+"<br>";
		var aTag = document.createElement('a');
		var br = document.createElement('br');
		aTag.setAttribute('href','javascript:drawCurrentChart(\''+jsonOrder+'\',\''+arrStr+'\')');
		//aTag.setAttribute('onclick', 'drawChart(jsonOrder,pqPaths[i])');
		aTag.innerHTML = pqPaths[i]+"";
		para.appendChild(aTag);
		para.appendChild(br);
			
	}
	
	
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

function sliderFunction(noise){
	
	var slide = document.getElementById("myRange").value;
	//console.log(noise);
	//console.log(slide);
	
	if (noise<slide){
		
		document.getElementById("msg").innerHTML="Noise ratio below threshold. Diameter path best order estimate";
	}
	else{
		
		document.getElementById("pq").style.visibility="visible";
		//displayPQ(counts,pqPerm,pqOrders);
		
	}
	
}

function computePQ(counts,dpath,graph){
	
	//console.log(counts);
	var graph_dict=JSON.parse(graph);
	//console.log(graph_dict);
	var pqnum = document.getElementById("pqno").value;
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
        	displayPQ(counts,response);
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

