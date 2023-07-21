# A collection of Python scripts for calling the RunPod GraphQL API

## Getting started

### Clone the repo, create venv and install dependencies

```bash
git clone https://github.com/ashleykleynhans/runpod-api.git
cd runpod-api
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Configure your RunPod API

Copy the `.env.example` file to `.env` as follows:


```bash
cp .env.example .env
```

Then edit the `.env` file and replace the text `INSERT_YOUR_RUNPOD_API_KEY_HERE`
with your RunPod API key that you can get from the [RunPod Settings](
https://www.runpod.io/console/user/settings) in the RunPod Web console.