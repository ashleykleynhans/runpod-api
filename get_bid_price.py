#!/usr/bin/env python3
"""Get pricing for a specific RunPod GPU type."""
import argparse
import json
import rpapi
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box


def get_args():
    parser = argparse.ArgumentParser(
        description='Get pricing for a specific RunPod GPU type',
    )

    parser.add_argument(
        '--gpu_id', '-gpu_id', '--gpu', '-gpu', '--g', '-g',
        type=str,
        required=True,
        help='GPU id (eg. "NVIDIA GeForce RTX 3090")'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    gpu_id = args.gpu_id
    console = Console()
    api = rpapi.API()

    with console.status(f'[bold cyan]Looking up {gpu_id}...[/bold cyan]'):
        response = api.get_bid_price(gpu_id)
        resp_json = response.json()

    if response.status_code != 200:
        console.print(f'[red]HTTP {response.status_code}[/red]')
        console.print(json.dumps(resp_json, indent=4, default=str))
        exit(1)

    if 'errors' in resp_json:
        console.print('[red]ERROR:[/red]')
        for error in resp_json['errors']:
            console.print(f'  {error["message"]}')
        exit(1)

    name = resp_json.get('name', gpu_id)
    gpu_id_val = resp_json.get('id', '')
    memory = resp_json.get('memory', 0)
    manufacturer = resp_json.get('manufacturer', 'Unknown')
    secure = resp_json.get('secure', False)
    community = resp_json.get('community', False)
    price = resp_json.get('price', {})
    secure_price = price.get('secure')
    community_price = price.get('community')
    pool = resp_json.get('pool')
    max_count = resp_json.get('maxCount', {})

    table = Table(
        box=box.ROUNDED,
        show_header=False,
        padding=(0, 2),
    )
    table.add_column(style='bold cyan', width=18)
    table.add_column()

    table.add_row('ID', gpu_id_val)
    table.add_row('Manufacturer', manufacturer)
    table.add_row('VRAM', f'{memory} GB')

    secure_style = 'green' if secure else 'dim'
    table.add_row('Secure Cloud', Text(str(secure), style=secure_style))
    community_style = 'yellow' if community else 'dim'
    table.add_row('Community Cloud', Text(str(community), style=community_style))

    if max_count:
        sc = max_count.get('secure', 0)
        cc = max_count.get('community', 0)
        table.add_row('Max GPUs', f'[green]{sc}[/green] secure / [yellow]{cc}[/yellow] community')

    if pool:
        table.add_row('Serverless Pool', pool)

    table.add_row()
    table.add_row('Secure Price', f'[green]${secure_price}[/green]' if secure_price else '[dim]-[/dim]')
    table.add_row('Community Price', f'[yellow]${community_price}[/yellow]' if community_price else '[dim]-[/dim]')

    console.print()
    console.print(Panel(table, title=f'[bold]{name}[/bold]', border_style='cyan'))
    console.print()
