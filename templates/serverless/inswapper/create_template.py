#!/usr/bin/env python3
import runpod
import json

TEMPLATE_NAME = 'Face Swap'
CONTAINER_DISK_IN_GB = 5
IMAGE_NAME = 'ashleykza/runpod-worker-inswapper:standalone-1.0.1'
RECOMMENDED_GPU_IDS = []
INCOMPATIBLE_GPU_IDS = []
ALLOWED_CUDA_VERSIONS = []
MIN_VRAM = 0
MIN_RAM = 0


if __name__ == '__main__':
    runpod = runpod.API()

    response = runpod.create_template(
        name=TEMPLATE_NAME,
        image_name=IMAGE_NAME,
        container_disk_in_gb=CONTAINER_DISK_IN_GB,
        docker_args="",
        env=[],
        volume_in_gb=0,
        volume_mount_path="/runpod-volume",
        is_serverless=True,
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
