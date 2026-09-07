#!/usr/bin/env python3
"""Fetch Runpod affiliate program earnings summary."""
import argparse
import json

import rpapi
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


def get_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Get Runpod affiliate program earnings (affiliateProgramEarnings)",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Print raw JSON instead of a table",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    console = Console()
    api = rpapi.API()

    with console.status("[bold cyan]Fetching affiliate earnings...[/bold cyan]"):
        response = api.get_affiliate_program_earnings()

    if response.status_code != 200:
        console.print(f"[red]HTTP {response.status_code}[/red]")
        try:
            console.print(json.dumps(response.json(), indent=4, default=str))
        except json.JSONDecodeError:
            console.print(response.text)
        exit(1)

    resp_json = response.json()

    if "errors" in resp_json:
        console.print("[red]ERROR:[/red]")
        for error in resp_json["errors"]:
            console.print(f"  {error['message']}")
        exit(1)

    data = resp_json.get("data", {})
    earnings = data.get("affiliateProgramEarnings")
    if earnings is None:
        earnings = resp_json.get("affiliateProgramEarnings")

    if args.json_output:
        print(json.dumps(resp_json, indent=4, default=str))
        exit(0)

    if not earnings:
        console.print("[yellow]No affiliate earnings returned.[/yellow]")
        exit(0)

    def fmt(val):
        if isinstance(val, (int, float)):
            return f"${val:,.2f}"
        return str(val) if val is not None else "-"

    table = Table(
        box=box.ROUNDED,
        show_header=False,
        padding=(0, 2),
    )
    table.add_column("Field", style="bold cyan", width=24)
    table.add_column("Value", justify="right", width=18)

    table.add_row("Total Referrals", str(earnings.get("totalReferrals", "-")))
    table.add_row("Total Paid Referrals", str(earnings.get("totalPaidReferrals", "-")))
    table.add_row("Template Earnings", f"[green]{fmt(earnings.get('templateEarnings'))}[/green]")
    table.add_row("Referral Earnings", f"[green]{fmt(earnings.get('referralEarnings'))}[/green]")
    table.add_row("Referral Bonus Earnings", f"[yellow]{fmt(earnings.get('referralBonusEarnings'))}[/yellow]")
    table.add_row("Affiliate Earnings", f"[bold yellow]{fmt(earnings.get('affiliateEarnings'))}[/bold yellow]")

    console.print()
    console.print(
        Panel(
            table,
            title="[bold]Affiliate Program Earnings[/bold]",
            border_style="cyan",
            box=box.DOUBLE,
            padding=(1, 2),
        )
    )
    console.print()
