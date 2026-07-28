#!/usr/bin/env python3
import argparse
import json
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import rpapi


def get_args():
    parser = argparse.ArgumentParser(
        description='Update the Template for a Serverless Endpoint',
    )

    parser.add_argument(
        '--endpoint_id', '-endpoint_id', '--endpoint', '-endpoint', '--e', '-e',
        type=str,
        required=True,
        help='endpoint id (eg. dg31b9aqtupn2z)'
    )

    parser.add_argument(
        '--template_id', '-template_id', '--template', '-template', '--t', '-t',
        type=str,
        required=True,
        help='template id (eg. mmmgzu2eyy)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    runpod = rpapi.Serverless()
    response = runpod.update_endpoint_template(args.endpoint_id, args.template_id)

    if response.status_code == 200:
        resp_json = response.json()

        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error.get('message', str(error)))
        else:
            endpoint = resp_json
            print('Updated successfully.')
            print(f"endpoint id: {endpoint.get('id')}")
            workers = endpoint.get('workers', {})
            print(f"min workers: {workers.get('min') if isinstance(workers, dict) else '?'}")
            print(f"max workers: {workers.get('max') if isinstance(workers, dict) else '?'}")
    elif response.status_code == 401:
        print('ERROR: Unauthorized (401) - Check your API token')
    else:
        print(f'ERROR: HTTP Status code: {response.status_code}')
