#!/usr/bin/env python3
import json
import runpod
from prettytable import PrettyTable


if __name__ == '__main__':
    runpod = runpod.API()
    response = runpod.get_gpu_types()
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error['message'])
        else:
            gpu_types = resp_json['data']['gpuTypes']
            sorted_gpu_types = sorted(gpu_types, key=lambda x: x["memoryInGb"])

            table = PrettyTable()
            table.field_names = ['ID', 'Name', 'GPU', 'GPU Max', 'Secure', 'Community', 'Spot']

            for gpu in sorted_gpu_types:
                memory = f"{gpu['memoryInGb']} GB"

                if not gpu['secureCloud']:
                    gpu['securePrice'] = '-'

                if not gpu['communityCloud']:
                    gpu['communityPrice'] = '-'

                if gpu['lowestPrice']['minimumBidPrice'] is None:
                    gpu['lowestPrice']['minimumBidPrice'] = '-'

                table.add_row([
                    gpu['id'],
                    gpu['displayName'],
                    memory,
                    gpu['maxGpuCount'],
                    gpu['securePrice'],
                    gpu['communityPrice'],
                    gpu['lowestPrice']['minimumBidPrice']
                ])

            print(table)
    else:
        print(response.status_code)
        print(json.dumps(resp_json, indent=4, default=str))
