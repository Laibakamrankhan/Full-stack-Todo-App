"""Display functions for the Todo Console App using Rich."""

from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.text import Text
from todo_console_app.models.task import Task


def display_tasks_table(tasks: List[Task], console: Optional[Console] = None) -> None:
    """Display tasks in a rich table format."""
    if console is None:
        console = Console()

    if not tasks:
        console.print("[bold]No tasks found[/bold]")
        return

    table = Table(title="Todo Tasks", show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("#", style="dim", width=3)  # Serial number
    table.add_column("ID", style="dim", width=8)  # Shortened ID
    table.add_column("Title", style="bold", min_width=15)
    table.add_column("Description", min_width=20)
    table.add_column("Status", justify="center", width=10)

    for index, task in enumerate(tasks, 1):
        status_text = "[green]Completed[/green]" if task.status.value == "completed" else "[yellow]Pending[/yellow]"
        description = task.description if task.description else ""
        # Show shortened ID (first 8 characters) to fit in table
        short_id = str(task.id)[:8] if len(str(task.id)) > 8 else str(task.id)
        table.add_row(str(index), short_id, task.title, description, status_text)

    console.print(table)


def display_success_message(message: str, console: Optional[Console] = None) -> None:
    """Display a success message."""
    if console is None:
        console = Console()
    console.print(f"[bold green]SUCCESS: {message}[/bold green]")


def display_error_message(message: str, console: Optional[Console] = None) -> None:
    """Display an error message."""
    if console is None:
        console = Console()
    console.print(f"[bold red]ERROR: {message}[/bold red]")


def display_info_message(message: str, console: Optional[Console] = None) -> None:
    """Display an info message."""
    if console is None:
        console = Console()
    console.print(f"[bold blue]INFO: {message}[/bold blue]")