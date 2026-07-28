#!/usr/bin/env python3
import sys
import json
import time
import rpapi

VERSION = '4.2.2'
NAME = f'stable-diffusion-webui {VERSION}'
IMAGE_NAME = f'ashleykza/stable-diffusion-webui:{VERSION}'
GPU_TYPE_ID = 'NVIDIA RTX A5000'
OS_DISK_SIZE_GB = 10
PERSISTENT_DISK_SIZE_GB = 100
BID_PRICE = 0.190
COUNTRY_CODE = 'NO'
MIN_DOWNLOAD = 600
ALLOWED_CUDA_VERSIONS = ['11.8', '12.0', '12.1', '12.2', '12.3']
PORTS = '22/tcp,3000/http,3010/http,3020/http,6006/http,8000/http,8888/http,2999/http'


def create_spot_pod():
    pod_config = {
        'name': NAME,
        'image': IMAGE_NAME,
        'gpu': {
            'id': GPU_TYPE_ID,
            'count': 1,
        },
        'cloud': 'COMMUNITY',
        'disk': OS_DISK_SIZE_GB,
        'ports': PORTS.split(','),
        'mounts': {
            'persistent': {
                'size': PERSISTENT_DISK_SIZE_GB,
                'path': '/workspace',
            }
        },
        'env': {
            'VENV_PATH': '/workspace/venvs/stable-diffusion-webui',
            'ENABLE_TENSORBOARD': '1',
        },
    }

    response = runpod.create_pod(pod_config)
    resp_json = response.json()

    if response.status_code in (200, 201):
        if 'errors' in resp_json:
            for error in resp_json['errors']:
                msg = error.get('message', str(error))
                if 'no longer any instances available' in msg.lower():
                    print('No resources currently available, sleeping for 5 seconds')
                    time.sleep(5)
                    create_spot_pod()
                elif 'enough disk space' in msg.lower():
                    print('No instances with enough disk space available, sleeping for 5 seconds')
                    time.sleep(5)
                    create_spot_pod()
                else:
                    print(f'ERROR: {msg}')
        else:
            print(json.dumps(resp_json, indent=4, default=str))
            sys.exit()
    else:
        print(response.status_code)
        print(json.dumps(resp_json, indent=4, default=str))


if __name__ == '__main__':
    runpod = rpapi.API()
    create_spot_pod()
