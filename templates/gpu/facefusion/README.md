## FaceFusion: Next generation face swapper and enhancer

### Version 1.1.0

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 11.8
* Python 3.10.12
* [FaceFusion](
  https://github.com/facefusion/facefusion) 1.1.0
* Torch 2.0.1
* xformers 0.0.21

### Ports

| Port | Description |
|------|-------------|
| 3000 | FaceFusion  |
| 8888 | Jupyter Lab |

### Environment Variables

| Variable           | Description                                     | Default  |
|--------------------|-------------------------------------------------|----------|
| JUPYTER_PASSWORD   | Password for Jupyter Lab                        | Jup1t3R! |
| DISABLE_AUTOLAUNCH | Disable FaceFusion from launching automatically | enabled  |

## Logs

FaceFusion creates a log file, and you can tail the log file
instead of killing the services to view the logs

| Application | Log file                       |
|-------------|--------------------------------|
| FaceFusion  | /workspace/logs/facefusion.log |

For example:

```bash
tail -f /workspace/logs/facefusion.log
```

### Jupyter Lab

If you wish to use the Jupyter lab, you must set
the **JUPYTER_PASSWORD** environment variable in the
Template Overrides configuration when deploying
your pod.

### General

Note that this does not work out of the box with
encrypted volumes!

This is a custom packaged template for FaceFusion.

I do not maintain the code for this repo,
I just package everything together so that it is
easier for you to use.

If you need help with settings, etc. You can feel free
to ask me, but just keep in mind that I am not an expert
at FaceFusion! I'll try my best to help, but the
RunPod community may be better at helping you.

### Uploading to Google Drive

If you're done with the pod and would like to send
things to Google Drive, you can use this colab to do it
using **runpodctl**. You run the **runpodctl** either in
a web terminal (found in the pod connect menu), or
in a terminal on the desktop.