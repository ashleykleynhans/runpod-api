#!/usr/bin/env python3
import rpapi
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
    api = rpapi.API()
    result = api.get_templates_and_endpoints()

    templates_list = result.get('templates', [])
    templates = {t.get('name', ''): t for t in templates_list}
    endpoints = result.get('endpoints', [])

    # Find the endpoint by name
    matching = [ep for ep in endpoints if ep.get('name') == endpoint_name]

    if not matching:
        console.print(f"[red]Endpoint '{endpoint_name}' not found.[/red] Available endpoints:")
        for ep in sorted(endpoints, key=lambda e: e.get('name', '')):
            console.print(f"  {ep.get('name')}  [dim]{ep.get('id')}[/dim]")
        exit(1)

    if len(matching) > 1:
        console.print(f"[yellow]Multiple endpoints named '{endpoint_name}':[/yellow]")
        for ep in matching:
            console.print(f"  {ep.get('name')}  [dim]{ep.get('id')}[/dim]")
        exit(1)

    endpoint = matching[0]

    if to_name not in templates:
        console.print(f"[red]Template '{to_name}' not found.[/red] Available templates:")
        for name in sorted(templates):
            console.print(f"  {name}")
        exit(1)

    to_template = templates[to_name]
    current_tpl_id = endpoint.get('templateId', '?')

    if endpoint.get('templateId') == to_template.get('id'):
        console.print(f"[yellow]Endpoint '{endpoint_name}' already uses template '{to_name}'.[/yellow]")
        exit(0)

    console.print(f"Endpoint:  [bold]{endpoint.get('name')}[/bold]  [dim]{endpoint.get('id')}[/dim]")
    console.print(f"From:      [red]{current_tpl_id}[/red]")
    console.print(f"To:        [green]{to_name}[/green]")

    console.print()
    confirm = console.input("[bold]Proceed? (y/N): [/bold]")
    if confirm.lower() != 'y':
        console.print("[yellow]Aborted.[/yellow]")
        exit(0)

    serverless = rpapi.Serverless()
    resp = serverless.update_endpoint_template(endpoint.get('id'), to_template.get('id'))
    resp_json = resp.json()

    if resp.status_code == 200 and 'errors' not in resp_json:
        console.print(f"\n[bold green]Updated {endpoint.get('name')} to {to_name}.[/bold green]")
    else:
        console.print(f"\n[red]Failed to update {endpoint.get('name')}[/red]")
        console.print_json(json.dumps(resp_json, default=str))
        exit(1)
