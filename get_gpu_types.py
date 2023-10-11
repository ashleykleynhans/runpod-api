#!/usr/bin/env python3
import json
import runpod


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

            #print(json.dumps(sorted_gpu_types, indent=4, default=str))

            # Define the column widths
            widths = [39, 22, 8, 9, 9, 11, 9]

            print('ID                                     Name                  GPU     GPU Max  Secure   Community  Spot')
            print('-------------------------------------  --------------------  ------  -------  -------  ---------  ------')

            for pod in sorted_gpu_types:
                memory = f"{pod['memoryInGb']} GB"
                row = f"{pod['id']:<{widths[0]}}"
                row += f"{pod['displayName']:<{widths[1]}}"
                row += f"{memory:<{widths[2]}}"
                row += f"{pod['maxGpuCount']:<{widths[3]}}"

                if not pod['secureCloud']:
                    pod['securePrice'] = '-'

                if not pod['communityCloud']:
                    pod['communityPrice'] = '-'

                row += f"{pod['securePrice']:<{widths[4]}}"
                row += f"{pod['communityPrice']:<{widths[5]}}"

                if pod['lowestPrice']['minimumBidPrice'] is None:
                    pod['lowestPrice']['minimumBidPrice'] = '-'

                row += f"{pod['lowestPrice']['minimumBidPrice']:<{widths[6]}}"
                print(row)
    else:
        print(response.status_code)
        print(json.dumps(resp_json, indent=4, default=str))
