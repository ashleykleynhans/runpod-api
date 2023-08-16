#!/usr/bin/env python3
import sys
import json
import time
import runpod

NAME = 'stable-diffusion-webui 1.7.0'
IMAGE_NAME = 'ashleykza/stable-diffusion-webui:1.7.0'
GPU_TYPE_ID = 'NVIDIA GeForce RTX 3090'
OS_DISK_SIZE_GB = 10
PERSISTENT_DISK_SIZE_GB = 75
COUNTRY_CODE = 'CA'
MIN_DOWNLOAD = 700
PORTS = '22/tcp,3000/http,3010/http,6006/http,8888/http'
# PORTS = '22/tcp,8888/http,3000/http,5000/http,5005/http'


def create_pod():
    pod_config = f"""
        countryCode: "{COUNTRY_CODE}",
        minDownload: {MIN_DOWNLOAD},
        gpuCount: 1,
        volumeInGb: {PERSISTENT_DISK_SIZE_GB},
        containerDiskInGb: {OS_DISK_SIZE_GB},
        gpuTypeId: "{GPU_TYPE_ID}",
        cloudType: COMMUNITY,
        supportPublicIp: true,
        name: "{NAME}",
        dockerArgs: "",
        ports: "{PORTS}",
        volumeMountPath: "/workspace",
        imageName: "{IMAGE_NAME}",
        startJupyter: true,
        startSsh: true,
        env: [
            {{
                key: "JUPYTER_PASSWORD",
                value: "Jup1t3R!"
            }},
            {{
                key: "ENABLE_TENSORBOARD",
                value: "1"
            }}
        ]
    """

    response = runpod.create_on_demand_pod(pod_config)
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:

            for error in resp_json['errors']:
                if error['message'] == 'There are no longer any instances available with the requested specifications. Please refresh and try again.':
                    print('No resources currently available, sleeping for 5 seconds')
                    time.sleep(5)
                    create_pod()
                elif error['message'] == 'There are no longer any instances available with enough disk space.':
                    print('No instances with enough disk space available, sleeping for 5 seconds')
                    time.sleep(5)
                    create_pod()
                else:
                    print('ERROR: ' + error['message'])
        else:
            print(json.dumps(resp_json, indent=4, default=str))
            sys.exit()


if __name__ == '__main__':
    runpod = runpod.API()
    create_pod()
