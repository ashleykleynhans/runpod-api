#!/usr/bin/env python3
import runpod
import json

VERSION = '1.4.0'
TEMPLATE_NAME = f'SUPIR Upscaling and Restoration'
CONTAINER_DISK_IN_GB = 10
IMAGE_NAME = f'ashleykza/supir:{VERSION}'
IS_PUBLIC = True
IS_SERVERLESS = False
# 3000 = SUPIR / 8888 = Jupyter / 2999 = RunPod Upload Manager
PORTS = '3000/http,8888/http,2999/http,22/tcp'
START_JUPYTER = True
START_SSH = True
VOLUME_IN_GB = 80
VOLUME_MOUNT_PATH = '/workspace'
RECOMMENDED_GPU_IDS = []
INCOMPATIBLE_GPU_IDS = []
ALLOWED_CUDA_VERSIONS = []
MIN_VRAM = 0
MIN_RAM = 0


if __name__ == '__main__':
    runpod = runpod.API()

    with open("README.md", "r") as file:
        README = file.read()

    response = runpod.create_template(
        name=TEMPLATE_NAME,
        image_name=IMAGE_NAME,
        container_disk_in_gb=CONTAINER_DISK_IN_GB,
        docker_args="",
        env=[{"key": "VENV_PATH", "value": "/workspace/venvs/SUPIR"}],
        volume_in_gb=VOLUME_IN_GB,
        volume_mount_path=VOLUME_MOUNT_PATH,
        ports=PORTS,
        readme=README,
        is_public=IS_PUBLIC,
        is_serverless=IS_SERVERLESS,
        start_jupyter=START_JUPYTER,
        start_ssh=START_SSH,
    )

    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            print(json.dumps(resp_json, indent=4, default=str))
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            print(json.dumps(resp_json, indent=4, default=str))
    else:
        print(response.status_code)
        print(json.dumps(resp_json, indent=4, default=str))
