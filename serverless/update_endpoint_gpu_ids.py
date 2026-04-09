#!/usr/bin/env python3
"""Update GPU pool IDs for a serverless endpoint."""
import argparse
import json
import runpod

VALID_GPU_POOLS = [
    'AMPERE_16', 'AMPERE_24', 'ADA_24', 'AMPERE_48',
    'ADA_48_PRO', 'AMPERE_80', 'ADA_80_PRO', 'HOPPER_141',
    'ADA_32_PRO', 'BLACKWELL_96', 'BLACKWELL_180',
]


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Update GPU pool IDs for a Serverless Endpoint',
    )

    parser.add_argument(
        '--endpoint-id', '-endpoint-id', '-e',
        type=str,
        required=True,
        help='endpoint id (eg. 73tp0h7f7798z4)'
    )

    parser.add_argument(
        '--name', '-name', '-n',
        type=str,
        required=True,
        help='endpoint name'
    )

    parser.add_argument(
        '--gpu-ids', '-gpu-ids', '-g',
        type=str,
        required=True,
        help=f'GPU pool IDs (eg. AMPERE_48). Valid: {", ".join(VALID_GPU_POOLS)}'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    serverless = runpod.Serverless()

    response = serverless.update_endpoint_gpu_ids(
        endpoint_id=args.endpoint_id,
        name=args.name,
        gpu_ids=args.gpu_ids,
    )

    if response.status_code == 200:
        resp_json = response.json()

        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            print(json.dumps(resp_json, indent=4, default=str))
    else:
        print(f'ERROR: HTTP Status code: {response.status_code}')
        print(response.text)
