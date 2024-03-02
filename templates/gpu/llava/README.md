# LLaVA: Large Language and Vision Assistant

## Version 1.4.5 (LLaVA 1.6)

**NOTE:** Although the container logs may say that the Container is READY and port 3000 is accessible,
the model worker will still need to download the model the first time you create the pod, and since the model
is around 20GB in size, this can take a few minutes.  You can monitor the progress by opening the **model-worker.log**
log file in Jupyter lab or tailing it using the instructions below (See the Logs section below).

I recommend A6000 or a GPU with more than 24GB of VRAM if you want to use the 13b model,
and a GPU with 24GB of VRAM if you want to use the 7b model.

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 11.8
* Python 3.10.12
* [LLaVA](
  https://github.com/haotian-liu/llava) v1.2.0 (LLaVA 1.6)
* Torch 2.1.2
* Jupyter Lab
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)
* speedtest-cli
* screen
* tmux
* llava-v1.6-mistral-7b model

## Ports

| Port | Description          |
|------|----------------------|
| 3000 | LLaVA                |
| 8888 | Jupyter Lab          |
| 2999 | RunPod File Uploader |

## Environment Variables

| Variable           | Description                                  | Default                          |
|--------------------|----------------------------------------------|----------------------------------|
| VENV_PATH          | Set the path for the Python venv for the app | /workspace/venvs/llava           |
| DISABLE_AUTOLAUNCH | Disable LLaVA from launching automatically   | enabled                          |
| MODEL              | The path of the Huggingface model            | liuhaotian/llava-v1.6-mistral-7b |

## Models

**NOTE:**
> If you select a 13B or larger model, CUDA will result in OOM errors
> with a GPU that has less than 48GB of VRAM, so A6000 or higher is
> recommended for 13B.

You can add an environment called `MODEL` to your Docker container to
specify the model that should be downloaded.  If the `MODEL` environment
variable is not set, the model will default to `liuhaotian/llava-v1.6-mistral-7b`.

### LLaVA-v1.6

| Model                                                                            | Environment Variable Value       | Version    | LLM           | Default |
|----------------------------------------------------------------------------------|----------------------------------|------------|---------------|---------|
| [llava-v1.6-vicuna-7b](https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b)   | liuhaotian/llava-v1.6-vicuna-7b  | LLaVA-1.6  | Vicuna-7B     | no      |
| [llava-v1.6-vicuna-13b](https://huggingface.co/liuhaotian/llava-v1.6-vicuna-13b) | liuhaotian/llava-v1.6-vicuna-13b | LLaVA-1.6  | Vicuna-13B    | no      |
| [llava-v1.6-mistral-7b](https://huggingface.co/liuhaotian/llava-v1.6-mistral-7b) | liuhaotian/llava-v1.6-mistral-7b | LLaVA-1.6  | Mistral-7B    | yes     |
| [llava-v1.6-34b](https://huggingface.co/liuhaotian/llava-v1.6-34b)               | liuhaotian/llava-v1.6-34b        | LLaVA-1.6  | Hermes-Yi-34B | no      |

### LLaVA-v1.5

| Model                                                              | Environment Variable Value       | Version   | Size | Default |
|--------------------------------------------------------------------|----------------------------------|-----------|------|---------|
| [llava-v1.5-7b](https://huggingface.co/liuhaotian/llava-v1.5-7b)   | liuhaotian/llava-v1.5-7b         | LLaVA-1.5 | 7B   | no      |
| [llava-v1.5-13b](https://huggingface.co/liuhaotian/llava-v1.5-13b) | liuhaotian/llava-v1.5-13b        | LLaVA-1.5 | 13B  | no      |
| [BakLLaVA-1](https://huggingface.co/SkunkworksAI/BakLLaVA-1)       | SkunkworksAI/BakLLaVA-1          | LLaVA-1.5 | 7B   | no      |

## Logs

LLaVA creates log files, and you can tail the log files
instead of killing the services to view the logs.

| Application   | Log file                         |
|---------------|----------------------------------|
| Controller    | /workspace/logs/controller.log   |
| Webserver     | /workspace/logs/webserver.log    |
| Model Worker  | /workspace/logs/model-worker.log |

For example:

```bash
tail -f /workspace/logs/webserver.log
```

## General

Note that this does not work out of the box with
encrypted volumes!

This is a custom packaged template for LLaVA.

I do not maintain the code for this repo,
I just package everything together so that it is
easier for you to use.

If you need help with settings, etc. You can feel free
to ask me, but just keep in mind that I am not an expert
at LLaVA! I'll try my best to help, but the
RunPod community may be better at helping you.