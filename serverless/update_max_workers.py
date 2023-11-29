#!/usr/bin/env python3
import argparse
import json
import runpod


def get_args():
    parser = argparse.ArgumentParser(
        description='Update Max Workers for a Serverless Endpoint',
    )

    parser.add_argument(
        '--endpoint_id', '-endpoint_id', '--endpoint', '-endpoint', '--e', '-e',
        type=str,
        required=True,
        help='endpoint id (eg. dg31b9aqtupn2z)'
    )

    parser.add_argument(
        '--max_workers', '-max_workers', '--min', '-min', '--m', '-m',
        type=int,
        required=True,
        help='min workers (eg. 1)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    runpod = runpod.Serverless()
    response = runpod.update_max_workers(args.endpoint_id, args.max_workers)
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            endpoint = resp_json['data']['updateEndpointWorkersMax']
            print('Max workers updated successfully.')
            print(f"endpoint id: {endpoint['id']}")
            print(f"template id: {endpoint['templateId']}")
            print(f"min workers: {endpoint['workersMin']}")
            print(f"max workers: {endpoint['workersMax']}")
