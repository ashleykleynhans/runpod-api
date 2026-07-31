#!/usr/bin/env python3
import sys
import time
import rpapi
from rich.console import Console
from rich.panel import Panel

console = Console()

# VERSION = 'cu124-py311-v0.29.2'
# VERSION = 'cu124-py312-v0.29.2'
VERSION = 'cu128-py312-v0.29.2'
# VERSION = '8.11.4'

# NAME = 'ULTIMATE Stable Diffusion Kohya ComfyUI InvokeAI'
NAME = 'ComfyUI RTX 5090 - Python 3.12'

# IMAGE_NAME = f'ghcr.io/ashleykleynhans/stable-diffusion-webui:{VERSION}'
IMAGE_NAME = f'ghcr.io/ashleykleynhans/comfyui:{VERSION}'

# GPU_TYPE_ID = 'NVIDIA GeForce RTX 3090'
GPU_TYPE_ID = 'NVIDIA GeForce RTX 5090'

# ALLOWED_CUDA_VERSIONS = ['12.4', '12.5', '12.6', '12.7', '12.8', '12.9', '13.0', '13.1', '13.2', '13.3']
ALLOWED_CUDA_VERSIONS = ['12.8', '12.9', '13.0', '13.1', '13.2', '13.3']

OS_DISK_SIZE_GB = 10
PERSISTENT_DISK_SIZE_GB = 80
CLOUD_TYPE = 'COMMUNITY'
COUNTRY_CODE = 'CA,FR'
MIN_DOWNLOAD = 700

# NAMED_PORTS = {
#     'SSH': '22/tcp',
#     'A1111 Stable Diffusion Web UI': '3000/http',
#     'Kohya_ss GUI': '3010/http',
#     'ComfyUI': '3020/http',
#     'TensorBoard': '6006/http',
#     'InvokeAI': '9090/http',
#     'Code Server': '7777/http',
#     'Application Manager': '8000/http',
#     'Jupyter Lab': '8888/http',
#     'Runpod File Uploader': '2999/http',
# }

NAMED_PORTS = {
    'SSH': '22/tcp',
    'ComfyUI': '3000/http',
    'Application Manager': '8000/http',
    'Jupyter Lab': '8888/http',
    'Runpod File Uploader': '2999/http',
    'Code Server': '7777/http',
}

PORTS = ','.join(NAMED_PORTS.values())

def create_on_demand_pod():
    pod_config = {
        'name': NAME,
        'image': IMAGE_NAME,
        'gpu': {
            'id': GPU_TYPE_ID,
            'count': 1,
        },
        'cloud': CLOUD_TYPE,
        'disk': OS_DISK_SIZE_GB,
        'ports': PORTS.split(','),
        'mounts': {
            'persistent': {
                'size': PERSISTENT_DISK_SIZE_GB,
                'path': '/workspace',
            }
        },
        # 'env': {
        #     'VENV_PATH': '/workspace/venvs/stable-diffusion-webui',
        #     'ENABLE_TENSORBOARD': '1',
        # },
    }

    response = runpod.create_pod(pod_config)
    resp_json = response.json()

    if response.status_code in (200, 201):
        if 'errors' in resp_json:
            for error in resp_json['errors']:
                msg = error.get('message', str(error))
                if 'no longer any instances available' in msg.lower():
                    console.print('[yellow]No resources currently available, sleeping for 5 seconds[/yellow]')
                    time.sleep(5)
                    create_on_demand_pod()
                elif 'enough disk space' in msg.lower():
                    console.print('[yellow]No instances with enough disk space available, sleeping for 5 seconds[/yellow]')
                    time.sleep(5)
                    create_on_demand_pod()
                else:
                    console.print(f'[red]ERROR: {msg}[/red]')
        else:
            console.print(Panel('', title='[bold green]Pod Created[/bold green]'))
            console.print_json(data=resp_json)
            sys.exit()
    elif response.status_code == 400 and 'does not have the resources' in resp_json.get('detail', ''):
        console.print('[yellow]Machine does not have resources, retrying in 5 seconds[/yellow]')
        time.sleep(5)
        create_on_demand_pod()
    else:
        console.print(f'[red]{response.status_code}[/red]')
        console.print_json(data=resp_json)


if __name__ == '__main__':
    runpod = rpapi.API()
    create_on_demand_pod()
