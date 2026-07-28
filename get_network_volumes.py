#!/usr/bin/env python3
import rpapi
import json
from rich.console import Console
from rich.table import Table


if __name__ == '__main__':
    console = Console()
    api = rpapi.API()
    response = api.get_network_volumes()
    resp_json = response.json()

    if response.status_code != 200:
        console.print(f"[red]HTTP {response.status_code}[/red]")
        console.print_json(json.dumps(resp_json, default=str))
        exit(1)

    if 'errors' in resp_json:
        for error in resp_json['errors']:
            console.print(f"[red]ERROR:[/red] {error['message']}")
        exit(1)

    volumes = resp_json.get('networkVolumes', [])

    table = Table(title="Network Volumes")
    table.add_column("Name", style="bold")
    table.add_column("ID", style="dim")
    table.add_column("Size (GB)", justify="right")
    table.add_column("Data Center", style="cyan")

    for vol in sorted(volumes, key=lambda v: v['name']):
        table.add_row(
            vol['name'],
            vol['id'],
            str(vol['size']),
            vol.get('dataCenter', vol.get('dataCenterId', ''))
        )

    console.print(table)
