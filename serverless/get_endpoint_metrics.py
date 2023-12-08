#!/usr/bin/env python3
import argparse
import json
import runpod
from prettytable import PrettyTable


def get_args():
    parser = argparse.ArgumentParser(
        description='Get Metrics for a Serverless Endpoint',
    )

    parser.add_argument(
        '--endpoint-id', '-endpoint-id', '--endpoint', '-endpoint', '--e', '-e',
        type=str,
        required=True,
        help='endpoint id (eg. dg31b9aqtupn2z)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    runpod = runpod.Serverless()

    response = runpod.get_serverless_metrics(args.endpoint_id)

    if response.status_code == 200:
        resp_json = response.json()

        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            print(json.dumps(resp_json, indent=4, default=str))
            # table = PrettyTable(padding_width=2)
            # table.field_names = ['Status', 'Request ID', 'Delay Time', 'Execution Time', 'Worker ID']
            # table.align = 'l'
            #
            # if 'requests' in resp_json and resp_json['requests'] is not None:
            #     for r in resp_json['requests']:
            #         table.add_row([
            #             r['status'],
            #             r['id'],
            #             r['delayTime'],
            #             r['executionTime'],
            #             r['workerId']
            #         ])
            #
            #     print(table)
            # else:
            #     print('No requests')

    elif response.status_code == 401:
        print('ERROR: Unauthorized (401) - Check your API token')
    else:
        print('ERROR: ', end='')
        print(f'HTTP Status code: {response.status_code}')