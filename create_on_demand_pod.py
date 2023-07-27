#!/usr/bin/env python3
import runpod
import json

NAME = 'stable-diffusion-webui 1.6.1'
IMAGE_NAME = 'ashleykza/stable-diffusion-webui:1.6.1'
GPU_TYPE_ID = 'NVIDIA GeForce RTX 3090'
OS_DISK_SIZE_GB = 10
PERSISTENT_DISK_SIZE_GB = 75
COUNTRY_CODE = ''
MIN_DOWNLOAD = 700
PORTS = '22/tcp,3000/http,3010/http,6006/http,8888/http'
# PORTS = '22/tcp,8888/http,3000/http,5000/http,5005/http'


if __name__ == '__main__':
    runpod = runpod.API()

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
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            print(json.dumps(resp_json, indent=4, default=str))
