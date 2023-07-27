## Text Generation Web UI and API for running Large Language Models like LLaMA, llama.cpp, GPT-J, Pythia, OPT, and GALACTICA 

### Version 1.5.0

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 11.8
* Python 3.10.6
* [Text Generation Web UI](
  https://github.com/oobabooga/text-generation-webui) v1.5
* Text Generation API
* Torch 2.0.1

### Ports

| Port | Description                    |
|------|--------------------------------|
| 3000 | Text Generation Web UI         |
| 5000 | Text Generation REST API       |
| 5005 | Text Generation Websockets API |
| 8888 | Jupyter Lab                    |

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
the `JUPYTER_PASSWORD` environment variable in the
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

Please wait until the GPU Utilization % is 0 before
attempting to connect. You will likely get a 502 error
before that as the pod is still getting ready to be used.

### Uploading to Google Drive

If you're done with the pod and would like to send
things to Google Drive, you can use this colab to do it
using `runpodctl`. You run the `runpodctl` either in
a web terminal (found in the pod connect menu), or
in a terminal on the desktop.
