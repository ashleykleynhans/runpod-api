#!/usr/bin/env python3
"""Display available GPU types with pricing from the Runpod API."""
import json
import runpod
from rich.console import Console
from rich.table import Table
from rich.text import Text


if __name__ == '__main__':
    console = Console()
    runpod = runpod.API()
    response = runpod.get_gpu_types()
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            console.print('[red]ERROR:[/red]')
            for error in resp_json['errors']:
                console.print(f'  {error["message"]}')
        else:
            gpu_types = resp_json['data']['gpuTypes']
            sorted_gpu_types = sorted(gpu_types, key=lambda x: x['memoryInGb'])

            table = Table(
                title='Runpod GPU Types',
                padding=(0, 1),
            )
            table.add_column('Name', style='bold', max_width=30)
            table.add_column('ID', style='cyan', max_width=48)
            table.add_column('VRAM', justify='right', width=8)
            table.add_column('Max', justify='right', width=5)
            table.add_column('Secure', justify='right', width=8)
            table.add_column('Community', justify='right', width=10)
            table.add_column('Spot', justify='right', width=8)

            for gpu in sorted_gpu_types:
                memory = f'{gpu["memoryInGb"]} GB'

                if gpu['secureCloud']:
                    secure = Text(str(gpu['securePrice']), style='green')
                else:
                    secure = Text('-', style='dim')

                if gpu['communityCloud']:
                    community = Text(str(gpu['communityPrice']), style='yellow')
                else:
                    community = Text('-', style='dim')

                spot_price = gpu['lowestPrice']['minimumBidPrice']
                if spot_price is not None:
                    spot = Text(str(spot_price), style='yellow')
                else:
                    spot = Text('-', style='dim')

                table.add_row(
                    gpu['displayName'],
                    gpu['id'],
                    memory,
                    str(gpu['maxGpuCount']),
                    secure,
                    community,
                    spot,
                )

            console.print(table)
    else:
        console.print(f'[red]HTTP {response.status_code}[/red]')
        console.print(json.dumps(resp_json, indent=4, default=str))
