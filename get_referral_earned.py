#!/usr/bin/env python3
"""Display Runpod referral earnings with rich formatting."""
import json
import time

import rpapi
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box


if __name__ == '__main__':
    console = Console()
    runpod = rpapi.API()

    with console.status('[bold cyan]Fetching account data...[/bold cyan]'):
        response = runpod.get_myself()

    if response.status_code != 200:
        console.print(f'[red]HTTP {response.status_code}[/red]')
        try:
            console.print(json.dumps(response.json(), indent=4, default=str))
        except json.JSONDecodeError:
            console.print(response.text)
        exit(1)

    resp_json = response.json()

    data = resp_json.get('data')
    if not data or not data.get('myself'):
        if 'errors' in resp_json:
            console.print('[red]ERROR:[/red]')
            for error in resp_json['errors']:
                console.print(f'  {error["message"]}')
        else:
            console.print('[red]No data returned[/red]')
        exit(1)

    myself = data['myself']
    referral_earned = myself.get('referralEarned') or 0
    template_earned = myself.get('templateEarned') or 0
    total_earned = referral_earned + template_earned
    balance = myself.get('clientBalance') or 0
    lifetime_spend = myself.get('clientLifetimeSpend') or 0
    current_spend = myself.get('currentSpendPerHr') or 0
    referral_id = myself.get('referralId', 'N/A')
    referral = myself.get('referral', {})

    def fmt_dollars(amount):
        color = 'green' if amount >= 0 else 'red'
        return f'[bold {color}]${amount:,.2f}[/bold {color}]'

    date_str = time.strftime('%A, %B %d %Y  %I:%M:%S %p')

    # Earnings table
    earnings = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style='bold cyan',
        padding=(0, 2),
    )
    earnings.add_column('Category', style='bold white', width=22)
    earnings.add_column('Amount', justify='right', width=18)

    earnings.add_row(
        ':handshake: Referral Earnings',
        fmt_dollars(referral_earned),
    )
    earnings.add_row(
        ':page_facing_up: Template Earnings',
        fmt_dollars(template_earned),
    )
    earnings.add_row(
        '',
        '',
    )
    earnings.add_row(
        '[bold yellow]:star: Total Earned[/bold yellow]',
        f'[bold yellow]${total_earned:,.2f}[/bold yellow]',
    )

    # Account overview
    overview = Table(
        box=box.SIMPLE,
        show_header=False,
        padding=(0, 2),
    )
    overview.add_column('', style='dim', width=16)
    overview.add_column('', width=16)

    overview.add_row('Balance', fmt_dollars(balance))
    overview.add_row('Lifetime Spend', fmt_dollars(lifetime_spend))
    overview.add_row('Spend/hr', f'${current_spend:.4f}')
    overview.add_row('Referral ID', f'[dim]{referral_id}[/dim]')

    if referral:
        code = referral.get('code', 'N/A')
        month = referral.get('currentMonth', {})
        total_refs = month.get('totalReferrals', 0)
        ref_spend = month.get('totalSpend', 0)
        overview.add_row('Referral Code', f'[bold magenta]{code}[/bold magenta]')
        overview.add_row('Refs This Month', str(total_refs))
        overview.add_row('Ref Spend/mo', fmt_dollars(ref_spend))

    # Compose layout
    console.print()
    panel = Panel(
        earnings,
        title='[bold]Runpod Referral Earnings[/bold]',
        subtitle=f'[dim]{date_str}[/dim]',
        border_style='cyan',
        box=box.DOUBLE,
        padding=(1, 2),
    )
    console.print(panel)
    console.print(overview)
    console.print()
