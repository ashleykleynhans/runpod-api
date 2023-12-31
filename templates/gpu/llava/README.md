## LLaVA: Large Language and Vision Assistant

### Version 1.1.1

**NOTE:** Although the container logs may say that the Container is READY and port 3000 is accessible,
the model worker will still need to download the model the first time you create the pod, and since the model
is around 20GB in size, this can take a few minutes.  You can monitor the progress by opening the **model-worker.log**
log file in Jupyter lab or tailing it using the instructions below (See the Logs section below).

I recommend A6000 or a GPU with more than 24GB of VRAM because the model tends to get GPU OOM errors with 24GB
or less of VRAM.

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 11.8
* Python 3.10.12
* [LLaVA](
  https://github.com/haotian-liu/llava) v1.1.1
* Torch 2.0.1
* xformers 0.0.22

### Ports

| Port | Description |
|------|-------------|
| 3000 | LLaVA       |
| 8888 | Jupyter Lab |

### Environment Variables

| Variable           | Description                                 | Default  |
|--------------------|---------------------------------------------|----------|
| JUPYTER_PASSWORD   | Password for Jupyter Lab                    | Jup1t3R! |
| DISABLE_AUTOLAUNCH | Disable LLaVA from launching automatically  | enabled  |

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

### Jupyter Lab

If you wish to use the Jupyter lab, you must set
the **JUPYTER_PASSWORD** environment variable in the
Template Overrides configuration when deploying
your pod.

### General

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

### Uploading to Google Drive

If you're done with the pod and would like to send
things to Google Drive, you can use this colab to do it
using **runpodctl**. You run the **runpodctl** either in
a web terminal (found in the pod connect menu), or
in a terminal on the desktop.