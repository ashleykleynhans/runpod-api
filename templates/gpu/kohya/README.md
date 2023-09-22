## Kohya SS

### Version 1.3.1

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 11.8
* Python 3.10.12
* [Kohya_ss](https://github.com/bmaltais/kohya_ss) v21.8.9
* Torch 2.0.1
* xformers 0.0.21
* sd_xl_base_1.0.safetensors

### Ports

| Port | Description             |
|------|-------------------------|
| 3000 | Kohya_ss                |
| 8888 | Jupyter Lab             |

### Environment Variables

| Variable           | Description                                  | Default  |
|--------------------|----------------------------------------------|----------|
| JUPYTER_PASSWORD   | Password for Jupyter Lab                     | Jup1t3R! |
| DISABLE_AUTOLAUNCH | Disable Web UIs from launching automatically | enabled  |

## Logs

Kohya SS creates a log files, and you can tail the log file
instead of killing the services to view the logs

| Application             | Log file                     |
|-------------------------|------------------------------|
| Kohya SS                | /workspace/logs/kohya_ss.log |

For example:

```bash
tail -f /workspace/logs/kohya_ss.log
```

### Jupyter Lab

If you wish to use the Jupyter lab, you must set
the **JUPYTER_PASSWORD** environment variable in the
Template Overrides configuration when deploying
your pod.

### General

Note that this does not work out of the box with
encrypted volumes!

This is a custom packaged template for the Kohya_ss
Web UI.

I do not maintain the code for this repo,
I just package everything together so that it is
easier for you to use.

If you need help with settings, etc. You can feel free
to ask me, but just keep in mind that I am not an expert
at Kohya_ss! I'll try my best to help, but the
RunPod community or Automatic/Kohya_ss communities
may be better at helping you.

### Using your own models

The best ways to get your models onto your pod is
by using **runpodctl** or by uploading them to Google
Drive or other cloud storage and downloading them
to your pod from there.

### Uploading to Google Drive

If you're done with the pod and would like to send
things to Google Drive, you can use this colab to do it
using **runpodctl**. You run the **runpodctl** either in
a web terminal (found in the pod connect menu), or
in a terminal on the desktop.