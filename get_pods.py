#!/usr/bin/env python3
import runpod
import json


if __name__ == '__main__':
    runpod = runpod.API()
    response = runpod.get_pods()
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        elif 'data' in resp_json and 'myself' in resp_json['data'] and resp_json['data']['myself'] is not None:
            print(json.dumps(resp_json['data']['myself']['pods'], indent=4, default=str))
        else:
            print('ERROR: Unable to get a list of pods')
            print(json.dumps(resp_json, indent=4, default=str))
    else:
        print(response.status_code)
        print(json.dumps(resp_json, indent=4, default=str))
