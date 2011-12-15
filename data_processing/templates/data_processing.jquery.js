

gnt['data_processing'] = {};

/*
 This function sends a json object
 to the server and recieved a csv file
 back with the information in the json
*/
gnt.data_processing['json_to_csv'] =
    function(json_object, callback_function) {
        
        $.ajax({
            url: "{% url json_to_csv %}",
            type: "POST",
            data: JSON.stringify(json_object),
            contentType: "application/json",
            success: function(data){
                if(callback_function !== undefined) {
                    callback_function(data);
                    }
                },
            error: function(e) {
                if(callback_function !== undefined) {
                    callback_function(e);
                }
            },
            dataType: "json",
            beforeSend: function(xhr){
                //for cross site authentication using CORS
                xhr.withCredentials = true;
                }
        });
    };

/*
 This function sends a geojson featurecollection
 to the server and recieved a csv file
 back with the information in the geojson featurecollection
*/
gnt.data_processing['geojson_to_csv'] =
    function(json_object, callback_function) {
        console.log("send post");
        $.ajax({
            url: "{% url geojson_to_csv %}",
            type: "POST",
            data: JSON.stringify(json_object),
            contentType: "application/json",
            success: function(data){
                if(callback_function !== undefined) {
                    callback_function(data);
                    }
                },
            error: function(e) {
                if(callback_function !== undefined) {
                    callback_function(e);
                }
            },
            dataType: "json",
            beforeSend: function(xhr){
                //for cross site authentication using CORS
                xhr.withCredentials = true;
                }
        });
    };

/*
 UNION function that returns the union of the two featurecollections
 according to the id of the features.
 
 Make sure all features have an id assigned to them before using this
 function. This function will throw an error if no id is found.
*/
gnt.data_processing['featurecollection_union'] =
function(featurecollection1, featurecollection2) {
    var featurecollection = featurecollection1;
    
    var ids = {}; //set of ids in the union
    for(var i = 0; i < featurecollection.features.length; i++) {
	ids[featurecollection.features[i].id] = true;
    }
    for(var j = 0; j < featurecollection2.features.length; j++) {
	var feat = featurecollection2.features[j];
	if(ids[feat.id] === undefined) {
	    featurecollection.features.push(feat);
	}
    }
    return featurecollection;
}

/*
 INTERSECT function that returns the intersect of two featurecollections
 according to their assigned id.
 
 If no id is signed to a feature it will throw an error.
*/
gnt.data_processing['featurecollection_intersect'] =
function(featurecollection1, featurecollection2) {
    var featurecollection = {
	"type": "FeatureCollection",
	"features": []
	};
    
    for(var i = 0; i < featurecollection1.features.length; i++) {
	for(var j = 0; j < featurecollection2.features.length; j++) {
	    if(featurecollection1.features[i].id === featurecollection2.features[j].id) {
		featurecollection.features.push(featurecollection1.features[i]);
		break;
	    }
	}
    }
    return featurecollection;
}

/*
 COMPLEMENT function that returns a new featurecollection with features
 that can be found in featurecollection1 but not in featurecollection2.
 
 Based on feature id, if id does not exist in a feature this function
 throws an error
*/
gnt.data_processing['featurecollection_complement'] =
function(featurecollection1, featurecollection2) {
    var featurecollection = featurecollection1;
    
    for(var i = 0; i < featurecollection.features.length; i++) {
	for(var j = 0; j < featurecollection2.features.length; j++) {
	    
	    if(featurecollection.features[i].id === featurecollection2.features[j].id) {
		featurecollection.features.splice(i, 1);
		i--;
		break;
	    }
	}
    }
    return featurecollection;
}