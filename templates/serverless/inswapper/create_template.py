#!/usr/bin/env python3
import runpod
import json

TEMPLATE_NAME = 'Face Swap'
CONTAINER_DISK_IN_GB = 5
IMAGE_NAME = 'ashleykza/runpod-worker-inswapper:standalone-1.0.1'


if __name__ == '__main__':
    runpod = runpod.API()

    template = f"""
        containerDiskInGb: {CONTAINER_DISK_IN_GB},
        dockerArgs: "",
        env: [],
        imageName: "{IMAGE_NAME}",
        isServerless: true,
        name: "{TEMPLATE_NAME}",
        readme: "",
        volumeInGb: 0,
        volumeMountPath: "/runpod-volume"
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
