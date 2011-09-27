from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

class FormatTest(TestCase):
    
    def setUp(self):
        
        self.client = Client()
        
        self.json_dict = {
            'array': [1,2,3],
            'boolean': True,
            'key': 'value',
            'null_value': None,
            'number': 1,
            'object': {
                'nested': True
            },
            'string': 'some; :tricky. ,string;'
        }
        
        self.correct_json_to_csv = u"%s%s%s%s%s%s%s%s" % ( 
        "array;boolean;key;null_value;number;object.nested;string;\n",
        "[1, 2, 3];",
        "true;",
        "\"value\";",
        "null;",
        "1;",
        "true;",
        "\"some :tricky. ,string\";\n") #remove ; characters
            
        self.geojson_dict = {
            'type': 'FeatureCollection',
            'features': [
                {'type': 'Feature',
                 'id': 1,
                 'geometry': {
                    'type': 'Point',
                    'coordinates': [1,2],
                    },
                'properties': self.json_dict
                },
                {'type': 'Feature',
                 'id': 2,
                 'geometry': {
                    'type': 'Polygon',
                    'coordinates': [[
                        [100.0, 0.0],
                        [101.0, 0.0],
                        [101.0, 1.0],
                        [100.0, 1.0],
                        [100.0, 0.0]]]
                    },
                'properties': {}
                },
                {'type': 'Feature',
                 'geometry': {
                    'type': 'LineString',
                    'coordinates': [
                        [100.0, 0.0],
                        [101.0, 1.0]]
                        },
                'properties': {
                    'some_unique_val': 'yes; this is it'
                    }
                }
            ]
        }
        
        self.correct_geojson_to_csv = u"%s%s%s%s%s%s%s" % (
        "id;geometry_wkt;array;boolean;key;null_value;number;",
        "object.nested;some_unique_val;string;\n",
        "1;\"POINT (1.0000000000000000 2.0000000000000000)\";[1, 2, 3];true;\"value\";null;1;true;\"\";",
        "\"some :tricky. ,string\";\n", #remove ; characters
        "2;\"POLYGON ((100.0000000000000000 0.0000000000000000, 101.0000000000000000 0.0000000000000000, 101.0000000000000000 1.0000000000000000, 100.0000000000000000 1.0000000000000000, 100.0000000000000000 0.0000000000000000))\";",
        "\"\";\"\";\"\";\"\";\"\";\"\";\"\";\"\";\n", 
        "null;\"LINESTRING (100.0000000000000000 0.0000000000000000, 101.0000000000000000 1.0000000000000000)\";\"\";\"\";\"\";\"\";\"\";\"\";\"yes this is it\";\"\";\n") 
        
    def test_json_to_csv(self):
        #send json to url
        response = self.client.post(reverse('json_to_csv'),
                                    data=json.dumps([self.json_dict]),
                                    content_type='application/json')
        
        #check that the same info can be found from the
        #returned csv
        self.assertEquals(response.content,
                          self.correct_json_to_csv,
                          "The csv response was not correct")
        
    def test_geojson_to_csv(self):
        #send json to url
        response = self.client.post(reverse('geojson_to_csv'),
                                    data=json.dumps(self.geojson_dict),
                                    content_type='application/json')
        
        #check that the same info can be found from the
        #returned csv
        self.assertEquals(response.content,
                          self.correct_geojson_to_csv,
                          "The csv response was not correct")
        
