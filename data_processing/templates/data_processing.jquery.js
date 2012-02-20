

gnt['data_processing'] = {}

/*
 This function sends a json object
 to the server and recieved a csv file
 back with the information in the json
*/
gnt.data_processing['json_to_csv'] =
    function(json_string_or_object, callback_function) {

        var json_string = json_string_or_object;
        if( typeof(" ") !== typeof(json_string_or_object)) {
            json_string = JSON.stringify(json_string_or_object);
        }

        $.ajax({
            url: "{% url json_to_csv %}",
            type: "POST",
            data: json_string,
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
    }

/*
 This function sends a geojson featurecollection
 to the server and recieved a csv file
 back with the information in the geojson featurecollection
*/
gnt.data_processing['geojson_to_csv'] =
    function(feature_collection, callback_function) {

        var json_string = feature_collection;
        if( typeof(" ") !== typeof(feature_collection)) {
            json_string = JSON.stringify(feature_collection);
        }

        $.ajax({
            url: "{% url geojson_to_csv %}",
            type: "POST",
            data: json_string,
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
    }
