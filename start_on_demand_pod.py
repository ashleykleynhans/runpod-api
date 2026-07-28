#!/usr/bin/env python3
import argparse
import sys
import rpapi
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
                msg = error.get('message', str(error))
                if 'not enough free gpus' in msg.lower():
                    print('No available GPU, sleeping for 10 seconds....')
                    time.sleep(10)
                    start_pod(pod_id)
                else:
                    print(f"ERROR: {msg}")
        else:
            pod = resp_json
            machine = pod.get('machine', {}) if isinstance(pod, dict) else {}
            print(f"id:         {pod.get('id')}")
            print(f"status:     {pod.get('status')}")
            print(f"image:      {pod.get('image')}")
            print(f"machine id: {pod.get('machineId', 'N/A')}")
            if machine:
                print(f"host id:    {machine.get('podHostId', 'N/A')}")
            sys.exit()
    elif response.status_code == 204:
        print(f'Pod {pod_id} action completed')
    else:
        print(f'HTTP {response.status_code}')
        print(resp_json)


if __name__ == '__main__':
    runpod = rpapi.API()
    args = get_args()
    start_pod(args.pod_id)
