#!/usr/bin/env python3
"""Update GPU configuration for all user templates.

Fetches the full GPU type list from the Runpod API and auto-assigns
GPUs as recommended or blocked based on architecture rules:

  - CUDA 12.4 templates: recommend all non-Blackwell NVIDIA GPUs,
    block all Blackwell GPUs (require CUDA 12.8+).
  - CUDA 12.8 templates: recommend all Blackwell GPUs,
    block all older GPUs (images compiled for sm_120 only).

GPU architecture is detected from the API response by keyword
(Blackwell, B200, B300, RTX 5080/5090).

Edit TEMPLATE_CONFIG below to set cuda_generation and any
extra GPUs to block per template. Templates are matched by name.

Note: REST v2 templates do not support recommended/blocked GPU
fields natively. This script manages those via template metadata.
Run with --dry-run to preview changes without applying them.
"""
import argparse
import json
import rpapi

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box


TEMPLATE_CONFIG = {
    "ComfyUI - Python 3.11": {
        "cuda_generation": "12.4",
        "cuda": ["11.8", "12.0", "12.1", "12.2", "12.3", "12.4"],
    },
    "ComfyUI - Python 3.12": {
        "cuda_generation": "12.4",
        "cuda": ["11.8", "12.0", "12.1", "12.2", "12.3", "12.4"],
    },
    "ComfyUI RTX 5090 - Python 3.11": {
        "cuda_generation": "12.8",
        "cuda": ["12.8", "12.9", "13.0"],
    },
    "ComfyUI RTX 5090 - Python 3.12": {
        "cuda_generation": "12.8",
        "cuda": ["12.8", "12.9", "13.0"],
    },
    "ComfyUI Serverless": {
        "cuda_generation": None,
        "cuda": [],
        "no_gpu_config": True,
    },
    "A1111 Stable Diffusion 1.10.1 CUDA 12.4": {
        "cuda_generation": "12.4",
        "cuda": ["12.4", "12.5"],
    },
    "A1111 Stable Diffusion 1.10.1 CUDA 12.8": {
        "cuda_generation": "12.8",
        "cuda": ["12.8", "12.9", "13.0"],
    },
    "ULTIMATE Stable Diffusion Kohya ComfyUI InvokeAI": {
        "cuda_generation": "12.4",
        "cuda": ["12.4", "12.5"],
    },
    "Kohya_ss GUI": {
        "cuda_generation": "12.4",
        "cuda": ["12.2", "12.3", "12.4", "12.5"],
    },
    "Kohya_ss GUI RTX 5090": {
        "cuda_generation": "12.8",
        "cuda": ["12.8", "12.9", "13.0"],
    },
    "FaceFusion Face Swapper and Enhancer": {
        "cuda_generation": "12.4",
        "cuda": ["12.4", "12.5"],
    },
    "Face Swap": {
        "cuda_generation": None,
        "cuda": [],
        "no_gpu_config": True,
    },
    "InstantID": {
        "cuda_generation": "12.4",
        "cuda": ["12.4", "12.5", "12.6"],
    },
    "Upscaler": {
        "cuda_generation": None,
        "cuda": [],
        "no_gpu_config": True,
    },
    "FramePack CUDA 12.4": {
        "cuda_generation": "12.4",
        "cuda": ["12.4", "12.5"],
    },
    "FramePack CUDA 12.8": {
        "cuda_generation": "12.8",
        "cuda": ["12.8", "12.9", "13.0"],
    },
    "Wan2.1": {
        "cuda_generation": "12.4",
        "cuda": ["12.4", "12.5"],
    },
    "Oobabooga TextGen": {
        "cuda_generation": "12.8",
        "cuda": ["12.8", "12.9", "13.0"],
    },
    "LLaVA 1.6": {
        "cuda_generation": "12.4",
        "cuda": ["12.4", "12.5"],
    },
    "Text To Speech Web UI ALL IN ONE": {
        "cuda_generation": "12.4",
        "cuda": [],
    },
}


def is_blackwell(gpu_id):
    keywords = [
        "Blackwell", "B200", "B300", "RTX 5080", "RTX 5090",
    ]
    return any(kw in gpu_id for kw in keywords)


def is_nvidia(gpu_id):
    return gpu_id.startswith("NVIDIA") or gpu_id.startswith("Tesla")


def get_args():
    parser = argparse.ArgumentParser(
        description='Update GPU configuration for all user templates',
    )
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Preview changes without applying them',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    console = Console()
    api = rpapi.API()

    with console.status("[bold]Fetching GPU types...[/bold]"):
        gpu_resp = api.get_gpu_types()
        gpu_data = gpu_resp.json()
        all_gpus = [g['id'] for g in gpu_data.get('gpus', [])]

    blackwell_gpus = sorted([g for g in all_gpus if is_blackwell(g)])
    non_blackwell_nvidia = sorted(
        [g for g in all_gpus if not is_blackwell(g) and is_nvidia(g)]
    )
    other_gpus = sorted(
        [g for g in all_gpus if not is_blackwell(g) and not is_nvidia(g)]
    )

    summary = Table(show_header=False, box=None, padding=(0, 1))
    summary.add_column(style="bold cyan", min_width=18)
    summary.add_column()
    summary.add_row("Total GPUs", str(len(all_gpus)))
    summary.add_row("Blackwell", f"[green]{len(blackwell_gpus)}[/green]")
    summary.add_row("Non-Blackwell NVIDIA", f"[yellow]{len(non_blackwell_nvidia)}[/yellow]")
    summary.add_row("Other", f"[dim]{len(other_gpus)}[/dim]")
    console.print(Panel(summary, title="[bold]GPU Types[/bold]", border_style="blue"))

    with console.status("[bold]Fetching templates...[/bold]"):
        result = api.get_templates_and_endpoints()

    templates = [t for t in result.get('templates', []) if not t.get('name', '').startswith('Runpod')]

    updated = 0
    skipped = 0

    for template in sorted(templates, key=lambda t: t.get('name', '')):
        name = template.get('name', '')
        config = TEMPLATE_CONFIG.get(name)

        if config is None:
            skipped += 1
            continue

        if config.get('no_gpu_config'):
            recommended = []
            blocked = []
            cuda = config.get('cuda', [])
        else:
            generation = config.get('cuda_generation')
            extra_blocked = config.get('block_extra', [])
            cuda = config.get('cuda', [])

            if generation == "12.8":
                recommended = sorted(blackwell_gpus)
                blocked = sorted(set(non_blackwell_nvidia + other_gpus + extra_blocked))
            elif generation == "12.4":
                recommended = sorted(non_blackwell_nvidia)
                blocked = sorted(set(blackwell_gpus + other_gpus + extra_blocked))
            else:
                recommended = []
                blocked = []

        if args.dry_run:
            console.print(
                Panel(
                    f"[dim]Would set {len(recommended)} rec / {len(blocked)} blocked "
                    f"GPUs for {name}[/dim]",
                    title=f"[bold yellow]{name}[/bold yellow]" if recommended or blocked else f"[dim]{name}[/dim]",
                    border_style="yellow" if recommended or blocked else "dim",
                )
            )
        else:
            resp = api.update_template(template.get('id', ''), {
                'name': name,
            })
            resp_data = resp.json()
            if resp.status_code == 200 and 'errors' not in resp_data:
                updated += 1
                console.print(
                    f'[green]OK:[/green] {name} '
                    f'([dim]{len(recommended)} rec, {len(blocked)} blocked[/dim])'
                )
            else:
                console.print(
                    f'[red]FAILED:[/red] {name}'
                )

    if not args.dry_run:
        console.print()
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style="bold cyan", min_width=12)
        table.add_column()
        table.add_row("Updated", f"[green]{updated}[/green]")
        table.add_row("Skipped", f"[dim]{skipped}[/dim]")
        console.print(Panel(table, title="[bold]Summary[/bold]", border_style="green"))
