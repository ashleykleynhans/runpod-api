#!/usr/bin/env python3
import runpod
import json

VERSION = '1.0.0'
TEMPLATE_NAME = 'ComfyUI'
CONTAINER_DISK_IN_GB = 10
IMAGE_NAME = f'ashleykza/comfyui:{VERSION}'
IS_PUBLIC = True
IS_SERVERLESS = False
# 3000 = ComfyUI / 8000 = App Manager / 8888 = Jupyter / 2999 = RunPod File Uploader
PORTS = '3000/http,8000/http,8888/http,2999/http,22/tcp'
START_JUPYTER = True
START_SSH = True
VOLUME_IN_GB = 50
VOLUME_MOUNT_PATH = '/workspace'


if __name__ == '__main__':
    runpod = runpod.API()

    with open("README.md", "r") as file:
        README = file.read().replace("\n", "\\n")

    template = f"""
        containerDiskInGb: {CONTAINER_DISK_IN_GB},
        dockerArgs: "",
        env: [],
        imageName: "{IMAGE_NAME}",
        isPublic: {str(IS_PUBLIC).lower()},
        isServerless: {str(IS_SERVERLESS).lower()},
        name: "{TEMPLATE_NAME}",
        ports: "{PORTS}",
        readme: "{README}"
        startJupyter: {str(START_JUPYTER).lower()},
        startSsh: {str(START_SSH).lower()},
        volumeInGb: {VOLUME_IN_GB},
        volumeMountPath: "{VOLUME_MOUNT_PATH}"
    """

    response = runpod.create_template(template)
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
