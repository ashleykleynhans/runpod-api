#!/usr/bin/env python3
"""Fetch Runpod affiliate statistics (signups / activations / revenue)."""
import argparse
import json
from datetime import datetime, timedelta, timezone

import rpapi
from rich.console import Console
from rich.table import Table
from rich import box


def get_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Get Runpod affiliate statistics (userAffiliateStatistics)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--start-date",
        dest="start_date",
        type=str,
        default=None,
        help="ISO 8601 start date, e.g. 2026-08-09T20:13:32.903Z",
    )
    parser.add_argument(
        "--end-date",
        dest="end_date",
        type=str,
        default=None,
        help="ISO 8601 end date, e.g. 2026-09-07T20:13:32.903Z",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to look back when --start-date/--end-date not given",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Print raw JSON instead of a table",
    )
    return parser.parse_args()


def _default_dates(days):
    """Return (start, end) ISO strings for the last N days."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    # Keep milliseconds like the captured request (903Z style) - use isoformat
    # but ensure Z suffix.
    return start.strftime(fmt)[:-3] + "Z", end.strftime(fmt)[:-3] + "Z"


if __name__ == "__main__":
    args = get_args()
    console = Console()
    api = rpapi.API()

    if args.start_date and args.end_date:
        start_date = args.start_date
        end_date = args.end_date
    elif args.start_date or args.end_date:
        console.print("[red]Both --start-date and --end-date must be provided together[/red]")
        exit(1)
    else:
        start_date, end_date = _default_dates(args.days)

    with console.status("[bold cyan]Fetching affiliate statistics...[/bold cyan]"):
        response = api.get_affiliate_statistics(start_date, end_date)

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

    # Payload shape: {"data": {"userAffiliateStatistics": [...]}} 
    data = resp_json.get("data", {})
    stats = data.get("userAffiliateStatistics")
    # Fallback: some responses nest differently
    if stats is None:
        stats = resp_json.get("userAffiliateStatistics", [])

    if args.json_output:
        print(json.dumps(resp_json, indent=4, default=str))
        exit(0)

    if not stats:
        console.print("[yellow]No affiliate statistics returned for the given period.[/yellow]")
        console.print(f"  Start: {start_date}")
        console.print(f"  End:   {end_date}")
        exit(0)

    table = Table(
        title=f"Affiliate Statistics  ({start_date} -> {end_date})",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        padding=(0, 1),
    )
    table.add_column("Date", style="dim")
    table.add_column("Signups", justify="right")
    table.add_column("Activations", justify="right", style="green")
    table.add_column("Revenue", justify="right", style="yellow")

    total_signups = 0
    total_activations = 0
    total_revenue = 0.0

    for row in sorted(stats, key=lambda r: r.get("date", "")):
        date = row.get("date", "-")[:10]
        signups = row.get("signups", 0) or 0
        activations = row.get("activations", 0) or 0
        revenue = row.get("revenue", 0) or 0
        total_signups += signups
        total_activations += activations
        try:
            total_revenue += float(revenue)
        except (TypeError, ValueError):
            pass
        table.add_row(
            date,
            str(signups),
            str(activations),
            f"${float(revenue):,.2f}" if isinstance(revenue, (int, float)) else str(revenue),
        )

    table.add_section()
    table.add_row(
        "[bold]TOTAL[/bold]",
        f"[bold]{total_signups}[/bold]",
        f"[bold green]{total_activations}[/bold green]",
        f"[bold yellow]${total_revenue:,.2f}[/bold yellow]",
    )

    console.print(table)
