# Automatic1111 Stable Diffusion WebUI

## Version 1.10.1

**NOTE:** This template requires **CUDA 12.4** or higher, ensure that you use the CUDA filter to select the correct CUDA versions.

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 12.4
* Python 3.10.12
* Torch 2.6.0
* xformers 0.0.29.post3
* [Jupyter Lab](https://github.com/jupyterlab/jupyterlab)
* [code-server](https://github.com/coder/code-server)
* [Automatic1111 Stable Diffusion Web UI](
  https://github.com/AUTOMATIC1111/stable-diffusion-webui) 1.10.1
* [ControlNet extension](
  https://github.com/Mikubill/sd-webui-controlnet) v1.1.455
* [After Detailer extension](
  https://github.com/Bing-su/adetailer) v25.3.0
* [ReActor extension](https://github.com/Gourieff/sd-webui-reactor)
* [Deforum extension](
  https://github.com/deforum-art/sd-webui-deforum)
* [Inpaint Anything extension](https://github.com/Uminosachi/sd-webui-inpaint-anything)
* [Infinite Image Browsing extension](https://github.com/zanllp/sd-webui-infinite-image-browsing)
* [CivitAI extension](https://github.com/civitai/sd_civitai_extension)
* [CivitAI Browser+ extension](https://github.com/BlafKing/sd-civitai-browser-plus)
* [TensorRT extension](https://github.com/NVIDIA/Stable-Diffusion-WebUI-TensorRT)
* [Stable Diffusion Dynamic Thresholding (CFG Scale Fix) extension](https://github.com/mcmonkeyprojects/sd-dynamic-thresholding)
* [inswapper_128.onnx](
  https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx)
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)
* [Application Manager](https://github.com/ashleykleynhans/app-manager)
* [CivitAI Downloader](https://github.com/ashleykleynhans/civitai-downloader)

## Ports

| Connect Port | Internal Port | Description                   |
|--------------|---------------|-------------------------------|
| 3000         | 3001          | A1111 Stable Diffusion Web UI |
| 7777         | 7777          | Code Server                   |
| 8000         | 8000          | Application Manager           |
| 8888         | 8888          | Jupyter Lab                   |
| 2999         | 2999          | RunPod File Uploader          |

## Environment Variables

| Variable             | Description                                      | Default                |
|----------------------|--------------------------------------------------|------------------------|
| VENV_PATH            | Set the path for the Python venv for the app     | /workspace/venvs/a1111 |
| JUPYTER_LAB_PASSWORD | Set a password for Jupyter lab                   | not set - no password  |
| DISABLE_AUTOLAUNCH   | Disable Web UIs from launching automatically     | (not set)              |
| DISABLE_SYNC         | Disable syncing if using a RunPod network volume | (not set)              |

## Logs

Stable Diffusion Web UI creates a log file, and you can tail it instead of
killing the services to view the logs

| Application             | Log file                     |
|-------------------------|------------------------------|
| Stable Diffusion Web UI | /workspace/logs/webui.log    |

For example:

```bash
tail -f /workspace/logs/webui.log
```
