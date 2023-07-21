#!/usr/bin/env python3
import argparse
import sys
import runpod
import time


def get_args():
    parser = argparse.ArgumentParser(
        description='Start an on-demand RunPod pod',
    )

    parser.add_argument(
        '--pod_id', '-pod_id', '--pod', '-pod', '--p', '-p',
        type=str,
        required=True,
        help='pod id (eg. dg31b9aqtupn2z)'
    )

    return parser.parse_args()


def start_pod(pod_id):
    response = runpod.start_on_demand_pod(pod_id)
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            for error in resp_json['errors']:
                if error['message'] == 'There are not enough free GPUs on the host machine to start this pod.':
                    print('No available GPU, sleeping for 30 seconds....')
                    time.sleep(30)
                    start_pod(pod_id)
                else:
                    print(f"ERROR: {error['message']}")
        else:
            pod = resp_json['data']['podResume']

            print(f"id:         {pod['id']}")
            print(f"status:     {pod['desiredStatus']}")
            print(f"image:      {pod['imageName']}")
            print(f"machine id: {pod['machineId']}")
            print(f"host id:    {pod['machine']['podHostId']}")
            sys.exit()


if __name__ == '__main__':
    runpod = runpod.API()
    args = get_args()
    start_pod(args.pod_id)
