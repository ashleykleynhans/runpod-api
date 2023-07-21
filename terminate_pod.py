#!/usr/bin/env python3
import argparse
import runpod


def get_args():
    parser = argparse.ArgumentParser(
        description='Terminate a RunPod pod',
    )

    parser.add_argument(
        '--pod_id', '-pod_id', '--pod', '-pod', '--p', '-p',
        type=str,
        required=True,
        help='pod id (eg. dg31b9aqtupn2z)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    pod_id = args.pod_id
    runpod = runpod.API()
    response = runpod.terminate_pod(pod_id)
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            print(f'Pod {pod_id} has been terminated')
