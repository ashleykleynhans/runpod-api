# Fooocus: Focus on prompting and generating

## Version 2.2.0

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 11.8
* Python 3.10.12
* [Fooocus](https://github.com/lllyasviel/Fooocus) 2.2.0
* Torch 2.0.1
* xformers 0.0.22
* Jupyter Lab
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)

## Ports

| Port | Description |
|------|-------------|
| 3000 | Fooocus     |
| 8888 | Jupyter Lab |
| 2999 | RunPod File Uploader |

## Environment Variables

| Variable           | Description                                  | Default                  |
|--------------------|----------------------------------------------|--------------------------|
| VENV_PATH          | Set the path for the Python venv for the app | /workspace/venvs/fooocus |
| DISABLE_AUTOLAUNCH | Disable Web UIs from launching automatically | (not set)                |
| PRESET             | Fooocus Preset (anime/realistic)             | (not set)                |


## Logs

Fooocus creates log files, and you can tail the log files
instead of killing the services to view the logs.

| Application | Log file                    |
|-------------|-----------------------------|
| Fooocus     | /workspace/logs/fooocus.log |

For example:

```bash
tail -f /workspace/logs/fooocus.log
```

## General

Note that this does not work out of the box with
encrypted volumes!

This is a custom packaged template for Fooocus.

I do not maintain the code for this repo,
I just package everything together so that it is
easier for you to use.

If you need help with settings, etc. You can feel free
to ask me, but just keep in mind that I am not an expert
at Fooocus! I'll try my best to help, but the
RunPod community may be better at helping you.

## Uploading to Google Drive

If you're done with the pod and would like to send
things to Google Drive, you can use this colab to do it
using `runpodctl`. You run the `runpodctl` either in
a web terminal (found in the pod connect menu), or
in a terminal on the desktop.