# Stable Diffusion WebUI Forge

## 1.1.1

**NOTE:** This template requires **CUDA 12.1** or higher, ensure that you use the CUDA filter to select the correct CUDA versions.

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 12.1
* Python 3.10.12
* [Stable Diffusion WebUI Forge](
  https://github.com/lllyasviel/stable-diffusion-webui-forge)
* Torch 2.1.2
* xformers 0.0.23.post1
* Jupyter Lab
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)

## Ports

| Port | Description |
|------|-------------|
| 3000 | Forge       |
| 8888 | Jupyter Lab |
| 2999 | RunPod File Uploader |

## Environment Variables

| Variable           | Description                                    | Default                                       |
|--------------------|------------------------------------------------|-----------------------------------------------|
| VENV_PATH          | Set the path for the Python venv for the app   | /workspace/venvs/stable-diffusion-webui-forge |
| DISABLE_AUTOLAUNCH | Disable Forge from launching automatically     | (not set)                                     |

## Logs

Forge creates log files, and you can tail the log files
instead of killing the services to view the logs.

| Application | Log file                  |
|-------------|---------------------------|
| Forge       | /workspace/logs/forge.log |

For example:

```bash
tail -f /workspace/logs/forge.log
```

## General

Note that this does not work out of the box with
encrypted volumes!

This is a custom packaged template for Stable Diffusion WebUI Forge.

I do not maintain the code for this repo,
I just package everything together so that it is
easier for you to use.

If you need help with settings, etc. You can feel free
to ask me, but just keep in mind that I am not an expert
at Stable Diffusion WebUI Forge! I'll try my best to help,
but the RunPod community may be better at helping you.

## Uploading to Google Drive

If you're done with the pod and would like to send
things to Google Drive, you can use this colab to do it
using `runpodctl`. You run the `runpodctl` either in
a web terminal (found in the pod connect menu), or
in a terminal on the desktop.