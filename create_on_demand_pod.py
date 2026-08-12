#!/usr/bin/env python3
import httpx
import sys
import time
import rpapi
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# VERSION = 'cu124-py311-v0.29.2'
# VERSION = 'cu128-py312-v0.32.0'
VERSION = '8.11.7'
TEMPLATE_ID = "jqw8e1my59"

NAME = 'ULTIMATE Stable Diffusion Kohya ComfyUI InvokeAI'
# NAME = 'FaceFusion Face Swapper and Enhancer'
# NAME = "A1111 Stable Diffusion 1.10.1 CUDA 12.4"
# NAME = 'ComfyUI RTX 5090 - Python 3.12'

IMAGE_NAME = f'ghcr.io/ashleykleynhans/stable-diffusion-webui:{VERSION}'
# IMAGE_NAME = f'ghcr.io/ashleykleynhans/comfyui:{VERSION}'
# IMAGE_NAME = 'ghcr.io/ashleykleynhans/comfyui:cu128-py312-v0.31.0'

GPU_TYPE_ID = "NVIDIA GeForce RTX 3090"
# GPU_TYPE_ID = 'NVIDIA GeForce RTX 5090'

ALLOWED_CUDA_VERSIONS = [
    "12.4",
    "12.5",
    "12.6",
    "12.7",
    "12.8",
    "12.9",
    "13.0",
    "13.1",
    "13.2",
    "13.3",
]
OS_DISK_SIZE_GB = 5
PERSISTENT_DISK_SIZE_GB = 80
CLOUD_TYPE = "COMMUNITY"
COUNTRY_CODE = "CA"
MIN_DOWNLOAD = 700

RETRY_DELAY_SECONDS = 30

NAMED_PORTS = {
    'SSH': '22/tcp',
    'A1111 Stable Diffusion Web UI': '3000/http',
    'Kohya_ss GUI': '3010/http',
    'ComfyUI': '3020/http',
    'TensorBoard': '6006/http',
    'InvokeAI': '9090/http',
    'Code Server': '7777/http',
    'Application Manager': '8000/http',
    'Jupyter Lab': '8888/http',
    'Runpod File Uploader': '2999/http',
}

# NAMED_PORTS = {
#     "SSH": "22/tcp",
#     "ComfyUI": "3000/http",
#     # "Application Manager": "8000/http",
#     "Jupyter Lab": "8888/http",
#     "Runpod File Uploader": "2999/http",
#     "Code Server": "7777/http",
# }

PORTS = ",".join(NAMED_PORTS.values())


def _gpu_is_available() -> bool:
    """Return True if the requested GPU has capacity to deploy right now.

    Checks the Runpod catalog for per-datacenter availability of
    GPU_TYPE_ID, scoped to the configured cloud type and minimum allowed
    CUDA version, and restricted to the configured country code(s).
    """
    min_cuda = ALLOWED_CUDA_VERSIONS[0] if ALLOWED_CUDA_VERSIONS else None
    response = runpod.get_gpu_availability(
        cloud=CLOUD_TYPE, count=1, min_cuda_version=min_cuda)
    if response.status_code != 200:
        console.print(
            f"[red]GPU availability check failed "
            f"(HTTP {response.status_code}), retrying[/red]"
        )
        return False

    countries = [c.strip()
                 for c in COUNTRY_CODE.split(",")] if COUNTRY_CODE else []
    for gpu in response.json().get("gpus", []):
        if gpu.get("id") != GPU_TYPE_ID:
            continue
        for dc in gpu.get("dataCenters", []):
            if dc.get("availability") == "NONE":
                continue
            if countries and not any(
                    c in dc.get("id", "") for c in countries):
                continue
            return True
        return False
    return False


def create_on_demand_pod():
    if not _gpu_is_available():
        console.print(
            f"[yellow]No {GPU_TYPE_ID} GPU available"
            f"{f' in {COUNTRY_CODE}' if COUNTRY_CODE else ''}, "
            f"retrying in {RETRY_DELAY_SECONDS} seconds[/yellow]"
        )
        time.sleep(RETRY_DELAY_SECONDS)
        return create_on_demand_pod()

    if TEMPLATE_ID:
        resp_json = _create_via_graphql()
    else:
        pod_config = {
            "name": NAME,
            "image": IMAGE_NAME,
            "gpu": {
                "id": GPU_TYPE_ID,
                "count": 1,
            },
            "cloud": CLOUD_TYPE,
            "disk": OS_DISK_SIZE_GB,
            "ports": PORTS.split(","),
            "mounts": {
                "persistent": {
                    "size": PERSISTENT_DISK_SIZE_GB,
                    "path": "/workspace",
                }
            },
        }
        response = runpod.create_pod(pod_config)
        resp_json = response.json()
        if response.status_code in (200, 201):
            if "errors" not in resp_json:
                return _display_success(resp_json)
            return _handle_errors(resp_json)
        elif (
            response.status_code == 400
            and "does not have the resources" in resp_json.get("detail", "")
        ):
            console.print(
                "[yellow]Machine does not have resources, retrying in 5 seconds[/yellow]"
            )
            time.sleep(5)
            return create_on_demand_pod()
        else:
            console.print(f"[red]{response.status_code}[/red]")
            console.print_json(data=resp_json)
            return

    if resp_json is None:
        return
    if "pod" in resp_json:
        _display_success(resp_json["pod"])
    elif "errors" in resp_json:
        _handle_errors(resp_json)
    elif "error" in resp_json:
        _handle_graphql_error(resp_json)


def _create_via_graphql():
    query = """
        mutation DeployPod($input: PodFindAndDeployOnDemandInput) {
            podFindAndDeployOnDemand(input: $input) {
                id
                name
                desiredStatus
                imageName
                costPerHr
                containerDiskInGb
                ports
                gpuCount
                machine {
                    dataCenterId
                    gpuDisplayName
                }
            }
        }
    """
    variables = {
        "input": {
            "templateId": TEMPLATE_ID,
            "name": NAME,
            "gpuTypeId": GPU_TYPE_ID,
            "gpuCount": 1,
            "cloudType": CLOUD_TYPE,
            "countryCode": COUNTRY_CODE if COUNTRY_CODE else None,
            "minDownload": MIN_DOWNLOAD,
            "allowedCudaVersions": ALLOWED_CUDA_VERSIONS,
        }
    }
    variables["input"] = {k: v for k,
                          v in variables["input"].items() if v is not None}

    response = httpx.post(
        rpapi.GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers=runpod._headers,
        timeout=60.0,
    )
    data = response.json()

    gql_errors = data.get("errors", [])
    pod = (data.get("data") or {}).get("podFindAndDeployOnDemand")

    if gql_errors:
        return {"errors": [{"message": e.get("message", str(e))} for e in gql_errors]}

    if pod is None:
        return {"error": "No pod returned from GraphQL"}

    return {
        "pod": {
            "id": pod.get("id"),
            "name": pod.get("name"),
            "status": pod.get("desiredStatus"),
            "image": pod.get("imageName"),
            "cost": pod.get("costPerHr"),
            "disk": pod.get("containerDiskInGb"),
            "ports": pod.get("ports", "").split(",") if pod.get("ports") else [],
            "gpu": {
                "id": (pod.get("machine") or {}).get("gpuDisplayName", ""),
                "count": pod.get("gpuCount", 1),
            },
            "cloud": CLOUD_TYPE,
            "dataCenterId": (pod.get("machine") or {}).get("dataCenterId"),
        }
    }


def _display_success(pod):
    console.print()
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    table.add_column("Key", style="bold cyan")
    table.add_column("Value")
    table.add_row("Pod ID", pod.get("id", ""))
    table.add_row("Name", pod.get("name", ""))
    table.add_row("Status", pod.get("status", ""))
    table.add_row("Image", pod.get("image", ""))
    gpu_info = pod.get("gpu", {})
    table.add_row(
        "GPU", f"{gpu_info.get('id', '')} x {gpu_info.get('count', '')}")
    ports = pod.get("ports", [])
    if isinstance(ports, str):
        ports = ports.split(",")
    table.add_row("Ports", ", ".join(ports))
    table.add_row("Cloud", pod.get("cloud", ""))
    if pod.get("dataCenterId"):
        table.add_row("Data Center", pod["dataCenterId"])
    if pod.get("cost"):
        table.add_row("Cost/hr", f"${pod['cost']}")
    console.print(Panel(table, title="[bold green]Pod Created[/bold green]"))
    sys.exit()


def _handle_errors(resp_json):
    for error in resp_json.get("errors", []):
        msg = error.get("message", str(error))
        if "no longer any instances available" in msg.lower():
            console.print(
                "[yellow]No resources currently available, sleeping for 5 seconds[/yellow]"
            )
            time.sleep(5)
            create_on_demand_pod()
        elif "enough disk space" in msg.lower():
            console.print(
                "[yellow]No instances with enough disk space available, sleeping for 5 seconds[/yellow]"
            )
            time.sleep(5)
            create_on_demand_pod()
        elif "does not have the resources" in msg.lower():
            console.print(
                "[yellow]Machine does not have resources, retrying in 5 seconds[/yellow]"
            )
            time.sleep(5)
            create_on_demand_pod()
        else:
            console.print(f"[red]ERROR: {msg}[/red]")


def _handle_graphql_error(resp_json):
    console.print(
        f'[red]ERROR: {resp_json.get("error", "Unknown error")}[/red]')


if __name__ == "__main__":
    runpod = rpapi.API()
    create_on_demand_pod()
