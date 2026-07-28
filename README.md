# rpapi - Runpod REST API v2 Client

[![Tests](https://github.com/ashleykleynhans/runpod-api/actions/workflows/tests.yml/badge.svg)](https://github.com/ashleykleynhans/runpod-api/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Python library for managing [Runpod](https://runpod.io) resources via the REST v2 API. Manage pods, serverless endpoints, templates, GPU types, and network volumes from Python scripts or the command line.

## Project Structure

```
runpod-api/
├── rpapi/                    # Core library package
│   └── __init__.py           # Client, API, Serverless, Endpoints classes
├── endpoints/                # Dreambooth training scripts
│   ├── train_dreambooth.py
│   ├── cancel_dreambooth_job.py
│   └── get_dreambooth_status.py
├── serverless/               # Serverless endpoint management scripts
│   ├── create_endpoint.py
│   ├── update_endpoint_template.py
│   ├── update_endpoint_gpu_ids.py
│   ├── update_min_workers.py
│   ├── update_max_workers.py
│   ├── get_endpoint_logs.py
│   ├── get_endpoint_metrics.py
│   ├── get_endpoint_requests.py
│   └── get_endpoint_summary.py
├── templates/                # Template creation scripts (one per image)
│   ├── gpu/
│   │   ├── a1111/            # Automatic1111 Stable Diffusion
│   │   ├── comfyui/          # ComfyUI
│   │   ├── forge/            # Forge WebUI
│   │   ├── kohya/            # Kohya SS training
│   │   ├── fooocus/          # Fooocus
│   │   ├── facefusion/       # FaceFusion
│   │   ├── instantid/        # InstantID
│   │   ├── framepack/        # FramePack video
│   │   ├── supir/            # SUPIR upscaler
│   │   ├── tts/              # Text-to-Speech
│   │   ├── llava/            # LLaVA vision
│   │   ├── oobabooga/        # TextGen
│   │   ├── audiocraft/       # AudioCraft
│   │   ├── rerender-a-video/ # Re-render Video
│   │   └── stable-diffusion/ # Stable Diffusion WebUI
│   └── serverless/
│       └── inswapper/        # Face Swap Serverless
├── tests/                    # Test suite (100% coverage)
│   ├── conftest.py
│   ├── test_client.py
│   ├── test_api.py
│   ├── test_serverless.py
│   ├── test_endpoints.py
│   └── test_imports.py
├── .github/workflows/
│   └── tests.yml             # CI pipeline (Python 3.10-3.14)
├── pyproject.toml            # Package metadata and tool config
├── .env.example              # API key configuration template
└── CHANGELOG.md
```

## Quick Start

### Install

```bash
git clone https://github.com/ashleykleynhans/runpod-api.git
cd runpod-api
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Configure

```bash
cp .env.example .env
```

Edit `.env` and add your [Runpod API key](https://www.runpod.io/console/user/settings):

```
RUNPOD_API_KEY=rpa_your_api_key_here
RUNPOD_METRICS_API_KEY=rm_your_metrics_key_here
```

## Usage

### Python Library

```python
import rpapi

# Pods, templates, catalog, volumes
api = rpapi.API()

# Serverless endpoints
serverless = rpapi.Serverless()

# Dreambooth training
endpoints = rpapi.Endpoints()
```

### API Class

```python
api = rpapi.API()

# GPU types
gpus = api.get_gpu_types().json()
gpu = api.get_gpu_type("NVIDIA RTX 4090").json()

# Pods
pods = api.get_pods().json()
pod = api.get_pod("pod123").json()

# Create a pod
api.create_pod({
    "name": "my-pod",
    "image": "ashleykza/stable-diffusion-webui:latest",
    "gpu": {"id": "NVIDIA RTX A5000", "count": 1},
    "cloud": "COMMUNITY",
    "disk": 10,
    "ports": ["22/tcp", "3000/http"],
    "mounts": {"persistent": {"size": 100, "path": "/workspace"}},
    "env": {"VENV_PATH": "/workspace/venv"},
})

# Pod lifecycle
api.stop_pod("pod123")
api.start_pod("pod123")
api.terminate_pod("pod123")

# Templates
templates = api.get_templates().json()
api.create_template(config={
    "name": "my-template",
    "image": "nginx:latest",
    "ports": ["80/http", "22/tcp"],
})

# Network volumes
volumes = api.get_network_volumes().json()

# Billing
billing = api.get_billing(
    start_time="2024-01-01T00:00:00Z",
    bucket_size="day",
).json()

# Account info (legacy GraphQL fallback)
account = api.get_myself().json()
```

### Serverless Class

```python
serverless = rpapi.Serverless()

# List endpoints
endpoints = serverless.get_endpoints().json()

# Create endpoint
serverless.create_endpoint({
    "name": "my-endpoint",
    "gpu": {"pools": ["AMPERE_48"], "count": 1},
    "workers": {"min": 0, "max": 3},
    "timeout": 5000,
})

# Update workers
serverless.update_min_workers("ep123", 1)
serverless.update_max_workers("ep123", 5)

# Update GPU pools
serverless.update_endpoint_gpu_ids(
    "ep123", "my-endpoint", "AMPERE_48, ADA_24"
)

# Metrics and logs (legacy REST)
logs = serverless.get_serverless_logs(
    "ep123", "2024-01-01T00:00:00Z", "2024-02-01T00:00:00Z", 500
).json()
metrics = serverless.get_serverless_metrics("ep123").json()
```

### Command-Line Scripts

All scripts accept command-line arguments:

```bash
# List GPU types with pricing
python3 get_gpu_types.py

# Get pod info
python3 get_pod.py --pod_id pod123

# List all pods
python3 get_pods.py

# Stop a pod
python3 stop_pod.py --pod_id pod123

# Create a template
cd templates/gpu/comfyui
python3 create_template.py

# Create a serverless endpoint
cd serverless
python3 create_endpoint.py --name my-ep --template-id tpl123 --gpu-ids "AMPERE_48"

# Update workers
python3 update_min_workers.py --endpoint_id ep123 --min_workers 1
```

## Supported Python Versions

| Python | Status |
|--------|--------|
| 3.10   | CI tested |
| 3.11   | CI tested |
| 3.12   | CI tested |
| 3.13   | CI tested |
| 3.14   | CI tested |

## Testing

```bash
pip install -e ".[test]"
python3 -m pytest
```

Enforces 100% code coverage on the `rpapi` package.

## Community and Contributing

Pull requests and issues on [GitHub](https://github.com/ashleykleynhans/runpod-api) are welcome.

## Appreciate my work?

<a href="https://www.buymeacoffee.com/ashleyk" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
