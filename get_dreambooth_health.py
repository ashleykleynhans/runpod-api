#!/usr/bin/env python3
import runpod
import json


if __name__ == '__main__':
    serverless = runpod.Serverless()
    response = serverless.get_dreambooth_health()
    resp_json = response.json()

    if response.status_code == 401:
        print('ERROR 401: Unauthorized')
    elif response.status_code == 200:
        print(json.dumps(resp_json, indent=4, default=str))
