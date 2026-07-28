#!/usr/bin/env python3
import argparse
import rpapi


def get_args():
    parser = argparse.ArgumentParser(
        description='Terminate a RunPod pod',
    )

    parser.add_argument(
        '--pod_id', '-pod_id', '--pod', '-pod', '--p', '-p',
        type=str,
        required=True,
        help='pod id (eg. dg31b9aqtupn2z)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    pod_id = args.pod_id
    runpod = rpapi.API()
    response = runpod.terminate_pod(pod_id)

    if response.status_code in (200, 204):
        print(f'Pod {pod_id} has been terminated')
    else:
        print(f'HTTP {response.status_code}')
        try:
            print(response.text)
        except Exception:
            pass
