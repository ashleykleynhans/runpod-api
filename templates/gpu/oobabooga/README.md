## Text Generation Web UI: A Gradio web UI for Large Language Models. Supports transformers, GPTQ, llama.cpp (GGUF), Llama models

>**NOTE:** This template requires at least *CUDA 12.1* to function correctly, please ensure that you use the CUDA filter at the top of the page to ensure that your pod gets the correct CUDA version.

>**NOTE:** The legacy APIs no longer work with the latest version of the Text Generation Web UI.  They were deprecated since November 2023 and have now been completely removed. If you want to use the LEGACY APIs, please set the image tag to **1.9.5**.  You will also have to add port 6000 for the legacy REST API and/or port 6005 for the legacy Websockets API.

### Version 1.12.4

* The blocking and non-blocking APIs have been removed in favour of the Open AI compatible API.
* The Open AI compatible API is now on port 5000.

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 12.1.1
* Python 3.10.12
* [Text Generation Web UI](
  https://github.com/oobabooga/text-generation-webui)
* [Legacy API Extension](https://github.com/ashleykleynhans/oobabooga-legacy-api-extension)
* Torch 2.1.2
* xformers 0.0.23post1
* Jupyter Lab
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)
* speedtest-cli
* screen
* tmux

### Ports

| Port | Description                 |
|------|-----------------------------|
| 3000 | Text Generation Web UI      |
| 5000 | Open AI Compatible API      |
| 8888 | Jupyter Lab                 |
| 2999 | RunPod File Uploader        |

### Environment Variables

| Variable           | Description                                     | Default  |
|--------------------|-------------------------------------------------|----------|
| JUPYTER_PASSWORD   | Password for Jupyter Lab                        | Jup1t3R! |
| DISABLE_AUTOLAUNCH | Disable the Web UI from launching automatically | enabled  |

## Logs

The Text Generation Web UI creates a log file, and you can tail the log file
instead of killing the services to view the logs

| Application           | Log file                    |
|-----------------------|-----------------------------|
| Text Generation WebUI | /workspace/logs/textgen.log |

For example:

```bash
tail -f /workspace/logs/textgen.log
```

### Jupyter Lab

If you wish to use the Jupyter lab, you must set
the **JUPYTER_PASSWORD** environment variable in the
Template Overrides configuration when deploying
your pod.

### General

Note that this does not work out of the box with
encrypted volumes!

This is a custom packaged template for The Text
Generation Web UI.

I do not maintain the code for this repo,
I just package everything together so that it is
easier for you to use.

If you need help with settings, etc. You can feel free
to ask me, but just keep in mind that I am not an expert
at the Text Generation Web UI! I'll try my best to help, but the
RunPod community may be better at helping you.

### Uploading to Google Drive

If you're done with the pod and would like to send
things to Google Drive, you can use this colab to do it
using **runpodctl**. You run the **runpodctl** either in
a web terminal (found in the pod connect menu), or
in a terminal on the desktop.