#!/usr/bin/env python3
import rpapi
import json
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


if __name__ == '__main__':
    console = Console()
    api = rpapi.API()
    result = api.get_templates_and_endpoints()

    templates = result.get('templates', [])
    endpoints = result.get('endpoints', [])

    # Filter out Runpod system templates
    templates = [t for t in templates if not t.get('name', '').startswith('Runpod')]

    endpoints_by_template = defaultdict(list)
    for ep in endpoints:
        tid = ep.get('templateId') or ep.get('id')
        endpoints_by_template[tid].append(ep)

    for template in sorted(templates, key=lambda t: t.get('name', '')):
        tid = template.get('id', '')
        associated = endpoints_by_template.get(tid, [])

        title = template.get('name', '')
        if associated:
            title += f" ({len(associated)} endpoint{'s' if len(associated) != 1 else ''})"

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style="bold cyan", min_width=10)
        table.add_column()
        table.add_row("ID", tid)
        table.add_row("Image", template.get('image', ''))
        table.add_row("Public", str(template.get('public', '')))
        table.add_row("Serverless", str(template.get('serverless', '')))

        if associated:
            for i, ep in enumerate(associated):
                gpu_info = ep.get('gpu', {})
                gpu_pools = gpu_info.get('pools', []) if isinstance(gpu_info, dict) else []
                gpu_list = ', '.join(gpu_pools) if gpu_pools else ''
                workers = ep.get('workers', {})
                if isinstance(workers, dict):
                    w_min = workers.get('min', '?')
                    w_max = workers.get('max', '?')
                else:
                    w_min = w_max = '?'
                if i == 0:
                    table.add_row("", "")
                ep_text = Text()
                ep_text.append(ep.get('name', ''), style="bold")
                ep_text.append(f"  {ep.get('id', '')}", style="dim")
                table.add_row("Endpoint", ep_text)
                table.add_row("  Workers", f"{w_min}-{w_max}")
                if gpu_list:
                    table.add_row("  GPU Pools", gpu_list)

        border_style = "green" if associated else "dim"
        console.print(Panel(table, title=f"[bold]{title}[/bold]", border_style=border_style))

    user_template_ids = {t.get('id') for t in templates}
    orphaned = [ep for ep in endpoints if ep.get('templateId') not in user_template_ids]
    if orphaned:
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style="bold cyan", min_width=14)
        table.add_column()
        for i, ep in enumerate(orphaned):
            if i > 0:
                table.add_row("", "")
            ep_text = Text()
            ep_text.append(ep.get('name', ''), style="bold")
            ep_text.append(f"  {ep.get('id', '')}", style="dim")
            table.add_row("Endpoint", ep_text)
            table.add_row("  Template ID", ep.get('templateId', ''))

        console.print(Panel(table, title="[bold]Endpoints using external templates[/bold]", border_style="yellow"))
