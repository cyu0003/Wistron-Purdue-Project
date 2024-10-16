import argparse
import json
import math

from utils.query import *
from utils.data import *
from utils.dicts import *
from utils.kmeans import *

def build_args():
    parser = argparse.ArgumentParser('data')
    parser.add_argument('--endpoint', type=str, default='fortigate', nargs='?', help='The endpoint to query data from')
    parser.add_argument('--size', type=int, default=2, nargs='?', help='The number of logs to query')
    parser.add_argument('--verbose', default=False, action='store_true', help='Toggle for verbose output')
    return parser.parse_args()

def main(args):
    query = make_query(args.size)

    res = send_query(query, args.endpoint)

    if (args.verbose):
        print(f'-----------------------JSON RESPONSE FROM {args.endpoint}-----------------------')
        print_res(res)
        print('-----------------------END OF RESPONSE-----------------------')
        print()

    with open('data.json', 'w') as f:
        json.dump(res, f)

    data = filter_logs(res['hits']['hits'])

    if (args.verbose):
        print('-----------------------FILTERED LOGS-----------------------')
        for datum in data:
            print_data(dict(datum))
        print('-----------------------END OF FILTERED LOGS-----------------------')
        print()
    
    df = make_df(data)
    c = int(math.sqrt(df.shape[0] / 2))

    id_col = df['id']
    df = df.drop('id', axis='columns')
    
    normalized_df = normalize_df(df)

    if (args.verbose):
        print('-----------------------DATAFRAME-----------------------')
        print(df.head())
        print('-----------------------END OF DATAFRAME-----------------------')
        print()
        print('-----------------------NORMALIZED DATAFRAME-----------------------')
        print(normalized_df.head())
        print('-----------------------END OF NORMALIZED DATAFRAME-----------------------')
    
    df = kmeans(normalized_df, c)

    visualize(df, c)

    df['id'] = id_col
    sorted = df.sort_values('cluster')
    sorted.to_csv('sorted.csv')

    return

if __name__ == '__main__':
    args = build_args()
    main(args)