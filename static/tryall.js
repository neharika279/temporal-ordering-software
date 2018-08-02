function drawTree(nodes,edges,labels,divName) {
    
	colors = ["red","blue","green","yellow","orange","black"];
	var result_labels=JSON.parse(labels);
	var result_edges=JSON.parse(edges);
	//console.log(result_labels);
	//console.log(result_edges);
	var dict = []; 
	var arrayLength = nodes.length;
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
		//console.log(result_edges[0]);
		//console.log(result_labels[0]);
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
	
	// create an array with edges
	
	
	
	
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


function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}


function ajaxTrial(dataset,pqDict){
	
	console.log(pqDict);
	console.log(dataset);
	//var result_pqDict=JSON.parse(pqDict);
	post_data = {}
    post_data["dataset"] = dataset 
    post_data["pqDict"] = pqDict
	
	$.ajax({
        url: '/ajaxTrial',
        data:JSON.stringify(post_data),
        type: 'POST',
        contentType:"text/json",  
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function thisFunct(){
	
	console.log("this");
}

/*$(function() {
    $('button').click(function() {
        $.ajax({
            url: '/signUpUser',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});*/


function threed(data){
	
	var x = [1,2,3,4,5];
	var y = [3,4,5,7,8];
	var z = [5,10,2,3,4]; 
	var c = ["red","green","yellow"];
	Plotly.plot('dimension', [{
	  type: 'scatter3d',
	  //mode: 'lines',
	  x: data[0],
	  y: data[1],
	  z: data[2],
	  opacity: 1,
	  line: {
	    width: 6,
	    color: c,
	    reversescale: false
	  }
	}], {
	  height: 640
	});
}




