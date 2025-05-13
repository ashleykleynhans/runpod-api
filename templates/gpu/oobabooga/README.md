# Text Generation Web UI: A Gradio web UI for Large Language Models. Supports transformers, GPTQ, llama.cpp (GGUF), Llama models

>**NOTE:** This template requires at least **CUDA 12.4** to function correctly, please ensure that you use the CUDA filter at the top of the page to ensure that your pod gets the correct CUDA version.

## Version v3.2

* The blocking and non-blocking APIs have been removed in favour of the Open AI compatible API.
* The Open AI compatible API is now on port 5000.

### Included in this Template

* Ubuntu 22.04 LTS
* CUDA 12.1.1
* Python 3.10.12
* [Text Generation Web UI](
  https://github.com/oobabooga/text-generation-webui) v3.2
* Torch 2.6.0
* xformers 0.0.29post3
* [Jupyter Lab](https://github.com/jupyterlab/jupyterlab)
* [code-server](https://github.com/coder/code-server)
* [runpodctl](https://github.com/runpod/runpodctl)
* [OhMyRunPod](https://github.com/kodxana/OhMyRunPod)
* [RunPod File Uploader](https://github.com/kodxana/RunPod-FilleUploader)
* [croc](https://github.com/schollz/croc)
* [rclone](https://rclone.org/)
* speedtest-cli
* screen
* tmux

## Ports

| Connect Port | Internal Port | Description            |
|--------------|---------------|------------------------|
| 3000         | 3001          | Text Generation Web UI |
| 5000         | 5001          | Open AI Compatible API |
| 7777         | 7777          | Code Server            |
| 8888         | 8888          | Jupyter Lab            |
| 2999         | 2999          | RunPod File Uploader   |

## Environment Variables

| Variable             | Description                                                   | Default                                |
|----------------------|---------------------------------------------------------------|----------------------------------------|
| VENV_PATH            | Set the path for the Python venv for the app                  | /workspace/venvs/text-generation-webui |
| JUPYTER_LAB_PASSWORD | Set a password for Jupyter lab                                | not set - no password                  |
| DISABLE_AUTOLAUNCH   | Disable Web UI from launching automatically                   | (not set)                              |
| DISABLE_SYNC         | Disable syncing if using a RunPod network volume              | (not set)                              |
| HF_TOKEN             | Hugging Face Hub token for models that require authentication | (not set)                              |

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
