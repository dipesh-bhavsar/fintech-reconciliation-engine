from rich.console import Console
from rich.table import Table
from rich import box
console=Console()
STYLES={'matched':'green','amount_mismatch':'yellow','date_mismatch':'dark_orange','missing_in_b':'red','missing_in_a':'red'}
def print_summary(results):
    t=Table(title='Reconciliation Results',box=box.ROUNDED,show_lines=True)
    for c in ['ID','Status','Amt A','Amt B','Diff','Notes']:t.add_column(c)
    for r in results:
        s=STYLES.get(r.status,'')
        t.add_row(r.transaction_id,f'[{s}]{r.status}[/{s}]',str(r.amount_a or '-'),str(r.amount_b or '-'),f'{r.amount_diff:.2f}' if r.amount_diff else '-',r.notes)
    console.print(t)
    total=len(results);matched=sum(1 for r in results if r.status=='matched')
    console.print(f'\n  Matched:[green]{matched}[/green]/{total} Issues:[red]{total-matched}[/red]')
