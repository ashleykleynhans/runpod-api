#!/usr/bin/env python3
import argparse
import json
import rpapi


def get_args():
    parser = argparse.ArgumentParser(
        description='Get pricing for a specific RunPod GPU type',
    )

    parser.add_argument(
        '--gpu_id', '-gpu_id', '--gpu', '-gpu', '--g', '-g',
        type=str,
        required=True,
        help='GPU id (eg. "NVIDIA GeForce RTX 3090")'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    gpu_id = args.gpu_id
    runpod = rpapi.API()
    response = runpod.get_bid_price(gpu_id)
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            price = resp_json.get('price', {})

            print()
            print(f"id:                 {resp_json['id']}")
            print(f"name:               {resp_json['name']}")
            print(f"vram:               {resp_json['memory']} GB")
            print(f"secure cloud:       {resp_json.get('secure', False)}")
            print(f"community cloud:    {resp_json.get('community', False)}")
            print(f"secure price:       {price.get('secure', '-')}")
            print(f"community price:    {price.get('community', '-')}")
    else:
        print(f'HTTP {response.status_code}')
        print(json.dumps(resp_json, indent=4, default=str))
