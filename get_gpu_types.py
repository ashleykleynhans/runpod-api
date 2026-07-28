#!/usr/bin/env python3
"""Display available GPU types with pricing from the Runpod API."""
import json
import rpapi
from rich.console import Console
from rich.table import Table
from rich.text import Text


if __name__ == '__main__':
    console = Console()
    runpod = rpapi.API()
    response = runpod.get_gpu_types()
    resp_json = response.json()

    if response.status_code == 200:
        if 'errors' in resp_json:
            console.print('[red]ERROR:[/red]')
            for error in resp_json['errors']:
                console.print(f'  {error["message"]}')
        else:
            gpu_types = resp_json['gpus']
            sorted_gpu_types = sorted(gpu_types, key=lambda x: x['memory'])

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

            for gpu in sorted_gpu_types:
                memory = f'{gpu["memory"]} GB'
                price = gpu.get('price', {})

                if gpu.get('secure'):
                    secure = Text(str(price.get('secure', '-')), style='green')
                else:
                    secure = Text('-', style='dim')

                if gpu.get('community'):
                    community = Text(str(price.get('community', '-')), style='yellow')
                else:
                    community = Text('-', style='dim')

                max_count = gpu.get('maxCount', {})
                max_gpu = max_count.get('secure', 0) or max_count.get('community', 0)

                table.add_row(
                    gpu['name'],
                    gpu['id'],
                    memory,
                    str(max_gpu),
                    secure,
                    community,
                )

            console.print(table)
    else:
        console.print(f'[red]HTTP {response.status_code}[/red]')
        console.print(json.dumps(resp_json, indent=4, default=str))
