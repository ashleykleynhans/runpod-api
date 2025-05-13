# Automatic1111 Stable Diffusion WebUI, Kohya SS, ComfyUI and InvokeAI

## Version 8.0.0

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 12.4
* Python 3.10.12
* Torch 2.6.0
* xformers 0.0.29.post3
* [Jupyter Lab](https://github.com/jupyterlab/jupyterlab)
* [code-server](https://github.com/coder/code-server)
* [Automatic1111 Stable Diffusion Web UI](
  https://github.com/AUTOMATIC1111/stable-diffusion-webui.git) 1.10.1
* [ControlNet extension](
  https://github.com/Mikubill/sd-webui-controlnet) v1.1.455
* [After Detailer extension](
  https://github.com/Bing-su/adetailer) v25.3.0
* [ReActor extension](https://github.com/Gourieff/sd-webui-reactor)
* [Deforum extension](
  https://github.com/deforum-art/sd-webui-deforum)
* [Locon extension](
  https://github.com/ashleykleynhans/a1111-sd-webui-locon)
* [Inpaint Anything extension](https://github.com/Uminosachi/sd-webui-inpaint-anything)
* [Infinite Image Browsing extension](https://github.com/zanllp/sd-webui-infinite-image-browsing)
* [CivitAI extension](https://github.com/civitai/sd_civitai_extension)
* [CivitAI Browser+ extension](https://github.com/BlafKing/sd-civitai-browser-plus)
* [Stable Diffusion Dynamic Thresholding (CFG Scale Fix) extension](https://github.com/mcmonkeyprojects/sd-dynamic-thresholding)
* [Kohya_ss](https://github.com/bmaltais/kohya_ss) v25.0.3
* [ComfyUI](https://github.com/comfyanonymous/ComfyUI) v0.3.33
* [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)
* [InvokeAI](https://github.com/invoke-ai/InvokeAI) v5.11.0
* inswapper_128.onnx
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
| 3010         | 3011          | Kohya_ss                      |
| 3020         | 3021          | ComfyUI                       |
| 9090         | 9090          | InvokeAI                      |
| 6006         | 6066          | Tensorboard                   |
| 7777         | 7777          | Code Server                   |
| 8000         | 8000          | Application Manager           |
| 8888         | 8888          | Jupyter Lab                   |
| 2999         | 2999          | RunPod File Uploader          |

You can use the Application Manager to stop and start
the applications.  This can be useful for stopping the
A1111 Web UI if you want to train using Kohya_ss for example.

## Environment Variables

| Variable             | Description                                      | Default                |
|----------------------|--------------------------------------------------|------------------------|
| VENV_PATH            | Set the path for the Python venv for the app     | /workspace/venvs/a1111 |
| JUPYTER_LAB_PASSWORD | Set a password for Jupyter lab                   | not set - no password  |
| DISABLE_AUTOLAUNCH   | Disable Web UIs from launching automatically     | (not set)              |
| DISABLE_SYNC         | Disable syncing if using a RunPod network volume | (not set)              |
| ENABLE_TENSORBOARD   | Enables Tensorboard on port 6006                 | enabled                |

## Logs

Stable Diffusion Web UI, Kohya SS, ComfyUI, and InvokeAI each
create log files, and you can tail the log files instead of
killing the services to view the logs

| Application             | Log file                     |
|-------------------------|------------------------------|
| Stable Diffusion Web UI | /workspace/logs/webui.log    |
| Kohya SS                | /workspace/logs/kohya_ss.log |
| ComfyUI                 | /workspace/logs/comfyui.log  |
| InvokeAI                | /workspace/logs/invokeai.log |

For example:

```bash
tail -f  /workspace/logs/webui.log
```

## Changing launch parameters

You may be used to changing a different file for your
launch parameters. This template uses `webui-user.sh`,
which is located in the webui directory
(`/workspace/stable-diffusion-webui`) to manage the
launch flags such as `--xformers` and `--skip-install`.
You can feel free to edit this file, and then restart
your pod via the hamburger menu to get them to go into
effect, or alternatively use the Application Manager
on port 8000 to stop A1111 and start it again.

## Using your own models

The best ways to get your models onto your pod is
by using `runpodctl` or `croc` or by uploading them to Google
Drive or other cloud storage and downloading them
to your pod from there.