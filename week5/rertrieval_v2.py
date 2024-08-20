from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

query='When is the next cohort?'
index_name='documents_20240820_5726'

@data_loader
def search(*args, **kwargs):
    connection_string = kwargs.get('connection_string', 'http://elasticsearch:9200')
    es_client = Elasticsearch(connection_string)
    search_query = {
        "size": 1,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    return result_docs