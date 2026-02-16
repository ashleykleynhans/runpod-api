# InstantID : Zero-shot Identity-Preserving Generation in Seconds

## Version 2.6.0

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 12.5
* Python 3.10.12
* [InstantID](
  https://github.com/InstantID/InstantID)
* Torch 2.6.0
* xformers 0.0.29.post3
* Jupyter Lab
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)

## Ports

| Connect Port | Internal Port | Description          |
|--------------|---------------|----------------------|
| 3000         | 3001          | InstantID            |
| 7777         | 7777          | Code Server          |
| 8888         | 8888          | Jupyter Lab          |
| 2999         | 2999          | RunPod File Uploader |

## Environment Variables

| Variable             | Description                                      | Default               |
|----------------------|--------------------------------------------------|-----------------------|
| JUPYTER_LAB_PASSWORD | Set a password for Jupyter lab                   | not set - no password |
| DISABLE_AUTOLAUNCH   | Disable InstantID from launching automatically   | (not set)             |
| DISABLE_SYNC         | Disable syncing if using a RunPod network volume | (not set)             |

## Logs

InstantID creates log files, and you can tail the log files
instead of killing the services to view the logs.

| Application  | Log file                      |
|--------------|-------------------------------|
| InstantID    | /workspace/logs/InstantID.log |

For example:

```bash
tail -f /workspace/logs/InstantID.log
```
