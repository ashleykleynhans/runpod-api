#!/usr/bin/env python3
import argparse
import json
import runpod


def get_args():
    parser = argparse.ArgumentParser(
        description='Get Logs for a Serverless Endpoint',
    )

    parser.add_argument(
        '--endpoint-id', '-endpoint-id', '--endpoint', '-endpoint', '--e', '-e',
        type=str,
        required=True,
        help='endpoint id (eg. dg31b9aqtupn2z)'
    )

    parser.add_argument(
        '--start', '-start', '--s', '-s',
        type=str,
        required=True,
        help='start date (eg. 2023-11-28T12:00:00.000Z)'
    )

    parser.add_argument(
        '--to', '-to', '--t', '-t',
        type=str,
        required=True,
        help='to date (eg. 2023-11-29T15:00:00.000Z)'
    )

    parser.add_argument(
        '--batch-size', '-batch-size', '--batch', '-batch', '--b', '-b',
        type=int,
        required=False,
        default=500,
        help='batch size (eg. 500)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    runpod = runpod.Serverless()

    response = runpod.get_serverless_logs(
        args.endpoint_id,
        args.start,
        args.to,
        args.batch_size
    )

    if response.status_code == 200:
        resp_json = response.json()

        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            print(json.dumps(resp_json, indent=4, default=str))
    elif response.status_code == 401:
        print('ERROR: Unauthorized (401) - Check your API token')
    else:
        print('ERROR: ', end='')
        print(f'HTTP Status code: {response.status_code}')