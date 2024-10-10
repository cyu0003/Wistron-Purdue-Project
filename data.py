import argparse
import os
import json
import requests
import socket, struct
import pandas as pd
from sklearn.cluster import KMeans
import ipaddress

action_to_num = {
    "close": 0,
    "accept": 1,
    "pass": 2,
    "deny": 3,
    "client-rst": 4,
    "server-rst": 5,
    "timeout": 6,
    "dns": 7,
    "ip_conn": 8
}

num_to_action = {
    0: "close",
    1: "accept",
    2: "pass",
    3: "deny",
    4: "client-rst",
    5: "server-rst",
    6: "timeout",
    7: "dns",
    8: "ip_conn"
}

num_to_proto = {
    6: "TCP",
    17: "UDP",
    1: "ICMP"
}

HEADERS = {
    'Content-Type': 'application/json'
}

def build_args():
    parser = argparse.ArgumentParser('data')
    parser.add_argument('--endpoint', type=str, default='fortigate', nargs='?', help='The endpoint to query data from')
    parser.add_argument('--size', type=int, default=1, nargs='?', help='The number of logs to query')
    parser.add_argument('--verbose', default=False, action="store_true", help='Toggle for verbose output')
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

def IP_to_num(ip):
    return struct.unpack("!L", socket.inet_aton(ip))[0]

def num_to_IP(num):
    return socket.inet_ntoa(struct.pack("!L", num))

def filter_logs(logs):
    data = []

    for log in logs: # HOW TO CHANGE STRINGS INTO MEANINGFUL NUMBERS FOR K-MEANS??
        print('current id: ' + log['_id'])
        source = log['_source']
        datum = {
            "id": log['_id'],
            "srcip": IP_to_num(source['srcip']),
            "dstip": IP_to_num(source['dstip']),
            "srcport": int(source.get('srcport', -1)),
            "dstport": int(source.get('dstport', -1)),
            "sentpkt": int(source.get('sentpkt', 0)),
            "rcvdpkt": int(source.get('rcvdpkt', 0)),
            "duration": source.get('duration', 0),
            "protocol": int(source['proto']),
            "opresult": action_to_num[source['action']]
        }
        data.append(datum)
    
    return data

def print_data(data):
    data["srcip"] = num_to_IP(data["srcip"])
    data["dstip"] = num_to_IP(data["dstip"])
    data["protocol"] = num_to_proto[data["protocol"]]
    data["opresult"] = num_to_action[data["opresult"]]

    print(json.dumps(data, indent=2))

def main(args):
    os.remove('temp.txt')
    print(args.verbose)
    query = make_query(args.size)

    res = send_query(query, args.endpoint)
    file = open('temp.txt', "w+")
    file.write(json.dumps(res, indent=2))
    if (args.verbose):
        print(f'-------------JSON response from {args.endpoint}-------------')
        print(json.dumps(res, indent=2))
        print('----------------------------END OF RESPONSE----------------------------')

    #https://stackoverflow.com/questions/67745643/select-specific-keys-inside-a-json-using-python
    #https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe/20638258#20638258

    data = filter_logs(res['hits']['hits'])

    if (args.verbose):
        for datum in data:
            print_data(dict(datum))
            print(json.dumps(datum, indent=2))
    
    df = pd.DataFrame(data)
    df = df.drop("id", axis='columns')

    if (args.verbose):
        print(df)
    
    kmeans = KMeans(n_clusters=2, init='k-means++', max_iter=300, random_state=0)
    kmeans.fit(df.values)
    df['cluster'] = kmeans.labels_

    print(df)

    return

if __name__ == '__main__':
    args = build_args()
    main(args)