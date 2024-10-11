action_to_num = {
    'close': 0,
    'accept': 1,
    'pass': 2,
    'deny': 3,
    'client-rst': 4,
    'server-rst': 5,
    'timeout': 6,
    'dns': 7,
    'ip-conn': 8
}

num_to_action = {
    0: 'close',
    1: 'accept',
    2: 'pass',
    3: 'deny',
    4: 'client-rst',
    5: 'server-rst',
    6: 'timeout',
    7: 'dns',
    8: 'ip-conn'
}

num_to_proto = {
    6: 'TCP',
    17: 'UDP',
    1: 'ICMP'
}