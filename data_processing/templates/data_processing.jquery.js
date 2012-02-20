

gnt['data_processing'] = {}

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
    }

/*
 This function sends a geojson featurecollection
 to the server and recieved a csv file
 back with the information in the geojson featurecollection
*/
gnt.data_processing['geojson_to_csv'] =
    function(json_object, callback_function) {
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
    }
