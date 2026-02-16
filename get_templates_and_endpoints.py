#!/usr/bin/env python3
import runpod
import json
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


if __name__ == '__main__':
    console = Console()
    api = runpod.API()
    response = api.get_templates_and_endpoints()
    resp_json = response.json()

    if response.status_code != 200:
        console.print(f"[red]HTTP {response.status_code}[/red]")
        console.print_json(json.dumps(resp_json, default=str))
        exit(1)

    if 'errors' in resp_json:
        for error in resp_json['errors']:
            console.print(f"[red]ERROR:[/red] {error['message']}")
        exit(1)

    myself = resp_json.get('data', {}).get('myself')
    if myself is None:
        console.print('[red]ERROR:[/red] Unable to get account data')
        console.print_json(json.dumps(resp_json, default=str))
        exit(1)

    templates = [t for t in myself.get('podTemplates', []) if not t.get('isRunpod')]
    endpoints = myself.get('endpoints', [])

    # Group endpoints by templateId
    endpoints_by_template = defaultdict(list)
    for ep in endpoints:
        endpoints_by_template[ep['templateId']].append(ep)

    for template in sorted(templates, key=lambda t: t['name']):
        tid = template['id']
        associated = endpoints_by_template.get(tid, [])

        # Build template info
        title = template['name']
        if associated:
            title += f" ({len(associated)} endpoint{'s' if len(associated) != 1 else ''})"

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style="bold cyan", min_width=10)
        table.add_column()
        table.add_row("ID", tid)
        table.add_row("Image", template['imageName'])
        table.add_row("Public", str(template['isPublic']))
        table.add_row("Serverless", str(template['isServerless']))

        if associated:
            for i, ep in enumerate(associated):
                gpu_list = ep.get('gpuIds') or ''
                workers = f"{ep['workersMin']}-{ep['workersMax']} (standby: {ep['workersStandby']})"
                if i == 0:
                    table.add_row("", "")
                ep_text = Text()
                ep_text.append(ep['name'], style="bold")
                ep_text.append(f"  {ep['id']}", style="dim")
                table.add_row("Endpoint", ep_text)
                table.add_row("  Workers", workers)
                if gpu_list:
                    table.add_row("  GPUs", gpu_list)

        border_style = "green" if associated else "dim"
        console.print(Panel(table, title=f"[bold]{title}[/bold]", border_style=border_style))

    # Show endpoints that reference a template not in the user's template list
    user_template_ids = {t['id'] for t in templates}
    orphaned = [ep for ep in endpoints if ep['templateId'] not in user_template_ids]
    if orphaned:
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style="bold cyan", min_width=14)
        table.add_column()
        for i, ep in enumerate(orphaned):
            if i > 0:
                table.add_row("", "")
            tpl = ep.get('template') or {}
            ep_text = Text()
            ep_text.append(ep['name'], style="bold")
            ep_text.append(f"  {ep['id']}", style="dim")
            table.add_row("Endpoint", ep_text)
            table.add_row("  Template ID", ep['templateId'])
            if tpl.get('name'):
                table.add_row("  Template", tpl['name'])
            if tpl.get('imageName'):
                table.add_row("  Image", tpl['imageName'])

        console.print(Panel(table, title="[bold]Endpoints using external/deleted templates[/bold]", border_style="yellow"))
