# SUPIR (Scaling Up to Excellence: Practicing Model Scaling for Photo-Realistic Image Restoration In the Wild)

## 1.4.0

**NOTE:** This template requires **CUDA 12.1** or higher, ensure that you use the CUDA filter to select the correct CUDA versions.

**NOTE:** This needs at least 24GB VRAM for 1x upscale. If you want to upscale more than 1x, you will need more than 24GB of VRAM.  48GB VRAM is recommended.

**NOTE**: The Docker image is 50GB in size because it includes all of the models so that they don't need to be downloaded at run time.

**NOTE:** Loading of models on start takes a few minutes, so you can view the log to watch the progress. You will be able to access the port when you see `Running on local URL:  http://0.0.0.0:3001` in the log.

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 12.1
* Python 3.10.12
* [SUPIR](
  https://github.com/Fanghua-Yu/SUPIR)
* Torch 2.2.0
* xformers 0.0.24
* Jupyter Lab
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)

## Ports

| Port | Description          |
|------|----------------------|
| 3000 | SUPIR                |
| 8888 | Jupyter Lab          |
| 2999 | RunPod File Uploader |

## Environment Variables

| Variable             | Description                                | Default                |
|----------------------|--------------------------------------------|------------------------|
| VENV_PATH          | Set the path for the Python venv for the app | /workspace/venvs/SUPIR |
| DISABLE_AUTOLAUNCH   | Disable SUPIR from launching automatically | (not set)              |
| NO_GPU_OPTIMIZATION  | Disable GPU optimization for A100/H100     | (not set)              |

## Logs

SUPIR creates log files, and you can tail the log files
instead of killing the services to view the logs.

| Application | Log file                  |
|-------------|---------------------------|
| SUPIR       | /workspace/logs/supir.log |

For example:

```bash
tail -f /workspace/logs/supir.log
```

## Models

| Model                             | Description |
|-----------------------------------|-------------|
| SUPIR-v0F.ckpt                    | SUPIR F     |
| SUPIR-v0Q.ckpt                    | SUPIR Q     |
| liuhaotian/llava-v1.5-7b          | LLaVA       |
| sd_xl_base_1.0_0.9vae.safetensors | SDXL        |
| openai/clip-vit-large-patch14-336 | LLaVA CLIP  |
| openai/clip-vit-large-patch14     | SDXL CLIP1  |
| open_clip_pytorch_model.bin       | SDXL CLIP2  |

## General

Note that this does not work out of the box with
encrypted volumes!

This is a custom packaged template for SUPIR.

I do not maintain the code for this repo,
I just package everything together so that it is
easier for you to use.

If you need help with settings, etc. You can feel free
to ask me, but just keep in mind that I am not an expert
at SUPIR! I'll try my best to help,
but the RunPod community may be better at helping you.

## Uploading to Google Drive

If you're done with the pod and would like to send
things to Google Drive, you can use this colab to do it
using `runpodctl`. You run the `runpodctl` either in
a web terminal (found in the pod connect menu), or
in a terminal on the desktop.