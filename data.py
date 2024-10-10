import argparse
import json
import requests
import socket, struct
from enum import Enum

class Action(Enum):
    close = 0
    accept = 1

class Protocol(Enum):
    tcp_8080 = 0
    HTTPS = 1

HEADERS = {
    'Content-Type': 'application/json'
}

def build_args():
    parser = argparse.ArgumentParser('data')
    parser.add_argument('--endpoint', type=str, default='fortigate', nargs='?', help='The endpoint to query data from')
    parser.add_argument('--size', type=int, default=1, nargs='?', help='The number of logs to query')
    parser.add_argument('--verbose', type=bool, default=True, nargs='?', help='Toggle for verbose output')
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
        source = log['_source']
        datum = {
            "id": log['_id'],
            "srcip": IP_to_num(source['srcip']),
            "dstip": IP_to_num(source['dstip']),
            "srcport": int(source['srcport']),
            "dstport": int(source['dstport']),
            "sentpkt": int(source['sentpkt']),
            "rcvdpkt": int(source['rcvdpkt']),
            "duration": source['duration'],
            "protocol": Protocol[source['service']].value,
            "opresult": Action[source['action']].value
        }
        data.append(datum)
    
    return data

def print_data(data):
    data["srcip"] = num_to_IP(data["srcip"])
    data["dstip"] = num_to_IP(data["dstip"])
    data["protocol"] = Protocol(data["protocol"]).name
    data["opresult"] = Action(data["opresult"]).name

    print(json.dumps(data, indent=2))

def main(args):
    query = make_query(args.size)

    res = send_query(query, args.endpoint)
    if (args.verbose):
        print(json.dumps(res, indent=2))

    #https://stackoverflow.com/questions/67745643/select-specific-keys-inside-a-json-using-python
    #https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe/20638258#20638258

    data = filter_logs(res['hits']['hits'])

    for datum in data:
        print_data(dict(datum))
        print(json.dumps(datum, indent=2))

    return

if __name__ == '__main__':
    args = build_args()
    main(args)