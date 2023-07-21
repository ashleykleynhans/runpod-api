#!/usr/bin/env python3
import runpod
import json

if __name__ == '__main__':
    runpod = runpod.API()
    response = runpod.get_myself()
    resp_json = response.json()

    if response.status_code == 200:
        myself = resp_json['data']['myself']
        print(json.dumps(myself, indent=4, default=str))
    else:
        print('ERROR:')
        print('Status code: ' + response.status_code)
        print(json.dumps(resp_json, indent=4, default=str))
