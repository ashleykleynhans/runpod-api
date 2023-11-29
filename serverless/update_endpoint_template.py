#!/usr/bin/env python3
import argparse
import json
import runpod


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
    runpod = runpod.Serverless()
    response = runpod.update_endpoint_template(args.endpoint_id, args.template_id)
    resp_json = response.json()

    if response.status_code == 200:
        resp_json = response.json()
        print(json.dumps(resp_json, indent=4, default=str))

        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            endpoint = resp_json['data']['updateEndpointTemplate']
            print('Min workers updated successfully.')
            print(f"endpoint id: {endpoint['id']}")
            print(f"template id: {endpoint['templateId']}")
            print(f"min workers: {endpoint['workersMin']}")
            print(f"max workers: {endpoint['workersMax']}")
    elif response.status_code == 401:
        print('ERROR: Unauthorized (401) - Check your API token')
    else:
        print('ERROR: ', end='')
        print(f'HTTP Status code: {response.status_code}')
