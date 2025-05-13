# FramePack

## Version 1.0.0

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 12.1
* Python 3.12.9
* [FramePack](
  https://github.com/lllyasviel/FramePack)
* Torch 2.5.1
* xformers 0.0.29.post1
* [Jupyter Lab](https://github.com/jupyterlab/jupyterlab)
* [code-server](https://github.com/coder/code-server)
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)

## Ports

| Port | Description          |
|------|----------------------|
| 3000 | FramePack            |
| 8888 | Jupyter Lab          |
| 2999 | RunPod File Uploader |

## Environment Variables

| Variable             | Description                                      | Default                    |
|----------------------|--------------------------------------------------|----------------------------|
| JUPYTER_LAB_PASSWORD | Set a password for Jupyter lab                   | not set - no password      |
| DISABLE_AUTOLAUNCH   | Disable FramePack from launching automatically   | (not set)                  |
| DISABLE_SYNC         | Disable syncing if using a RunPod network volume | (not set)                  |

## Logs

FramePack creates a log file, and you can tail the log instead of
killing the service to view the logs.

| Application | Log file                      |
|-------------|-------------------------------|
| FramePack   | /workspace/logs/framepack.log |

For example:

```bash
tail -f /workspace/logs/framepack.log
```
