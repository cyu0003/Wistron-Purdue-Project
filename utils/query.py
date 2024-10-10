import json
import requests

HEADERS = {
    'Content-Type': 'application/json'
}

def make_query(size):
    query = json.dumps({
        'size': size,
        'query': {
            'range': {
                '@timestamp': {
                    'gte': 'now-1d/d',
                    'lte': 'now/d'
                }
            }
        }
    })

    return query

def send_query(query, endpoint):
    uri = f'http://10.37.34.70:9200/{endpoint}-*/_search'

    return requests.get(uri, headers=HEADERS, data=query).json()