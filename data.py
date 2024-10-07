import argparse
import json
import requests

HEADERS = {
    'Content-Type': 'application/json'
}

def build_args():
    parser = argparse.ArgumentParser('data')
    parser.add_argument('endpoint', type=str, default='fortigate', nargs='?', help='The endpoint to query data from')
    parser.add_argument('size', type=int, default=2, nargs='?', help='The number of logs to query')
    return parser.parse_args()


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

def filter_res(res):
    data = []

    for log in res['hits']['hits']: # HOW TO CHANGE STRINGS INTO MEANINGFUL NUMBERS FOR K-MEANS??
        log.pop('blahblah', None) # CHANGE THIS TO SELECT NECESSARY INSTEAD OF REMOVE UNNECESSARY
        data.append(log)
    
    return data

def main(args):
    query = make_query(args.size)

    res = send_query(query, args.endpoint)

    #https://stackoverflow.com/questions/67745643/select-specific-keys-inside-a-json-using-python
    #https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe/20638258#20638258

    data = filter_res(res)

    for datum in data:
        print(json.dump(datum, indent=2))

    return

if __name__ == '__main__':
    args = build_args()
    main(args)