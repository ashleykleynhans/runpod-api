#!/usr/bin/env python3
import runpod
import json
import sys
from rich.console import Console


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <from-template-name> <to-template-name>")
        print(f"Example: {sys.argv[0]} COMFYUI-DEV COMFYUI")
        exit(1)

    from_name = sys.argv[1]
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
    templates = {t['name']: t['id'] for t in myself.get('podTemplates', [])}
    endpoints = myself.get('endpoints', [])

    if from_name not in templates:
        console.print(f"[red]Template '{from_name}' not found.[/red] Available templates:")
        for name in sorted(templates):
            console.print(f"  {name}")
        exit(1)

    if to_name not in templates:
        console.print(f"[red]Template '{to_name}' not found.[/red] Available templates:")
        for name in sorted(templates):
            console.print(f"  {name}")
        exit(1)

    from_id = templates[from_name]
    to_id = templates[to_name]

    matching = [ep for ep in endpoints if ep['templateId'] == from_id]

    if not matching:
        console.print(f"[yellow]No endpoints found using template '{from_name}'[/yellow]")
        exit(0)

    console.print(f"Switching [bold]{len(matching)}[/bold] endpoint(s) from [red]{from_name}[/red] to [green]{to_name}[/green]:\n")
    for ep in matching:
        console.print(f"  {ep['name']}  [dim]{ep['id']}[/dim]")

    console.print()
    confirm = console.input("[bold]Proceed? (y/N): [/bold]")
    if confirm.lower() != 'y':
        console.print("[yellow]Aborted.[/yellow]")
        exit(0)

    serverless = runpod.Serverless()
    for ep in matching:
        resp = serverless.update_endpoint_template(ep['id'], to_id)
        resp_json = resp.json()
        if resp.status_code == 200 and 'errors' not in resp_json:
            console.print(f"  [green]Updated[/green] {ep['name']}")
        else:
            console.print(f"  [red]Failed[/red] {ep['name']}")
            console.print_json(json.dumps(resp_json, default=str))

    console.print("\n[bold green]Done.[/bold green]")
