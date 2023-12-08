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

    response = runpod.get_serverless_request_metrics(args.endpoint_id)

    if response.status_code == 200:
        resp_json = response.json()

        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            table = PrettyTable(padding_width=2)
            table.field_names = [
                'Time',
                'Jobs',
                'C',
                'F',
                'R',
                'DT Max',
                'DT Min',
                'DT Total',
                'DT N95',
                'DT P70',
                'DT P90',
                'DT P98',
                'ET Max',
                'ET Min',
                'ET Total',
                'ET N95',
                'ET P70',
                'ET P90',
                'ET P98'
            ]
            table.align = 'l'

            for row in resp_json['data']:
                table.add_row([
                    row['time'],
                    row['requests'],
                    row['completed_requests'],
                    row['failed_requests'],
                    row['retried'],
                    row['dt_max'],
                    row['dt_min'],
                    row['dt_total'],
                    row['dt_n95'],
                    row['dt_p70'],
                    row['dt_p90'],
                    row['dt_p98'],
                    row['et_max'],
                    row['et_min'],
                    row['et_total'],
                    row['et_n95'],
                    row['et_p70'],
                    row['et_p90'],
                    row['et_p98']
                ])

            print(table)
    elif response.status_code == 401:
        print('ERROR: Unauthorized (401) - Check your API token')
    else:
        print('ERROR: ', end='')
        print(f'HTTP Status code: {response.status_code}')