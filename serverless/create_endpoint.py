#!/usr/bin/env python3
import argparse
import json
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import rpapi


def get_args():
    parser = argparse.ArgumentParser(
        description='Create a Serverless Endpoint',
    )

    parser.add_argument(
        '--name', '-name', '-n',
        type=str,
        required=True,
        help='endpoint name (eg. MY-ENDPOINT)'
    )

    parser.add_argument(
        '--template-id', '-template-id', '-t',
        type=str,
        required=True,
        help='template id (eg. oqemm2d5jy)'
    )

    parser.add_argument(
        '--gpu-ids', '-gpu-ids', '-g',
        type=str,
        required=True,
        help='GPU type IDs (eg. NVIDIA A40)'
    )

    parser.add_argument(
        '--network-volume-id', '-network-volume-id', '-nv',
        type=str,
        required=False,
        default=None,
        help='network volume id'
    )

    parser.add_argument(
        '--workers-min', '-workers-min',
        type=int,
        required=False,
        default=0,
        help='minimum number of workers (default: 0)'
    )

    parser.add_argument(
        '--workers-max', '-workers-max',
        type=int,
        required=False,
        default=3,
        help='maximum number of workers (default: 3)'
    )

    parser.add_argument(
        '--idle-timeout', '-idle-timeout',
        type=int,
        required=False,
        default=5,
        help='idle timeout in seconds (default: 5)'
    )

    parser.add_argument(
        '--locations', '-locations', '-l',
        type=str,
        required=False,
        default=None,
        help='data center locations (eg. EU-IS-1)'
    )

    parser.add_argument(
        '--scaler-type', '-scaler-type',
        type=str,
        required=False,
        default='QUEUE_DELAY',
        help='scaler type (default: QUEUE_DELAY)'
    )

    parser.add_argument(
        '--scaler-value', '-scaler-value',
        type=int,
        required=False,
        default=4,
        help='scaler value (default: 4)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    serverless = rpapi.Serverless()

    config = {
        'name': args.name,
        'gpu': {
            'pools': [p.strip() for p in args.gpu_ids.split(',') if p.strip()],
            'count': 1,
        },
        'workers': {
            'min': args.workers_min,
            'max': args.workers_max,
        },
        'timeout': args.idle_timeout * 1000,
    }

    if args.network_volume_id:
        config['networkVolumes'] = [args.network_volume_id]

    if args.locations:
        config['dataCenterIds'] = [args.locations]

    if args.scaler_type and args.scaler_value:
        config['scaling'] = {
            'type': args.scaler_type,
            'value': args.scaler_value,
        }

    response = serverless.create_endpoint(config)

    if response.status_code in (200, 201):
        resp_json = response.json()

        if 'errors' in resp_json:
            print('ERROR:')
            for error in resp_json['errors']:
                print(error.get('message', str(error)))
        else:
            print(json.dumps(resp_json, indent=4, default=str))
    else:
        print(f'ERROR: HTTP Status code: {response.status_code}')
