# Docker image for ComfyUI: The most powerful and modular stable diffusion GUI, api and backend with a graph/nodes interface.

## Version 2.5.0

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 12.1
* Python 3.11.11
* Torch 2.5.1
* xformers 0.0.29.post1
* [Jupyter Lab](https://github.com/jupyterlab/jupyterlab)
* [code-server](https://github.com/coder/code-server)
* [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)
* [Application Manager](https://github.com/ashleykleynhans/app-manager)
* [CivitAI Downloader](https://github.com/ashleykleynhans/civitai-downloader)
* [sd_xl_base_1.0.safetensors](
  https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors)
* [sd_xl_refiner_1.0.safetensors](
  https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors)
* [sdxl_vae.safetensors](
  https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl_vae.safetensors)

## Ports

| Connect Port | Internal Port | Description          |
|--------------|---------------|----------------------|
| 3000         | 3001          | ComfyUI              |
| 8000         | 8000          | Application Manager  |
| 8888         | 8888          | Jupyter Lab          |
| 2999         | 2999          | RunPod File Uploader |

You can use the Application Manager to stop and start
the applications.

## Environment Variables

| Variable             | Description                                                       | Default               |
|----------------------|-------------------------------------------------------------------|-----------------------|
| JUPYTER_LAB_PASSWORD | Set a password for Jupyter lab                                    | not set - no password |
| DISABLE_AUTOLAUNCH   | Disable application from launching automatically                  | (not set)             |
| DISABLE_SYNC         | Disable syncing if using a RunPod network volume                  | (not set)             |
| EXTRA_ARGS           | Specify extra command line arguments for ComfyUI, eg. `--lowvram` | (not set)             |

## Logs

ComfyUI creates a log file, and you can tail it instead of
killing the service to view the logs

| Application          | Log file                    |
|----------------------|-----------------------------|
| ComfyUI              | /workspace/logs/comfyui.log |

For example:

```bash
tail -f /workspace/logs/comfyui.log
```