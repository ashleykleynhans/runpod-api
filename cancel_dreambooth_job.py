#!/usr/bin/env python3
import argparse
import runpod
import json


def get_args():
    parser = argparse.ArgumentParser(
        description='Cancel Dreambooth training job',
    )

    parser.add_argument(
        '--job_id', '-job_id', '--job', '-job', '--j', '-j',
        type=str,
        required=True,
        help='job id (eg. 12345)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    job_id = args.job_id
    endpoints = runpod.Endpoints()
    response = endpoints.cancel_dreambooth_training(job_id)

    if response.status_code == 401:
        print('ERROR 401: Unauthorized')
    elif response.status_code == 404:
        print(f'ERROR 404: request with job_id {job_id} does not exist')
    else:
        resp_json = response.json()

        # if response.status_code == 200:
        print(json.dumps(resp_json, indent=4, default=str))
