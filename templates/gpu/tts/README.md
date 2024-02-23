## TTS Generation Web UI (Bark, MusicGen + AudioGen, Tortoise, RVC, Vocos, Demucs, SeamlessM4T, MAGNeT)

### Version 2.0.4

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 11.8
* Python 3.10.12
* [TTS Generation Web UI](
  https://github.com/rsxdalv/tts-generation-webui)
* Torch 2.0.0
* xformers 0.0.19
* Jupyter Lab
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/
* screen
* tmux

### Ports

| Port | Description                        |
|------|------------------------------------|
| 3000 | Gradio TTS Generation Web UI       |
| 3005 | React TTS Generation Web UI (beta) |
| 8888 | Jupyter Lab                        |
| 2999 | RunPod File Uploader               |

### Environment Variables

| Variable           | Description                                                | Default  |
|--------------------|------------------------------------------------------------|----------|
| JUPYTER_PASSWORD   | Password for Jupyter Lab                                   | Jup1t3R! |
| DISABLE_AUTOLAUNCH | Disable TTS Generation Web UI from launching automatically | enabled  |

## Logs

TTS Generation Web UI creates a log file, and you can tail the log file
instead of killing the services to view the logs

| Application           | Log file                |
|-----------------------|-------------------------|
| TTS Generation Web UI | /workspace/logs/tts.log |

For example:

```bash
tail -f /workspace/logs/tts.log
```

### Jupyter Lab

If you wish to use the Jupyter lab, you must set
the **JUPYTER_PASSWORD** environment variable in the
Template Overrides configuration when deploying
your pod.

### General

Note that this does not work out of the box with
encrypted volumes!

This is a custom packaged template for TTS Generation
Web UI.

I do not maintain the code for this repo,
I just package everything together so that it is
easier for you to use.

If you need help with settings, etc. You can feel free
to ask me, but just keep in mind that I am not an expert
at TTS Generation! I'll try my best to help, but the
RunPod community may be better at helping you.

### Uploading to Google Drive

If you're done with the pod and would like to send
things to Google Drive, you can use this colab to do it
using **runpodctl**. You run the **runpodctl** either in
a web terminal (found in the pod connect menu), or
in a terminal on the desktop.