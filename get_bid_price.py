#!/usr/bin/env python3
import argparse
import json
import runpod


def get_args():
    parser = argparse.ArgumentParser(
        description='Get bid price for a specific RunPod GPU pod type',
    )

    parser.add_argument(
        '--gpu_id', '-gpu_id', '--gpu', '-gpu', '--g', '-g',
        type=str,
        required=True,
        help='GPU id (eg. NVIDIA GeForce RTX 3090")'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    gpu_id = args.gpu_id
    runpod = runpod.API()
    response = runpod.get_bid_price(gpu_id)
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            gpu = resp_json['data']['gpuTypes'][0]

            print()
            print(f"id:                 {gpu['id']}")
            print(f"name:               {gpu['displayName']}")
            print(f"vram:               {gpu['memoryInGb']}")
            print(f"secure cloud:       {gpu['secureCloud']}")
            print(f"community cloud:    {gpu['communityCloud']}")
            print(f"minimum price:      {gpu['lowestPrice']['minimumBidPrice']}")
            print(f"uniterrupted price: {gpu['lowestPrice']['uninterruptablePrice']}")
            # print(json.dumps(resp_json, indent=4, default=str))
