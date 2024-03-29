from django.http import HttpResponse
from django.contrib.gis.geos import GEOSGeometry
from django.utils import simplejson as json

import types

def geojson_to_csv(request):
    """
    This function should recieve a post request with
    a featurecollection.

    From this featurecollection this function will make a csv
    string and return it as a csv file for download.
    """

    if request.method == "POST":
        feature_collection = json.loads(request.raw_post_data)

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
        csv_header_list.insert(0, 'wkt')
        csv_header_list.insert(0, 'id')

        #create the csv
        csv_string = u""

        #write the header
        for header in csv_header_list:
            csv_string = u"%s%s;" % (csv_string, header)

        csv_string = u"%s\n" % (csv_string,)
        csv_row = []
        csv_rows = []

        for feature in features:

            geometry = feature['geometry']
            properties = feature['properties']

            id = None
            if feature.has_key('id'):
                id = feature['id']

            properties['id'] = id

            #make the geometry
            properties['wkt'] = GEOSGeometry(json.dumps(geometry)).wkt

            value_list = get_value_list(properties, csv_header_list)

            for value in value_list:

                #remove harmful characterers
                if type(value) == types.UnicodeType or type(value) == types.StringType:
                    value = value.replace(";", "")
                    value = value.replace("\n", " ")
                    value = value.replace("\r", " ")

                csv_row.append("%s;" % value)

            csv_rows.append(''.join(csv_row))
            csv_row = []

        csv_string = "%s%s" % (csv_string, '\n'.join(csv_rows))

        return HttpResponse(csv_string,
                            content_type='text/csv')
    else:
        return HttpResponse("This view only takes POST requests")


def json_to_csv(request):
    """
    This function takes a array of json objects
    and returns a csv file for download.
    """

    if request.method == "POST":
        json_array = json.loads(request.raw_post_data)

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
        csv_row = []
        csv_rows = []

        for json_dict in json_array:
            value_list = get_value_list(json_dict, csv_header_list)

            for value in value_list:

                #remove harmful characterers
                if type(value) == types.UnicodeType or type(value) == types.StringType:
                    value = value.replace(";", "")
                    value = value.replace("\n", " ")
                    value = value.replace("\r", " ")

                #modify value to json string
                #value = json.dumps(value)

                csv_row.append("%s;" % value)

            csv_rows.append(''.join(csv_row))
            csv_row = []

        csv_string = "%s%s" % (csv_string, '\n'.join(csv_rows))

        return HttpResponse(csv_string,
                            mimetype='text/csv')
    else:
        return HttpResponse("This view only takes POST requests")

def create_csv_header_set(json_dict):

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

    value_list = []

    for key in key_list:

        keys = key.split(".")

        if len(keys) == 1:
            if json_dict.has_key(key):
                value_list.append(json_dict[key])
            else:
                value_list.append('')
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
