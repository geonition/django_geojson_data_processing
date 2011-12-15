# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

urlpatterns = patterns('data_processing.views',
                       
            #maybe these could be smarter
            url(r'^geojson_to_csv$',
                'geojson_to_csv',
                name="geojson_to_csv"),
            
            url(r'^json_to_csv$',
                'json_to_csv',
                name="json_to_csv"),
              
        )