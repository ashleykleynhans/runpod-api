#!/usr/bin/env python3
import runpod
import json
import sys
from rich.console import Console


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <endpoint-name> <to-template-name>")
        print(f"Example: {sys.argv[0]} my-endpoint COMFYUI")
        exit(1)

    endpoint_name = sys.argv[1]
    to_name = sys.argv[2]

    console = Console()
    api = runpod.API()
    response = api.get_templates_and_endpoints()
    resp_json = response.json()

    if response.status_code != 200 or 'errors' in resp_json:
        console.print(f"[red]ERROR fetching data[/red]")
        console.print_json(json.dumps(resp_json, default=str))
        exit(1)

    myself = resp_json['data']['myself']
    templates = {t['name']: t for t in myself.get('podTemplates', [])}
    endpoints = myself.get('endpoints', [])

    # Find the endpoint by name
    matching = [ep for ep in endpoints if ep['name'] == endpoint_name]

    if not matching:
        console.print(f"[red]Endpoint '{endpoint_name}' not found.[/red] Available endpoints:")
        for ep in sorted(endpoints, key=lambda e: e['name']):
            tpl = ep.get('template') or {}
            tpl_name = tpl.get('name', '?')
            console.print(f"  {ep['name']}  [dim]{ep['id']}  ({tpl_name})[/dim]")
        exit(1)

    if len(matching) > 1:
        console.print(f"[yellow]Multiple endpoints named '{endpoint_name}':[/yellow]")
        for ep in matching:
            console.print(f"  {ep['name']}  [dim]{ep['id']}[/dim]")
        console.print("[yellow]Please rename them so names are unique, or use serverless/update_endpoint_template.py with IDs.[/yellow]")
        exit(1)

    endpoint = matching[0]

    if to_name not in templates:
        console.print(f"[red]Template '{to_name}' not found.[/red] Available templates:")
        for name in sorted(templates):
            console.print(f"  {name}")
        exit(1)

    to_template = templates[to_name]
    current_tpl = endpoint.get('template') or {}
    current_name = current_tpl.get('name', '?')

    if endpoint['templateId'] == to_template['id']:
        console.print(f"[yellow]Endpoint '{endpoint_name}' already uses template '{to_name}'.[/yellow]")
        exit(0)

    console.print(f"Endpoint:  [bold]{endpoint['name']}[/bold]  [dim]{endpoint['id']}[/dim]")
    console.print(f"From:      [red]{current_name}[/red]")
    console.print(f"To:        [green]{to_name}[/green]")

    console.print()
    confirm = console.input("[bold]Proceed? (y/N): [/bold]")
    if confirm.lower() != 'y':
        console.print("[yellow]Aborted.[/yellow]")
        exit(0)

    serverless = runpod.Serverless()
    resp = serverless.update_endpoint_template(endpoint['id'], to_template['id'])
    resp_json = resp.json()

    if resp.status_code == 200 and 'errors' not in resp_json:
        console.print(f"\n[bold green]Updated {endpoint['name']} to {to_name}.[/bold green]")
    else:
        console.print(f"\n[red]Failed to update {endpoint['name']}[/red]")
        console.print_json(json.dumps(resp_json, default=str))
        exit(1)
