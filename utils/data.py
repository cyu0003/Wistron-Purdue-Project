import ipaddress
import json
from utils.dicts import *

def print_res(res):
    print(json.dumps(res, indent=2))

def print_data(data):
    #data['srcip'] = num_to_IP(data['srcip'])
    #data['dstip'] = num_to_IP(data['dstip'])
    data['protocol'] = num_to_proto[data['protocol']]
    data['opresult'] = num_to_action[data['opresult']]

    print(json.dumps(data, indent=2))
    print()

def IP_to_num(ip):
    if ':' in ip:
        print('has ipv6')
    return int(ipaddress.ip_address(ip))

def num_to_IP(num):
    return str(ipaddress.ip_address(num))

#FORTIGATE ONLY
def filter_logs(logs):
    data = []

    for log in logs: # HOW TO CHANGE STRINGS INTO MEANINGFUL NUMBERS FOR K-MEANS??
        source = log['_source']
        datum = {
            'id': log['_id'],
            #'srcip': IP_to_num(source['srcip']),
            #'dstip': IP_to_num(source['dstip']),
            'srcport': int(source.get('srcport', 0)),
            'dstport': int(source.get('dstport', 0)),
            'sentpkt': int(source.get('sentpkt', 0)),
            'rcvdpkt': int(source.get('rcvdpkt', 0)),
            'duration': source.get('duration', 0),
            'protocol': int(source['proto']),
            'opresult': action_to_num[source['action']]
        }
        data.append(datum)
    
    return data