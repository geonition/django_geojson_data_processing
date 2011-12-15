from django.http import HttpResponse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import WKTWriter
from django.utils import simplejson as json
import types
import string

def geojson_to_csv(request):
    """
    This function should recieve a post request with
    a featurecollection.
    
    From this featurecollection this function will make a csv
    string and return it as a csv file for download.
    """
    
    json_string = request.raw_post_data
    
    feature_collection = json.loads(json_string)
    
    crs = getattr(feature_collection,
                  'crs',
                  {
                    'type': 'name',
                    'properties': {
                        'name': 'urn:ogc:def:crs:EPSG::4979'
                        }})
    
    features = feature_collection['features']
    
    csv_header_set = set()
    for feature in features:
        csv_header_set.update(create_csv_header_set(feature['properties']))
    
    csv_header_list = list(csv_header_set)
    csv_header_list.sort()
    csv_header_list.insert(0, 'geometry_wkt')
    csv_header_list.insert(0, 'id')
    
    #create the csv
    csv_string = u""
    
    #write the header
    for header in csv_header_list:
        csv_string = u"%s%s;" % (csv_string, header)
    
    csv_string = u"%s\n" % (csv_string,)
    
    for feature in features:
        
        geometry = feature['geometry']
        properties = feature['properties']
        
        id = None
        if feature.has_key('id'):
            id = feature['id']
        
        properties['id'] = id
        
        #make the geometry
        ggeom = GEOSGeometry(json.dumps(geometry))
        wkt_w = WKTWriter()
        properties['geometry_wkt'] = wkt_w.write(ggeom)
        
        value_list = get_value_list(properties, csv_header_list)
        
        for value in value_list:
            
            #remove harmful characterers
            if type(value) == types.UnicodeType or type(value) == types.StringType:
                for c in string.whitespace:
                    value = value.replace(c, " ")
            
                value = value.replace("\n", " ")
                value = value.replace("\r", " ")
                value = value.replace(";", " ")
                value = value.strip()
            
            #modify value to json string
            value = json.dumps(value)
            
            csv_string = "%s%s;" % (csv_string, value)
            
        csv_string = u"%s\n" % (csv_string,)
    
    return HttpResponse(csv_string,
                        content_type='text/csv')
    

def json_to_csv(request):
    """
    This function takes a array of json objects
    and returns a csv file for download.
    """
    
    json_string = request.raw_post_data
    
    json_array = json.loads(json_string)
    
    if type(json_array) == types.DictType:
        json_array = [json_array]
    
    #this part has to check for nested objects
    csv_header_set = set()
    for json_dict in json_array:
        csv_header_set.update(create_csv_header_set(json_dict))

    csv_header_list = list(csv_header_set)
    csv_header_list.sort()
    
    #create the csv
    csv_string = u""
    
    #write the header
    for header in csv_header_list:
        csv_string = u"%s%s;" % (csv_string, header)
    
    csv_string = u"%s\n" % (csv_string,)
    
    for json_dict in json_array:
        value_list = get_value_list(json_dict, csv_header_list)
        
        for value in value_list:
            
            #remove harmful characterers
            if type(value) == types.UnicodeType or type(value) == types.StringType:
                for c in string.whitespace:
                    value = value.replace(c, " ")
            
                value = value.replace("\n", " ")
                value = value.replace("\r", " ")
                value = value.replace(";", " ")
                value = value.strip()
            
                
            #modify value to json string
            value = json.dumps(value)
            
            csv_string = u"%s%s;" % (csv_string, value)
            
        csv_string = u"%s\n" % (csv_string,)
    
    return HttpResponse(csv_string,
                        mimetype='text/csv')
   
def create_csv_header_set(json_dict):
    """
    This function returns a set of header
    field names created according
    to the keys and sub dictionaries
    foung in the given json_dict.
    """
    csv_header_set = set()
    
    for key, item in json_dict.items():
        if type(item) == types.DictType:
            temp_set = create_csv_header_set(item)
            for header in temp_set:
                add_header = "%s.%s" % (key, header)
                csv_header_set.add(add_header)
        else:
            csv_header_set.add(key)
            
    return csv_header_set

def get_value_list(json_dict, key_list):
    """
    Given the key_list this function returns
    a list of values that are can be found in
    the given json_dict. The not found values
    will be an empty string.
    """
    
    value_list = []
    
    for key in key_list:
        
        keys = key.split(".")
        
        if len(keys) == 1:
            if json_dict.has_key(key):
                value_list.append(json_dict[key])
            else:
                value_list.append("")
        else:
            temp_key = ""
            
            for k in keys[1:]:
                if temp_key != "":
                    temp_key = temp_key + "." + k
                else:
                    temp_key = k
            
            if json_dict.has_key(keys[0]):
                temp_value_list = get_value_list(json_dict[keys[0]],
                                                 [temp_key])
            else:
                temp_value_list = get_value_list({},
                                                 [temp_key])
                
            value_list.extend(temp_value_list)
    
    return value_list